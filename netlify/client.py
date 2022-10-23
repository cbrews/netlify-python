from typing import Any, Iterable, Mapping, Sequence

import httpx

from netlify.auth.bearer import BearerAuth
from netlify.enums import ListSitesFilter
from netlify.exceptions import NetlifyError, NetlifyException
from netlify.schemas import Site, SiteDeploy, SiteFile, User


class NetlifyClient:
    base_url: str
    access_token: str
    user_agent: str
    timeout: float

    def __init__(
        self,
        access_token: str,
        base_url: str = "https://api.netlify.com/api/v1",
        user_agent: str = "NetlifyPythonClient/0.1.0",
        timeout: float = 60.000,
    ):
        self.access_token = access_token
        self.base_url = base_url
        self.user_agent = user_agent
        self.timeout = timeout

    def get_current_user(self) -> User:
        """
        GET /user
        """
        return User.from_dict(self._send("GET", "/user"))

    def delete_site(self, site_id: str) -> None:
        """
        DELETE /sites/{site_id}
        """
        return self._send("DELETE", f"/sites/{site_id}")

    def get_site(self, site_id: str) -> Site:
        """
        GET /sites/{site_id}
        """
        return Site.from_dict(self._send("GET", f"/sites/{site_id}"))

    def list_sites(
        self,
        filter: ListSitesFilter | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[Site]:
        """
        GET /sites
        """
        response = self._send(
            "GET",
            "/sites",
            params={"filter": filter, "page": page, "per_page": per_page},
        )
        return [Site.from_dict(site) for site in response]

    def get_site_file_by_path_name(self, site_id: str, file_path: str) -> SiteFile:
        """
        GET /sites/{site_id}/files/{file_path}
        """
        response = self._send("GET", f"/sites/{site_id}/files/{file_path}")
        return SiteFile.from_dict(response)

    def list_site_files(self, site_id: str) -> list[SiteFile]:
        """
        GET /sites/{site_id}/files
        """
        response = self._send("GET", f"/sites/{site_id}/files")
        return [SiteFile.from_dict(site_file) for site_file in response]

    def create_site_deploy(
        self, site_id: str, zip_file_path: str, title: str | None = None
    ) -> SiteDeploy:
        """
        POST /sites/{site_id}/deploys
        """
        with open(zip_file_path, "rb") as fd:
            file_bytes = fd.read()

        response = self._send(
            "POST",
            f"/sites/{site_id}/deploys",
            headers={"Content-Type": "application/zip"},
            params={"title": title},
            content=file_bytes,
        )
        return SiteDeploy.from_dict(response)

    def get_site_deploy(self, site_id: str, deploy_id: str) -> SiteDeploy:
        """
        GET /sites/{site_id}/deploys/{deploy_id}
        """
        response = self._send("GET", f"/sites/{site_id}/deploys/{deploy_id}")
        return SiteDeploy.from_dict(response)

    def _send(
        self,
        method: str,
        path: str,
        *,
        content: str | bytes | Iterable[bytes] | None = None,
        data: dict | None = None,
        files: httpx._types.RequestFiles | None = None,
        json: Any | None = None,
        params: Mapping[
            str,
            str | int | float | bool | Sequence[str | int | float | bool | None] | None,
        ]
        | None = None,
        headers: dict[str, str] | None = None,
        timeout: float | None = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        prepared_headers = self._default_headers()
        prepared_headers.update(headers or {})

        with httpx.Client(
            base_url=self.base_url,
            auth=BearerAuth(self.access_token),
            headers=prepared_headers,
            timeout=timeout or self.timeout,
        ) as client:
            try:
                response = client.request(
                    method,
                    path,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    auth=BearerAuth(self.access_token),
                    params=params,
                    cookies=None,
                    headers=None,
                    follow_redirects=False,
                    timeout=None,
                    extensions=None,
                    **kwargs,
                )
                response.raise_for_status()

                if response.status_code == httpx.codes.NO_CONTENT:
                    return None

                return response.json()
            except httpx.HTTPStatusError as http_err:
                if "application/json" in response.headers.get("content-type", ""):
                    error = NetlifyError.from_dict(response.json())
                    raise NetlifyException(method, path, error) from http_err

                raise http_err

    def _default_headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent}
