import datetime
from typing import Any

from pydantic import BaseModel


class User(BaseModel):
    id: str
    uid: str | None = None
    full_name: str | None = None
    avatar_url: str | None = None
    email: str
    affiliate_id: str | None = None
    site_count: int
    created_at: datetime.datetime
    last_login: datetime.datetime | None = None
    login_providers: list[str]
    onboarding_process: dict[str, str] | None = None


class SiteFile(BaseModel):
    id: str
    path: str
    sha: str
    mime_type: str
    size: int
    site_id: str | None = None
    deploy_id: str | None = None


class FunctionSchedules(BaseModel):
    name: str
    cron: str


class SiteDeploy(BaseModel):
    id: str
    site_id: str
    user_id: str
    build_id: str | None = None
    state: str
    name: str
    url: str
    ssl_url: str
    admin_url: str
    deploy_url: str
    deploy_ssl_url: str
    screenshot_url: str | None = None
    review_id: float | None = None
    draft: bool | None = None
    required: list[str]
    required_functions: list[str] | None = None
    error_message: str | None = None
    branch: str | None = None
    commit_ref: str | None = None
    commit_url: str | None = None
    skipped: bool | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None
    published_at: datetime.datetime | None = None
    title: str | None = None
    context: str
    locked: bool | None = None
    review_url: str | None = None
    framework: str | None = None
    function_schedules: list[FunctionSchedules]


class GenericResponse(BaseModel):
    code: int
    message: str


class DefaultHooksData(BaseModel):
    access_token: str


class SiteRepoInfo(BaseModel):
    id: int | None = None
    provider: str | None = None
    deploy_key_id: str | None = None
    repo_path: str | None = None
    repo_branch: str | None = None
    dir: str | None = None
    functions_dir: str | None = None
    cmd: str | None = None
    allowed_branches: list[str] | None = None
    public_repo: bool | None = None
    private_logs: bool | None = None
    repo_url: str | None = None
    env: dict[str, str] | None = None
    installation_id: int | None = None
    stop_builds: bool | None = None


class SiteProcessingSettingsHtml(BaseModel):
    pretty_urls: bool


class SiteProcessingSettings(BaseModel):
    html: SiteProcessingSettingsHtml | None = None


class Site(BaseModel):
    id: str
    state: str
    plan: str
    name: str
    custom_domain: str | None = None
    domain_aliases: list[str]
    branch_deploy_custom_domain: str | None = None
    deploy_preview_custom_domain: str | None = None
    password: str | None = None
    notification_email: str | None = None
    url: str
    ssl_url: str
    admin_url: str
    screenshot_url: str | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: str
    session_id: str | None = None
    ssl: bool
    force_ssl: bool | None = None
    managed_dns: bool
    deploy_url: str
    published_deploy: SiteDeploy | None
    account_id: str | None = None
    account_name: str
    account_slug: str
    git_provider: str | None = None
    deploy_hook: str | None = None
    capabilities: dict[str, Any] | None = None
    processing_settings: SiteProcessingSettings | None = None
    build_settings: SiteRepoInfo | None = None
    id_domain: str
    default_hooks_data: DefaultHooksData | None = None
    build_image: str
    prerender: str | None = None
    functions_region: str | None = None
    prevent_non_git_prod_deploys: bool | None = None


class CreateSiteRequest(BaseModel):
    state: str | None = None
    plan: str | None = None
    name: str | None = None
    custom_domain: str | None = None
    domain_aliases: list[str] | None = None
    branch_deploy_custom_domain: str | None = None
    deploy_preview_custom_domain: str | None = None
    password: str | None = None
    notification_email: str | None = None
    url: str | None = None
    ssl_url: str | None = None
    admin_url: str | None = None
    screenshot_url: str | None = None
    deploy_url: str | None = None
    account_id: str | None = None
    account_name: str | None = None
    account_slug: str | None = None
    force_ssl: bool | None = None
    processing_settings: SiteProcessingSettings | None = None
    repo: SiteRepoInfo | None = None
