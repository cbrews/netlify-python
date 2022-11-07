# pylint: disable=redefined-outer-name
from typing import Generator

import pytest

from netlify import __version__
from netlify.client import NetlifyClient


@pytest.fixture
def client() -> Generator[NetlifyClient, None, None]:
    yield NetlifyClient("test_access_token")


def test_default_client_user_agent_version_matches(client: NetlifyClient):
    assert f"NetlifyPythonClient/{__version__}" == client.user_agent


def test_client_get_current_user(
    httpx_mock, current_user_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=current_user_response)

    result = client.get_current_user()

    assert result.id == "1234567890abcdef"
    assert result.full_name == "Marty McFly"
    assert result.email == "example@example.com"


def test_client_get_site(httpx_mock, site_response: bytes, client: NetlifyClient):
    httpx_mock.add_response(content=site_response)

    result = client.get_site("11111111-1111-1111-1111-111111111111")

    assert result.id == "11111111-1111-1111-1111-111111111111"
    assert result.url == "https://mcfly-site.netlify.app"
    assert result.account_name == "Marty McFly's team"
