from collections.abc import Generator

import httpx


class BearerAuth(httpx.Auth):
    bearer_token: str

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.bearer_token}"
        yield request
