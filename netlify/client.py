import dataclasses
from typing import Any, Iterable, Mapping, Sequence

import httpx

from netlify.auth.bearer import BearerAuth
from netlify.enums import ListSitesFilter, Period
from netlify.schemas import GenericResponse, Site, SiteFile, User


class NetlifyClient:
    base_url: str
    access_token: str
    user_agent: str
    timeout: float

    def __init__(
        self,
        access_token: str,
        base_url: str = "https://api.netlify.com/api/v1",
        user_agent: str = "NetlifyPythonClient/0.0.1",
        timeout: float = 60.000,
    ):
        self.access_token = access_token
        self.base_url = base_url
        self.user_agent = user_agent
        self.timeout = timeout

    ############
    # 0. OAuth #
    ############

    # Ticket

    def create_ticket(self, client_id: str):
        """
        POST /oauth/tickets

        Not implemented
        """
        raise NotImplementedError("PUT /oauth/tickets is not implemented.")

    def show_ticket(self, ticket_id: str):
        """
        GET /oauth/tickets/{ticket_id}

        Not implemented
        """
        raise NotImplementedError(f"GET /oauth/tickets/{ticket_id} is not implemented.")

    # Access token

    def exchange_ticket(self, ticket_id):
        """
        POST /oauth/tickets/{ticket_id}/exchange

        Not implemented
        """
        raise NotImplementedError(
            f"POST /oauth/tickets/{ticket_id}/exchange is not implemented."
        )

    ####################
    # I. User Accounts #
    ####################

    # User

    def get_current_user(self) -> User:
        """
        GET /user
        """
        return User.from_dict(self._send("GET", "/user"))

    # Accounts

    def cancel_account(self, account_id: str):
        """
        DELETE /accounts/{account_id}

        Not implemented
        """
        raise NotImplementedError(f"DELETE /accounts/{account_id} is not implemented.")

    def create_account(
        self,
        name: str,
        type_id: str,
        payment_method_id: str | None,
        period: Period | None,
        extra_seats_block: int | None,
    ):
        """
        POST /accounts

        Not implemented
        """
        raise NotImplementedError("POST /accounts is not implemented.")

    def get_account(self, account_id: str):
        """
        GET /accounts/{account_id}

        Not implemented
        """
        raise NotImplementedError(f"GET /accounts/{account_id} is not implemented.")

    def list_accounts_for_user(self):
        """
        GET /accounts

        Not implemented
        """
        raise NotImplementedError("GET /accounts is not implemented.")

    def update_account(self, account_id: str):
        """
        PUT /accounts/{account_id}

        Not implemented
        """
        raise NotImplementedError(f"PUT /accounts/{account_id} is not implemented.")

    # Member

    def add_member_to_account(self, account_slug: str):
        """
        POST /{account_slug}/members

        Not implemented
        """
        raise NotImplementedError(f"POST /{account_slug}/members is not implemented.")

    def list_members_for_account(self, account_slug: str):
        """
        GET /{account_slug}/members

        Not implemented
        """
        raise NotImplementedError(f" GET /{account_slug}/membersis not implemented.")

    # Access type

    def list_account_types_for_user(self):
        """
        GET /accounts/types

        Not implemented
        """
        raise NotImplementedError("GET /accounts/types is not implemented.")

    # Payment method

    def list_payment_methods_for_user(self):
        """
        GET /billing/payment_methods

        Not implemented
        """
        raise NotImplementedError("GET /billing/payment_methods is not implemented.")

    # Audit log

    def list_account_audit_events(self, account_id: str):
        """
        GET /accounts/{account_id}/audit

        Not implemented
        """
        raise NotImplementedError(
            f"GET /accounts/{account_id}/audit is not implemented."
        )

    ############
    # II. Site #
    ############

    # Site

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

    def unlink_site_repo(self, site_id: str):
        """
        PUT /sites/{site_id}/unlink_repo
        Not Implemented
        """
        raise NotImplementedError(
            f"PUT /sites/{site_id}/unlink_repo is a "
            "beta endpoint and is not implemented."
        )

    def update_site(self, site_id: str, site: Site) -> Site:
        """
        PATCH /sites/{site_id}
        """
        response = self._send(
            "PATCH", f"/sites/{site_id}", json=dataclasses.asdict(site)
        )
        return Site.from_dict(response)

    # Environment variables

    def create_env_vars(self, account_id: str):
        """
        POST /accounts/{account_id}/env
        Not Implemented
        """
        raise NotImplementedError(
            f"POST /accounts/{account_id}/env is not implemented."
        )

    def delete_env_var(self, account_id: str, key: str):
        """
        DELETE /accounts/{account_id}/env/{key}
        Not Implemented
        """
        raise NotImplementedError(
            f"DELETE /accounts/{account_id}/env/{key} is not implemented."
        )

    def delete_env_var_value(self, account_id: str, key: str, id: str):
        """
        DELETE /accounts/{account_id}/env/{key}/value/{id}
        Not Implemented
        """
        raise NotImplementedError(
            f"DELETE /accounts/{account_id}/env/{key}/value{id} is not implemented."
        )

    def get_env_var(self, account_id: str, key: str):
        """
        GET /accounts/{account_id}/env/{key}
        Not Implemented
        """
        raise NotImplementedError(
            f"GET /accounts/{account_id}/env/{key} is not implemented."
        )

    def get_env_vars(self, account_id: str):
        """
        GET /accounts/{account_id}/env
        Not Implemented
        """
        raise NotImplementedError(f"GET /accounts/{account_id}/env is not implemented.")

    def set_env_var_value(self, account_id: str, key: str):
        """
        PATCH /accounts/{account_id}/env/{key}
        Not Implemented
        """
        raise NotImplementedError(
            f"PATCH /accounts/{account_id}/env/{key} is not implemented."
        )

    def update_env_var(self, account_id: str, key: str):
        """
        PUT /accounts/{account_id}/env/{key}
        Not Implemented
        """
        raise NotImplementedError(
            f"PUT /accounts/{account_id}/env/{key} is not implemented."
        )

    # File

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

    def upload_deploy_file(self):
        pass

    # Metadata

    def get_site_metadata(self):
        raise NotImplementedError()

    def update_site_metadata(self):
        raise NotImplementedError()

    # Snippet

    def create_site_snippet(self):
        raise NotImplementedError()

    def delete_site_snippet(self):
        raise NotImplementedError()

    def get_site_snippet(self):
        raise NotImplementedError()

    def list_site_snippets(self):
        raise NotImplementedError()

    def update_site_snippet(self):
        raise NotImplementedError()

    #####################
    # III. Domain Names #
    #####################

    ###############
    # IV. Deploys #
    ###############

    #############
    # V. Builds #
    #############

    ##################################
    # VI. Webhooks and Notifications #
    ##################################

    #################
    # VII. Services #
    #################

    ###################
    # VIII. Functions #
    ###################

    #############
    # IX. Forms #
    #############

    ##################
    # X. Split Tests #
    ##################

    ###################
    # XI. Large Media #
    ###################

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
