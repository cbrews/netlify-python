# pylint: disable=redefined-outer-name
import json
from typing import Generator

import pytest
from httpx import HTTPStatusError

from netlify import __version__
from netlify.client import NetlifyClient
from netlify.exceptions import NetlifyException


@pytest.fixture
def client() -> Generator[NetlifyClient, None, None]:
    yield NetlifyClient("test_access_token")


def test_default_client_user_agent_version_matches(client: NetlifyClient):
    assert f"NetlifyPythonClient/{__version__}" == client.user_agent


def test_client_json_error(httpx_mock, client: NetlifyClient):
    httpx_mock.add_response(
        content=json.dumps({"code": 404, "message": "Not found"}),
        status_code=404,
        headers={"content-type": "application/json"},
    )

    with pytest.raises(NetlifyException) as excinfo:
        client._send("GET", "/bad_url")  # pylint: disable=protected-access

    netlify_exception = excinfo.value

    assert netlify_exception.method == "GET"
    assert netlify_exception.path == "/bad_url"
    assert netlify_exception.code == 404
    assert netlify_exception.message == "Not found"


def test_client_unhandled_error(httpx_mock, client: NetlifyClient):
    httpx_mock.add_response(
        content=b"garbage response",
        status_code=500,
    )

    with pytest.raises(HTTPStatusError):
        client._send("GET", "/bad_url")  # pylint: disable=protected-access


def test_get_current_user(
    httpx_mock, current_user_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=current_user_response)

    result = client.get_current_user()

    assert result.id == "1234567890abcdef"
    assert result.full_name == "Marty McFly"
    assert result.email == "example@example.com"


def test_delete_site(httpx_mock, client: NetlifyClient):
    httpx_mock.add_response(content=b"", status_code=204)

    client.delete_site("11111111-1111-1111-1111-111111111111")


def test_get_site(httpx_mock, site_response: bytes, client: NetlifyClient):
    httpx_mock.add_response(content=site_response)

    result = client.get_site("11111111-1111-1111-1111-111111111111")

    assert result.id == "11111111-1111-1111-1111-111111111111"
    assert result.url == "https://mcfly-site.netlify.app"
    assert result.account_name == "Marty McFly's team"


def test_list_sites(httpx_mock, list_sites_response: bytes, client: NetlifyClient):
    httpx_mock.add_response(content=list_sites_response)

    result = client.list_sites()

    assert len(result) == 1
    assert result[0].id == "11111111-1111-1111-1111-111111111111"
    assert result[0].url == "https://mcfly-site.netlify.app"
    assert result[0].account_name == "Marty McFly's team"


def test_get_site_file_by_path_name(
    httpx_mock, site_by_file_path_name_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=site_by_file_path_name_response)

    result = client.get_site_file_by_path_name(
        "11111111-1111-1111-1111-111111111111", "index.html"
    )

    assert result.id == "/index.html"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"
    assert result.sha == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def test_list_site_files(
    httpx_mock, list_site_files_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=list_site_files_response)

    result = client.list_site_files("11111111-1111-1111-1111-111111111111")

    assert len(result) == 2
    assert result[0].id == "/index.html"
    assert result[0].site_id == "11111111-1111-1111-1111-111111111111"
    assert result[0].sha == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert result[1].id == "/other.html"
    assert result[1].site_id == "11111111-1111-1111-1111-111111111111"
    assert result[1].sha == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def test_create_site_deploy__file_exists(
    httpx_mock, site_deploy_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=site_deploy_response)

    result = client.create_site_deploy(
        "11111111-1111-1111-1111-111111111111", "./tests/fixtures/test_site.zip"
    )

    assert result.id == "abcdef0123456789"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"


def test_create_site_deploy__file_not_exists(client: NetlifyClient):
    with pytest.raises(FileNotFoundError) as excinfo:
        client.create_site_deploy(
            "11111111-1111-1111-1111-111111111111", "./tests/fixtures/non-extant.zip"
        )

    assert "No such file or directory" in str(excinfo.value)
    assert "tests/fixtures/non-extant.zip" in str(excinfo.value)


def test_get_site_deploy(
    httpx_mock, site_deploy_response: bytes, client: NetlifyClient
):
    httpx_mock.add_response(content=site_deploy_response)

    result = client.get_site_deploy(
        "11111111-1111-1111-1111-111111111111", "abcdef0123456789"
    )

    assert result.id == "abcdef0123456789"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"
