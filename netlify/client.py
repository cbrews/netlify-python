from netlify.enums import ListSitesFilter
from netlify.schemas import CreateSiteRequest, Site, SiteDeploy, SiteFile, User
from netlify.transport import NetlifyTransport

CLIENT_USER_AGENT = "NetlifyPythonClient/0.2.0"


class NetlifyClient:
    _transport: NetlifyTransport

    def __init__(
        self,
        access_token: str,
        base_url: str = "https://api.netlify.com/api/v1",
        user_agent: str = CLIENT_USER_AGENT,
        timeout: float = 60.000,
    ):
        self._transport = NetlifyTransport(access_token, base_url, user_agent, timeout)

    def get_current_user(self) -> User:
        """
        GET /user
        """
        response = self._transport.send("GET", "/user")
        return User.parse_obj(response)

    def create_site(
        self,
        create_site_request: CreateSiteRequest,
        configure_dns: bool | None = None,
    ) -> Site:
        """
        POST /sites
        """
        response = self._transport.send(
            "POST",
            "/sites",
            params={"configure_dns": configure_dns},
            payload=create_site_request.dict(),
        )
        return Site.parse_obj(response)

    def create_site_in_team(
        self,
        account_slug: str,
        create_site_request: CreateSiteRequest,
        configure_dns: bool | None = None,
    ) -> Site:
        """
        POST /{account_slug}/sites
        """
        response = self._transport.send(
            "POST",
            f"/{account_slug}/sites",
            params={"configure_dns": configure_dns},
            payload=create_site_request.dict(),
        )
        return Site.parse_obj(response)

    def delete_site(self, site_id: str) -> None:
        """
        DELETE /sites/{site_id}
        """
        self._transport.send("DELETE", f"/sites/{site_id}")

    def get_site(self, site_id: str) -> Site:
        """
        GET /sites/{site_id}
        """
        return Site.parse_obj(self._transport.send("GET", f"/sites/{site_id}"))

    def list_sites(
        self,
        filter: ListSitesFilter | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> list[Site]:
        """
        GET /sites
        """
        response = self._transport.send(
            "GET",
            "/sites",
            params={"filter": filter, "page": page, "per_page": per_page},
        )
        return [Site.parse_obj(site) for site in response]

    def get_site_file_by_path_name(self, site_id: str, file_path: str) -> SiteFile:
        """
        GET /sites/{site_id}/files/{file_path}
        """
        response = self._transport.send("GET", f"/sites/{site_id}/files/{file_path}")
        return SiteFile.parse_obj(response)

    def list_site_files(self, site_id: str) -> list[SiteFile]:
        """
        GET /sites/{site_id}/files
        """
        response = self._transport.send("GET", f"/sites/{site_id}/files")
        return [SiteFile.parse_obj(site_file) for site_file in response]

    def create_site_deploy(
        self, site_id: str, zip_file_path: str, title: str | None = None
    ) -> SiteDeploy:
        """
        POST /sites/{site_id}/deploys
        """
        with open(zip_file_path, "rb") as fd:
            file_bytes = fd.read()

        response = self._transport.send(
            "POST",
            f"/sites/{site_id}/deploys",
            headers={"Content-Type": "application/zip"},
            params={"title": title},
            content=file_bytes,
        )
        return SiteDeploy.parse_obj(response)

    def get_site_deploy(self, site_id: str, deploy_id: str) -> SiteDeploy:
        """
        GET /sites/{site_id}/deploys/{deploy_id}
        """
        response = self._transport.send("GET", f"/sites/{site_id}/deploys/{deploy_id}")
        return SiteDeploy.parse_obj(response)
