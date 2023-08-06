"""
SporeStack CLI: `sporestack`
"""

import importlib.util
import json
import logging
import os
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, Optional

import typer

from . import __version__


def lazy_import(name: str) -> ModuleType:
    """
    Lazily import a module. Helps speed up CLI performance.
    """
    spec = importlib.util.find_spec(name)
    assert spec is not None
    assert spec.loader is not None
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


# For mypy
if TYPE_CHECKING:
    from . import api_client
else:
    api_client = lazy_import("sporestack.api_client")

HELP = """
SporeStack Python CLI

Optional environment variables:
SPORESTACK_ENDPOINT
*or*
SPORESTACK_USE_TOR_ENDPOINT

TOR_PROXY (defaults to socks5h://127.0.0.1:9050 which is fine for most)
"""

_home = os.getenv("HOME", None)
assert _home is not None, "Unable to detect $HOME environment variable?"
HOME = Path(_home)

SPORESTACK_DIR = HOME / ".sporestack"

# Try to protect files in ~/.sporestack
os.umask(0o0077)

cli = typer.Typer(help=HELP)

HOME = Path(_home)

token_cli = typer.Typer(help="Commands to interact with SporeStack tokens")
cli.add_typer(token_cli, name="token")
server_cli = typer.Typer(help="Commands to interact with SporeStack servers")
cli.add_typer(server_cli, name="server")

logging.basicConfig(level=logging.INFO)

DEFAULT_TOKEN = "primary"
DEFAULT_FLAVOR = "vps-1vcpu-1gb"
# Users may have a different key file, but this is the most common.
DEFAULT_SSH_KEY_FILE = HOME / ".ssh" / "id_rsa.pub"

# On disk format
TOKEN_VERSION = 1

WAITING_PAYMENT_TO_PROCESS = "Waiting for payment to process..."


def get_api_endpoint() -> str:
    api_endpoint = os.getenv("SPORESTACK_ENDPOINT", api_client.CLEARNET_ENDPOINT)
    if os.getenv("SPORESTACK_USE_TOR_ENDPOINT", None) is not None:
        api_endpoint = api_client.TOR_ENDPOINT
    return api_endpoint


def make_payment(currency: str, uri: str, usd: str) -> None:
    import segno

    premessage = """Payment URI: {}
Pay *exactly* the specified amount. No more, no less. Pay within
one hour at the very most.
Resize your terminal and try again if QR code above is not readable.
Press ctrl+c to abort."""
    message = premessage.format(uri)
    qr = segno.make(uri)
    # This typer.echos.
    qr.terminal()
    typer.echo(message)
    typer.echo(f"Approximate price in USD: {usd}")
    input("[Press enter once you have made payment.]")


@server_cli.command()
def launch(
    hostname: str = "",
    days: int = typer.Option(...),
    operating_system: str = typer.Option(...),
    ssh_key_file: Path = DEFAULT_SSH_KEY_FILE,
    flavor: str = DEFAULT_FLAVOR,
    token: str = DEFAULT_TOKEN,
    region: Optional[str] = None,
    quote: bool = typer.Option(True, help="Require manual price confirmation."),
    autorenew: bool = typer.Option(False, help="BETA: Automatically renew server."),
) -> None:
    """
    Launch a server on SporeStack.
    """

    from . import utils

    typer.echo(f"Launching server with token {token}...", err=True)
    _token = load_token(token)

    typer.echo(f"Loading SSH key from {ssh_key_file}...")
    if not ssh_key_file.exists():
        msg = f"{ssh_key_file} does not exist. "
        msg += "You can try generating a key file with `ssh-keygen`"
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    ssh_key = ssh_key_file.read_text()

    machine_id = utils.random_machine_id()

    if quote:
        response = api_client.launch(
            machine_id=machine_id,
            days=days,
            flavor=flavor,
            operating_system=operating_system,
            ssh_key=ssh_key,
            region=region,
            token=_token,
            api_endpoint=get_api_endpoint(),
            retry=True,
            quote=True,
            hostname=hostname,
            autorenew=autorenew,
        )

        msg = f"Is {response.payment.usd} for {days} day(s) of {flavor} okay?"
        typer.echo(msg, err=True)
        input("[Press ctrl+c to cancel, or enter to accept.]")

    if autorenew:
        typer.echo(
            "Server will be automatically renewed (from this token) to one week of expiration.",  # noqa: E501
            err=True,
        )
        typer.echo(
            "If using this feature, watch your token balance and server expiration closely!",  # noqa: E501
            err=True,
        )

    tries = 360
    while tries > 0:
        response = api_client.launch(
            machine_id=machine_id,
            days=days,
            flavor=flavor,
            operating_system=operating_system,
            ssh_key=ssh_key,
            region=region,
            token=_token,
            hostname=hostname,
            autorenew=autorenew,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        if response.created is True:
            break
        typer.echo("Waiting for server to build...", err=True)
        tries = tries + 1
        # Waiting for server to spin up.
        time.sleep(10)

    if response.created is False:
        typer.echo("Server creation failed, tries exceeded.", err=True)
        raise typer.Exit(code=1)

    typer.echo(
        pretty_machine_info(
            api_client.info(
                machine_id=machine_id, api_endpoint=get_api_endpoint()
            ).dict()
        )
    )


@server_cli.command()
def topup(
    hostname: str = "",
    machine_id: str = "",
    days: int = typer.Option(...),
    token: str = DEFAULT_TOKEN,
) -> None:
    """
    Extend an existing SporeStack server's lifetime.
    """

    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)

    _token = load_token(token)

    response = api_client.topup(
        machine_id=machine_id,
        days=days,
        api_endpoint=get_api_endpoint(),
        token=_token,
        retry=True,
    )
    assert response.payment.paid is True

    typer.echo(response.expiration)


def server_info_path() -> Path:
    # Put servers in a subdirectory
    servers_dir = SPORESTACK_DIR / "servers"

    # Migrate existing server.json files into servers subdirectory
    if SPORESTACK_DIR.exists() and not servers_dir.exists():
        typer.echo(
            f"Migrating server profiles found in {SPORESTACK_DIR} to {servers_dir}.",
            err=True,
        )
        servers_dir.mkdir()
        for json_file in SPORESTACK_DIR.glob("*.json"):
            json_file.rename(servers_dir / json_file.name)

    # Make it, if it doesn't exist already.
    SPORESTACK_DIR.mkdir(exist_ok=True)
    servers_dir.mkdir(exist_ok=True)

    return servers_dir


def token_path() -> Path:
    token_dir = SPORESTACK_DIR / "tokens"

    # Make it, if it doesn't exist already.
    token_dir.mkdir(exist_ok=True, parents=True)

    return token_dir


def get_machine_info(hostname: str) -> Dict[str, Any]:
    """
    Get info from disk.
    """
    directory = server_info_path()
    json_file = directory / f"{hostname}.json"
    if not json_file.exists():
        raise ValueError(f"{hostname} does not exist in {directory} as {json_file}")
    machine_info = json.loads(json_file.read_bytes())
    assert isinstance(machine_info, dict)
    if machine_info["vm_hostname"] != hostname:
        raise ValueError("hostname does not match filename.")
    return machine_info


def pretty_machine_info(info: Dict[str, Any]) -> str:
    msg = "Machine ID (keep this secret!): {}\n".format(info["machine_id"])
    if "vm_hostname" in info:
        msg += "Hostname: {}\n".format(info["vm_hostname"])
    elif "hostname" in info:
        msg += "Hostname: {}\n".format(info["hostname"])

    if "network_interfaces" in info:
        if "ipv6" in info["network_interfaces"][0]:
            msg += "IPv6: {}\n".format(info["network_interfaces"][0]["ipv6"])
        if "ipv4" in info["network_interfaces"][0]:
            msg += "IPv4: {}\n".format(info["network_interfaces"][0]["ipv4"])
    else:
        if "ipv6" in info:
            msg += "IPv6: {}\n".format(info["ipv6"])
        if "ipv4" in info:
            msg += "IPv4: {}\n".format(info["ipv4"])
    expiration = info["expiration"]
    human_expiration = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(expiration))
    if "running" in info:
        msg += "Running: {}\n".format(info["running"])
    msg += f"Expiration: {expiration} ({human_expiration})\n"
    time_to_live = expiration - int(time.time())
    hours = time_to_live // 3600
    msg += f"Server will be deleted in {hours} hours."
    return msg


@server_cli.command(name="list")
def server_list(
    token: str = DEFAULT_TOKEN,
    local: bool = typer.Option(
        True, help="List older servers not associated to token."
    ),
) -> None:
    """
    List all locally known servers and all servers under the given token.
    """
    from .exceptions import SporeStackUserError

    _token = load_token(token)

    server_infos = api_client.servers_launched_from_token(
        token=_token, api_endpoint=get_api_endpoint()
    ).servers
    machine_id_hostnames = {}

    if local:
        directory = server_info_path()
        for hostname_json in os.listdir(directory):
            hostname = hostname_json.split(".")[0]
            saved_vm_info = get_machine_info(hostname)
            machine_id_hostnames[saved_vm_info["machine_id"]] = hostname

    printed_machine_ids = []

    for info in server_infos:
        typer.echo()

        hostname = info.hostname
        if hostname == "":
            if info.machine_id in machine_id_hostnames:
                hostname = machine_id_hostnames[info.machine_id]
        if hostname != "":
            typer.echo(f"Hostname: {hostname}")

        typer.echo(f"Machine ID (keep this secret!): {info.machine_id}")
        typer.echo(f"IPv6: {info.network_interfaces[0].ipv6}")
        typer.echo(f"IPv4: {info.network_interfaces[0].ipv4}")
        typer.echo(f"Running: {info.running}")
        typer.echo(f"Region: {info.region}")
        typer.echo(f"Flavor: {info.flavor.slug}")
        typer.echo(f"Token: {info.token}")
        typer.echo(f"Autorenew: {info.autorenew}")
        human_expiration = time.strftime(
            "%Y-%m-%d %H:%M:%S %z", time.localtime(info.expiration)
        )
        typer.echo(f"Expiration: {info.expiration} ({human_expiration})")
        time_to_live = info.expiration - int(time.time())
        hours = time_to_live // 3600
        typer.echo(f"Server will be deleted in {hours} hours.")
        if info.deleted:
            typer.echo("Server was deleted!")

        printed_machine_ids.append(info.machine_id)

    if local:
        for hostname_json in os.listdir(directory):
            hostname = hostname_json.split(".")[0]
            saved_vm_info = get_machine_info(hostname)
            machine_id = saved_vm_info["machine_id"]
            if machine_id in printed_machine_ids:
                continue

            try:
                upstream_vm_info = api_client.info(
                    machine_id=saved_vm_info["machine_id"],
                    api_endpoint=get_api_endpoint(),
                )
                saved_vm_info["expiration"] = upstream_vm_info.expiration
                saved_vm_info["running"] = upstream_vm_info.running
                typer.echo()
                typer.echo(pretty_machine_info(saved_vm_info))
            except SporeStackUserError as e:
                expiration = saved_vm_info["expiration"]
                human_expiration = time.strftime(
                    "%Y-%m-%d %H:%M:%S %z", time.localtime(expiration)
                )
                msg = hostname
                msg += f" expired ({expiration} {human_expiration}): "
                msg += str(e)
                typer.echo(msg)

    typer.echo()


def _get_machine_id(machine_id: str, hostname: str, token: str) -> str:
    usage = "--hostname *OR* --machine-id must be set."

    if machine_id != "" and hostname != "":
        typer.echo(usage, err=True)
        raise typer.Exit(code=2)

    if machine_id != "":
        return machine_id

    if hostname == "":
        typer.echo(usage, err=True)
        raise typer.Exit(code=2)

    try:
        machine_id = get_machine_info(hostname)["machine_id"]
        assert isinstance(machine_id, str)
        return machine_id
    except Exception:
        pass

    _token = load_token(token)

    for server in api_client.servers_launched_from_token(
        token=_token, api_endpoint=get_api_endpoint()
    ).servers:
        if server.hostname == hostname:
            return server.machine_id

    typer.echo(
        f"Could not find any servers matching the hostname: {hostname}", err=True
    )
    raise typer.Exit(code=1)


@server_cli.command()
def info(hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN) -> None:
    """
    Info on the VM
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    typer.echo(
        api_client.info(machine_id=machine_id, api_endpoint=get_api_endpoint()).json()
    )


@server_cli.command()
def start(hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN) -> None:
    """
    Boots the VM.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.start(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} started.")


@server_cli.command()
def stop(hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN) -> None:
    """
    Immediately shuts down the VM.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.stop(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} stopped.")


@server_cli.command()
def autorenew_enable(
    hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN
) -> None:
    """
    Enable autorenew on a server.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.autorenew_enable(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo("Autorenew enabled.")


@server_cli.command()
def autorenew_disable(
    hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN
) -> None:
    """
    Disable autorenew on a server.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.autorenew_disable(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo("Autorenew disabled.")


@server_cli.command()
def destroy(
    hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN
) -> None:
    """
    Deletes/destroys the VM before expiration (no refunds/credits)
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.destroy(machine_id=machine_id, api_endpoint=get_api_endpoint())
    # Also remove the .json file
    server_info_path().joinpath(f"{hostname}.json").unlink(missing_ok=True)
    typer.echo(f"{machine_id} was destroyed.")


@server_cli.command()
def forget(
    hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN
) -> None:
    """
    Forget about a deleted server so that it doesn't show up in server list.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.forget(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{machine_id} was forgotten.")


@server_cli.command()
def rebuild(
    hostname: str = "", machine_id: str = "", token: str = DEFAULT_TOKEN
) -> None:
    """
    Rebuilds the VM with the operating system and SSH key given at launch time.

    Will take a couple minutes to complete after the request is made.
    """
    machine_id = _get_machine_id(machine_id=machine_id, hostname=hostname, token=token)
    api_client.rebuild(machine_id=machine_id, api_endpoint=get_api_endpoint())
    typer.echo(f"{hostname} rebuilding.")


@server_cli.command()
def flavors() -> None:
    """
    Returns available flavors.
    """
    flavors = api_client.flavors(api_endpoint=get_api_endpoint()).flavors
    for flavor in flavors:
        typer.echo(f"{flavor}: {flavors[flavor]}")


@server_cli.command()
def operating_systems() -> None:
    """
    Returns available operating systems.
    """
    os_list = api_client.operating_systems(
        api_endpoint=get_api_endpoint()
    ).operating_systems
    for operating_system in os_list:
        typer.echo(operating_system)


def load_token(token: str) -> str:
    token_file = token_path().joinpath(f"{token}.json")
    if not token_file.exists():
        msg = f"Token '{token}' ({token_file}) does not exist. Create it with:\n"
        msg += f"sporestack token create {token} --dollars 20 --currency xmr\n"
        msg += "(Can do more than $20, or a different currency, like btc.)\n"
        msg += (
            "With the token credited, you can launch servers, renew existing ones, etc."
        )
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    token_data = json.loads(token_file.read_text())
    assert token_data["version"] == 1
    assert isinstance(token_data["key"], str)
    return token_data["key"]


def save_token(token: str, key: str) -> None:
    token_file = token_path().joinpath(f"{token}.json")
    if token_file.exists():
        msg = f"Token '{token}' already exists in {token_file}. Aborting!"
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)

    token_data = {"version": TOKEN_VERSION, "name": token, "key": key}
    token_file.write_text(json.dumps(token_data))


@token_cli.command(name="create")
def token_create(
    token: str = typer.Argument(DEFAULT_TOKEN),
    dollars: int = typer.Option(...),
    currency: str = typer.Option(...),
) -> None:
    """
    Enables a new settlement token.

    Dollars is starting balance.
    """
    from . import utils

    _token = utils.random_token()

    typer.echo(f"Generated key {_token} for use with token {token}", err=True)

    if Path(SPORESTACK_DIR / "tokens" / f"{token}.json").exists():
        typer.echo("Token already created! Did you mean to `topup`?", err=True)
        raise typer.Exit(1)

    response = api_client.token_add(
        token=_token,
        dollars=dollars,
        currency=currency,
        api_endpoint=get_api_endpoint(),
        retry=True,
    )

    uri = response.payment.uri
    assert uri is not None
    usd = response.payment.usd

    make_payment(currency=currency, uri=uri, usd=usd)

    tries = 360 * 2
    while tries > 0:
        typer.echo(WAITING_PAYMENT_TO_PROCESS, err=True)
        tries = tries - 1
        # FIXME: Wait two hours in a smarter way.
        # Waiting for payment to set in.
        time.sleep(10)
        response = api_client.token_add(
            token=_token,
            dollars=dollars,
            currency=currency,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        if response.payment.paid is True:
            typer.echo(f"{token} has been enabled with ${dollars}.")
            typer.echo(f"{token}'s key is {_token}.")
            typer.echo("Save it, don't share it, and don't lose it!")
            save_token(token, _token)
            return
    raise ValueError(f"{token} did not get enabled in time.")


@token_cli.command(name="import")
def token_import(
    name: str = typer.Argument(DEFAULT_TOKEN),
    key: str = typer.Option(...),
) -> None:
    """
    Imports a token from a key.
    """
    save_token(name, key)


@token_cli.command(name="topup")
def token_topup(
    token: str = typer.Argument(DEFAULT_TOKEN),
    dollars: int = typer.Option(...),
    currency: str = typer.Option(...),
) -> None:
    """
    Adds balance to an existing settlement token.
    """
    token = load_token(token)

    response = api_client.token_add(
        token,
        dollars,
        currency=currency,
        api_endpoint=get_api_endpoint(),
        retry=True,
    )

    uri = response.payment.uri
    assert uri is not None
    usd = response.payment.usd

    make_payment(currency=currency, uri=uri, usd=usd)

    tries = 360 * 2
    while tries > 0:
        typer.echo(WAITING_PAYMENT_TO_PROCESS, err=True)
        tries = tries - 1
        # FIXME: Wait two hours in a smarter way.
        response = api_client.token_add(
            token,
            dollars,
            currency=currency,
            api_endpoint=get_api_endpoint(),
            retry=True,
        )
        # Waiting for payment to set in.
        time.sleep(10)
        if response.payment.paid is True:
            typer.echo(f"Added {dollars} dollars to {token}")
            return
    raise ValueError(f"{token} did not get enabled in time.")


@token_cli.command()
def balance(token: str = typer.Argument(DEFAULT_TOKEN)) -> None:
    """
    Gets balance for a settlement token.
    """
    _token = load_token(token)

    typer.echo(
        api_client.token_balance(token=_token, api_endpoint=get_api_endpoint()).usd
    )


@token_cli.command()
def servers(token: str = typer.Argument(DEFAULT_TOKEN)) -> None:
    """
    Returns server info for servers launched by a given token.
    """
    _token = load_token(token)

    typer.echo(
        api_client.servers_launched_from_token(
            token=_token, api_endpoint=get_api_endpoint()
        )
    )


@token_cli.command(name="list")
def token_list() -> None:
    """
    Gets balance for a settlement token.
    """
    token_dir = token_path()
    typer.echo(f"SporeStack tokens present in {token_dir}:", err=True)
    typer.echo("(Name): (Key)", err=True)
    for token_file in token_dir.glob("*.json"):
        token = token_file.stem
        key = load_token(token)
        typer.echo(f"{token}: {key}")


@cli.command()
def version() -> None:
    """
    Returns the installed version.
    """
    typer.echo(__version__)


@cli.command()
def api_endpoint() -> None:
    """
    Prints the selected API endpoint: Env var: SPORESTACK_ENDPOINT,
    or, SPORESTACK_USE_TOR=1
    """
    endpoint = get_api_endpoint()
    if ".onion" in endpoint:
        typer.echo(f"{endpoint} using {api_client._get_tor_proxy()}")
        return
    else:
        typer.echo(endpoint)
        return


if __name__ == "__main__":
    cli()
