"""

SporeStack API request/response models

"""


from typing import Dict, List, Optional

from pydantic import BaseModel

from .models import Flavor, NetworkInterface, Payment


class TokenAdd:
    url = "/token/{token}/add"
    method = "POST"

    class Request(BaseModel):
        currency: str
        dollars: int
        affiliate_token: Optional[str] = None

    class Response(BaseModel):
        token: str
        payment: Payment


class TokenBalance:
    url = "/token/{token}/balance"
    method = "GET"

    class Response(BaseModel):
        token: str
        cents: int
        usd: str


class ServerLaunch:
    url = "/server/{machine_id}/launch"
    method = "POST"

    class Request(BaseModel):
        days: int
        flavor: str
        ssh_key: str
        operating_system: str
        region: Optional[str] = None
        """null is automatic, otherwise a string region slug."""
        token: str
        """Token to draw from when launching the server."""
        quote: bool = False
        """Don't launch, get a quote on how much it would cost"""
        affiliate_token: Optional[str] = None
        hostname: str = ""
        """Hostname to refer to your server by."""
        autorenew: bool = False
        """
        Automatically renew the server with the token used, keeping it at 1 week
        expiration.
        """

    class Response(BaseModel):
        payment: Payment
        """Deprecated, not needed when paying with token. Only used for quote."""
        expiration: int
        machine_id: str
        network_interfaces: List[NetworkInterface] = []
        """Deprecated, use ipv4/ipv6 from ServerInfo instead."""
        created_at: int = 0
        region: Optional[str] = None
        """Deprecated, use ServerInfo instead."""
        created: bool = False
        paid: bool = False
        """Deprecated, not needed when paying with token."""
        warning: Optional[str] = None
        flavor: str = ""
        """Deprecated, use ServerInfo instead."""


class ServerTopup:
    url = "/server/{machine_id}/topup"
    method = "POST"

    class Request(BaseModel):
        days: int
        token: str
        quote: bool = False
        affiliate_token: Optional[str] = None

    class Response(BaseModel):
        machine_id: str
        payment: Payment
        """Deprecated, not needed when paying with token."""
        expiration: int
        paid: bool = False
        """Deprecated, not needed when paying with token."""
        warning: Optional[str] = None


class ServerInfo:
    url = "/server/{machine_id}/info"
    method = "GET"

    class Response(BaseModel):
        created_at: int
        expiration: int
        running: bool
        machine_id: str
        token: str
        ipv4: str
        ipv6: str
        region: str
        flavor: Flavor
        deleted: bool
        network_interfaces: List[NetworkInterface]
        """Deprecated, use ipv4/ipv6 instead."""
        operating_system: str
        hostname: str
        autorenew: bool


class ServerStart:
    url = "/server/{machine_id}/start"
    method = "POST"


class ServerStop:
    url = "/server/{machine_id}/stop"
    method = "POST"


class ServerDelete:
    url = "/server/{machine_id}/delete"
    method = "POST"


class ServerDestroy:
    url = "/server/{machine_id}/destroy"
    method = "POST"


class ServerForget:
    url = "/server/{machine_id}/forget"
    method = "POST"


class ServerRebuild:
    url = "/server/{machine_id}/rebuild"
    method = "POST"


class ServerEnableAutorenew:
    url = "/server/{machine_id}/autorenew/enable"
    method = "POST"


class ServerDisableAutorenew:
    url = "/server/{machine_id}/autorenew/disable"
    method = "POST"


class ServersLaunchedFromToken:
    url = "/token/{token}/servers"
    method = "GET"

    class Response(BaseModel):
        servers: List[ServerInfo.Response]


class Flavors:
    url = "/flavors"
    method = "GET"

    class Response(BaseModel):
        flavors: Dict[str, Flavor]


class OperatingSystems:
    url = "/operatingsystems"
    method = "GET"

    class Response(BaseModel):
        operating_systems: List[str]
