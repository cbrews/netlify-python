import httpx

from netlify.auth.bearer import BearerAuth


def test_bearer_auth() -> None:
    bearer_auth = BearerAuth("test-token")

    request = httpx.Request("GET", "https://example.com")
    # Run auth generator
    result = next(bearer_auth.auth_flow(request))
    assert result.headers["Authorization"] == "Bearer test-token"
