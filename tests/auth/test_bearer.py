from pydantic import BaseModel

from netlify.auth.bearer import BearerAuth


class MockRequest(BaseModel):
    headers: dict


def test_bearer_auth():
    bearer_auth = BearerAuth("test-token")
    # Run auth generator
    generator = bearer_auth.auth_flow(MockRequest(headers={}))  # type: ignore[arg-type]
    result = generator.__next__()

    assert result.headers["Authorization"] == "Bearer test-token"
