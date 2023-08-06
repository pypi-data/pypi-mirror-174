from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from sporestack import api_client


def test__is_onion_url() -> None:
    onion_url = "http://spore64i5sofqlfz5gq2ju4msgzojjwifls7"
    onion_url += "rok2cti624zyq3fcelad.onion/v2/"
    assert api_client._is_onion_url(onion_url) is True
    # This is a good, unusual test.
    onion_url = "https://www.facebookcorewwwi.onion/"
    assert api_client._is_onion_url(onion_url) is True
    assert api_client._is_onion_url("http://domain.com") is False
    assert api_client._is_onion_url("domain.com") is False
    assert api_client._is_onion_url("http://onion.domain.com/.onion/") is False
    assert api_client._is_onion_url("http://me.me/file.onion/") is False
    assert api_client._is_onion_url("http://me.me/file.onion") is False


@patch("sporestack.api_client._api_request")
def test_launch(mock_api_request: MagicMock) -> None:
    with pytest.raises(ValidationError):
        api_client.launch(
            "dummymachineid",
            days=1,
            operating_system="freebsd-12",
            ssh_key="id-rsa...",
            flavor="aflavor",
            token="f" * 64,
        )


@patch("sporestack.api_client._api_request")
def test_topup(mock_api_request: MagicMock) -> None:
    with pytest.raises(ValidationError):
        api_client.topup("dummymachineid", token="f" * 64, days=1)


@patch("sporestack.api_client._api_request")
def test_start(mock_api_request: MagicMock) -> None:
    api_client.start("dummymachineid")
    mock_api_request.assert_called_once_with(
        "https://api.sporestack.com/server/dummymachineid/start", empty_post=True
    )


@patch("sporestack.api_client._api_request")
def test_stop(mock_api_request: MagicMock) -> None:
    api_client.stop("dummymachineid")
    mock_api_request.assert_called_once_with(
        "https://api.sporestack.com/server/dummymachineid/stop", empty_post=True
    )


@patch("sporestack.api_client._api_request")
def test_rebuild(mock_api_request: MagicMock) -> None:
    api_client.rebuild("dummymachineid")
    mock_api_request.assert_called_once_with(
        "https://api.sporestack.com/server/dummymachineid/rebuild", empty_post=True
    )


@patch("sporestack.api_client._api_request")
def test_info(mock_api_request: MagicMock) -> None:
    with pytest.raises(ValidationError):
        api_client.info("dummymachineid")
    mock_api_request.assert_called_once_with(
        "https://api.sporestack.com/server/dummymachineid/info"
    )


@patch("sporestack.api_client._api_request")
def test_delete(mock_api_request: MagicMock) -> None:
    api_client.delete("dummymachineid")
    mock_api_request.assert_called_once_with(
        "https://api.sporestack.com/server/dummymachineid/destroy", empty_post=True
    )


@patch("sporestack.api_client._api_request")
def test_token_balance(mock_api_request: MagicMock) -> None:
    with pytest.raises(ValidationError):
        api_client.token_balance("dummytoken")
    mock_api_request.assert_called_once_with(
        url="https://api.sporestack.com/token/dummytoken/balance"
    )
