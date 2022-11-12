import dataclasses
from typing import Any, Iterable, Mapping, Sequence

import httpx

from netlify.auth.bearer import BearerAuth
from netlify.enums import ListSitesFilter
from netlify.schemas import GenericResponse, Site, SiteDeploy, SiteFile, User


class NetlifyClient:
    base_url: str
    access_token: str
    user_agent: str
    timeout: float

    def __init__(
        self,
        access_token: str,
        base_url: str = "https://api.netlify.com/api/v1",
        user_agent: str = "NetlifyPythonClient/0.0.2",
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

    def create_site(self, site: Site, configure_dns: bool | None) -> Site:
        """
        POST /sites
        """
        response = self._send(
            "POST",
            "/sites",
            params={"configure_dns": configure_dns},
            json=dataclasses.asdict(site),
        )
        return Site.from_dict(response)

    def create_site_in_team(
        self, account_slug: str, site: Site, configure_dns: bool | None
    ) -> Site:
        """
        POST /{account_slug}/sites
        """
        response = self._send(
            "POST",
            f"/{account_slug}/sites",
            params={"configure_dns": configure_dns},
            json=dataclasses.asdict(site),
        )
        return Site.from_dict(response)

    def delete_site(self, site_id: str) -> GenericResponse:
        """
        DELETE /sites/{site_id}
        """
        response = self._send("DELETE", f"/sites/{site_id}")
        return GenericResponse.from_dict(response)

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

    def list_sites_for_account(
        self,
        account_slug: str,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[Site]:
        """
        GET /{account_slug}/sites
        """
        response = self._send(
            "GET",
            f"/{account_slug}/sites",
            params={"name": name, "page": page, "per_page": per_page},
        )
        return [Site.from_dict(site) for site in response]

    def update_site(self, site_id: str, site: Site) -> Site:
        """
        PATCH /sites/{site_id}
        """
        response = self._send(
            "PATCH", f"/sites/{site_id}", json=dataclasses.asdict(site)
        )
        return Site.from_dict(response)

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
    ) -> Any:
        """
        POST /sites/{site_id}/deploys
        """
        with open(zip_file_path, "rb") as fd:
            file_bytes = fd.read()

        response = self._send(
            "GET",
            f"/sites/{site_id}/deploys",
            headers={"Content-Type": "application/zip"},
            params={"title": title},
            content=file_bytes,
        )
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

            return response.json()  # probably needs to be smarter

    def _default_headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent}
