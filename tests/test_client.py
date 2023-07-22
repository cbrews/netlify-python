from collections.abc import Generator

import pytest
from pytest_httpx import HTTPXMock

from netlify import __version__
from netlify.client import CLIENT_USER_AGENT, NetlifyClient
from netlify.schemas import (
    CreateSiteRequest,
)


def test_default_client_user_agent_version_matches():
    assert f"NetlifyPythonClient/{__version__}" == CLIENT_USER_AGENT


@pytest.fixture
def client() -> Generator[NetlifyClient, None, None]:
    yield NetlifyClient("access-token")


@pytest.fixture
def set_mock_response(httpx_mock: HTTPXMock):
    def set_mock_response(content: bytes = b"", status_code: int = 200) -> None:
        httpx_mock.add_response(status_code=status_code, content=content)

    return set_mock_response


@pytest.mark.parametrize("json_fixture", ["current_user_response"], indirect=True)
def test_get_current_user(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.get_current_user()

    assert result.id == "1234567890abcdef"
    assert result.full_name == "Marty McFly"
    assert result.email == "example@example.com"


@pytest.mark.parametrize("json_fixture", ["site_response"], indirect=True)
def test_create_site(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture, status_code=201)

    result = client.create_site(CreateSiteRequest(name="test-site-name"))

    # Using mocked site_response
    assert result.id == "11111111-1111-1111-1111-111111111111"


@pytest.mark.parametrize("json_fixture", ["site_response"], indirect=True)
def test_create_site_in_team(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture, status_code=201)

    result = client.create_site_in_team(
        "my-account",
        CreateSiteRequest(name="test-site-name"),
    )

    # Using mocked site_response
    assert result.id == "11111111-1111-1111-1111-111111111111"


def test_delete_site(
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(status_code=204)

    client.delete_site("11111111-1111-1111-1111-111111111111")


@pytest.mark.parametrize("json_fixture", ["site_response"], indirect=True)
def test_get_site(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.get_site("11111111-1111-1111-1111-111111111111")

    assert result.id == "11111111-1111-1111-1111-111111111111"
    assert result.url == "https://mcfly-site.netlify.app"
    assert result.account_name == "Marty McFly's team"


@pytest.mark.parametrize("json_fixture", ["list_sites_response"], indirect=True)
def test_list_sites(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.list_sites()

    assert len(result) == 1
    assert result[0].id == "11111111-1111-1111-1111-111111111111"
    assert result[0].url == "https://mcfly-site.netlify.app"
    assert result[0].account_name == "Marty McFly's team"


@pytest.mark.parametrize(
    "json_fixture", ["site_file_by_path_name_response"], indirect=True
)
def test_get_site_file_by_path_name(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.get_site_file_by_path_name(
        "11111111-1111-1111-1111-111111111111", "index.html"
    )

    assert result.id == "/index.html"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"
    assert result.sha == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@pytest.mark.parametrize("json_fixture", ["list_site_files_response"], indirect=True)
def test_list_site_files(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.list_site_files("11111111-1111-1111-1111-111111111111")

    assert len(result) == 2
    assert result[0].id == "/index.html"
    assert result[0].site_id == "11111111-1111-1111-1111-111111111111"
    assert result[0].sha == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert result[1].id == "/other.html"
    assert result[1].site_id == "11111111-1111-1111-1111-111111111111"
    assert result[1].sha == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


@pytest.mark.parametrize("json_fixture", ["site_deploy_response"], indirect=True)
def test_create_site_deploy__file_exists(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.create_site_deploy(
        "11111111-1111-1111-1111-111111111111", "./tests/fixtures/test_site.zip"
    )

    assert result.id == "abcdef0123456789"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"


def test_create_site_deploy__file_not_exists(
    client: NetlifyClient,
):
    with pytest.raises(FileNotFoundError) as excinfo:
        client.create_site_deploy(
            "11111111-1111-1111-1111-111111111111", "./tests/fixtures/non-extant.zip"
        )

    assert "No such file or directory" in str(excinfo.value)
    assert "tests/fixtures/non-extant.zip" in str(excinfo.value)


@pytest.mark.parametrize("json_fixture", ["site_deploy_response"], indirect=True)
def test_get_site_deploy(
    json_fixture: bytes,
    client: NetlifyClient,
    set_mock_response,  # type: ignore
):
    set_mock_response(json_fixture)

    result = client.get_site_deploy(
        "11111111-1111-1111-1111-111111111111", "abcdef0123456789"
    )

    assert result.id == "abcdef0123456789"
    assert result.site_id == "11111111-1111-1111-1111-111111111111"
