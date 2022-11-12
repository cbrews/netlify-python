import dataclasses

from netlify.auth.bearer import BearerAuth


@dataclasses.dataclass
class MockRequest:
    headers: dict


def test_bearer_auth():
    bearer_auth = BearerAuth("test-token")
    request = MockRequest(headers={})

    # Run auth generator
    generator = bearer_auth.auth_flow(request)  # type: ignore[arg-type]
    result = generator.__next__()

    assert result.headers["Authorization"] == "Bearer test-token"
