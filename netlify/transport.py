import logging
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

import httpx

from netlify.auth.bearer import BearerAuth
from netlify.exceptions import NetlifyError, NetlifyErrorSchema

logger = logging.getLogger(__name__)


class NetlifyTransport:
    _auth: BearerAuth
    _default_base_url: str
    _default_timeout: int | float
    _default_headers: dict[str, str]

    def __init__(
        self, access_token: str, base_url: str, user_agent: str, timeout: int | float
    ):
        self._auth = BearerAuth(access_token)
        self._default_base_url = base_url
        self._default_timeout = timeout
        self._default_headers = {"User-Agent": user_agent}

    def send(
        self,
        method: str,
        path: str,
        *,
        content: str | bytes | Iterable[bytes] | None = None,
        files: httpx._types.RequestFiles | None = None,
        payload: Any | None = None,
        params: Mapping[
            str,
            str | int | float | bool | Sequence[str | int | float | bool | None] | None,
        ]
        | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | float | None = None,
        base_url: str | None = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        with httpx.Client(
            base_url=self._build_base_url(base_url),
            auth=self._auth,
            headers=self._build_headers(headers),
            timeout=self._build_timeout(timeout),
        ) as httpx_client:
            try:
                if params is not None:
                    params = {
                        key: value
                        for (key, value) in params.items()
                        if value is not None
                    }

                response = httpx_client.request(
                    method,
                    path,
                    content=content,
                    data=None,
                    files=files,
                    json=payload,
                    auth=self._auth,
                    params=params,
                    cookies=None,
                    headers=None,
                    follow_redirects=False,
                    timeout=None,
                    extensions=None,
                    **kwargs,
                )

                logger.debug(f"Response from netlify: {response}")
                response.raise_for_status()

                if response.status_code == httpx.codes.NO_CONTENT:
                    return None

                return response.json()
            except httpx.HTTPStatusError as http_err:
                if "application/json" in response.headers.get("content-type", ""):
                    error = NetlifyErrorSchema.parse_obj(response.json())
                    raise NetlifyError(method, path, error) from http_err

                raise http_err

    def _build_headers(self, headers_input: dict[str, str] | None) -> dict[str, str]:
        if headers_input is None:
            return self._default_headers
        return {**self._default_headers, **headers_input}

    def _build_timeout(self, timeout_input: int | float | None) -> float:
        if timeout_input is None:
            return float(self._default_timeout)
        return float(timeout_input)

    def _build_base_url(self, base_url_input: str | None) -> str:
        if base_url_input is None:
            return self._default_base_url
        return base_url_input
