import json
from collections.abc import Generator
from typing import Any

import pytest
from httpx import HTTPStatusError
from pytest_httpx import HTTPXMock

from netlify.exceptions import NetlifyError
from netlify.transport import NetlifyTransport


@pytest.fixture
def transport() -> Generator[NetlifyTransport, None, None]:
    yield NetlifyTransport(
        "access-token", "https://api.netlify.com/api/v1", "test-user-agent", 1
    )


def test_transport_build_headers(transport: NetlifyTransport):
    assert transport._build_headers(None) == {"User-Agent": "test-user-agent"}
    assert transport._build_headers({"new-header": "abc"}) == {
        "User-Agent": "test-user-agent",
        "new-header": "abc",
    }
    assert transport._build_headers({"User-Agent": "override-user-agent"}) == {
        "User-Agent": "override-user-agent"
    }
    assert transport._build_headers(
        {"User-Agent": "override-user-agent", "new-header": "abc"}
    ) == {"User-Agent": "override-user-agent", "new-header": "abc"}


def test_transport_build_timeout(transport: NetlifyTransport):
    assert transport._build_timeout(None) == 1.0
    assert transport._build_timeout(2.0) == 2.0
    assert transport._build_timeout(0.0) == 0.0


def test_transport_build_base_url(transport: NetlifyTransport):
    assert transport._build_base_url(None) == "https://api.netlify.com/api/v1"
    assert (
        transport._build_base_url("https://test.netlify.com/")
        == "https://test.netlify.com/"
    )
    assert transport._build_base_url("") == ""


@pytest.mark.parametrize(
    "error_response",
    [
        {"code": 404, "message": "Not found"},
        {"code": 500, "errors": {"bad_response": "something"}},
        {"errors": {"fatal": True}},
    ],
)
def test_transport_json_error(
    httpx_mock: HTTPXMock, error_response: dict[str, Any], transport: NetlifyTransport
):
    httpx_mock.add_response(
        content=json.dumps(error_response).encode("utf-8"),
        status_code=404,
        headers={"content-type": "application/json"},
    )

    with pytest.raises(NetlifyError) as excinfo:
        transport.send("GET", "/bad_url")

    netlify_exception = excinfo.value

    assert netlify_exception.method == "GET"
    assert netlify_exception.path == "/bad_url"
    assert netlify_exception.code == error_response.get("code")
    assert netlify_exception.message == error_response.get("message")
    assert netlify_exception.errors == error_response.get("errors")


def test_transport_unhandled_error(httpx_mock: HTTPXMock, transport: NetlifyTransport):
    httpx_mock.add_response(
        content=b"garbage response",
        status_code=500,
    )

    with pytest.raises(HTTPStatusError):
        transport.send("GET", "/bad_url")
