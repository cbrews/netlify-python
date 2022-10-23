import datetime
from dataclasses import dataclass
from typing import Any

from netlify.util.extended_dataclass import ExtendedDataclass as EDC


@dataclass
class User(EDC):
    id: str
    uid: str | None
    full_name: str | None
    avatar_url: str | None
    email: str
    affiliate_id: str | None
    site_count: int
    created_at: datetime.datetime
    last_login: datetime.datetime | None
    login_providers: list[str]
    onboarding_process: dict[str, str]


@dataclass
class SiteCapabilities(EDC):
    large_media_enabled: bool


@dataclass
class FunctionSchedules(EDC):
    name: str
    cron: str


@dataclass
class SiteDeploy(EDC):
    id: str
    site_id: str
    user_id: str
    build_id: str | None
    state: str
    name: str
    url: str
    ssl_url: str
    admin_url: str
    deploy_url: str
    deploy_ssl_url: str
    screenshot_url: str | None
    review_id: float | None
    draft: bool
    required: list[str]
    required_functions: list[str]
    error_message: str | None
    branch: str | None
    commit_ref: str | None
    commit_url: str | None
    skipped: bool | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    published_at: datetime.datetime | None
    title: str | None
    context: str
    locked: bool | None
    review_url: str | None
    site_capabilities: SiteCapabilities
    framework: str | None
    function_schedules: list


@dataclass
class DefaultHooksData(EDC):
    access_token: str


@dataclass
class SiteRepoInfo(EDC):
    id: int
    provider: str
    deploy_key_id: str | None
    repo_path: str
    dir: str | None
    functions_dir: str | None
    cmd: str | None
    allowed_branches: list[str]
    public_repo: bool
    private_logs: bool | None
    repo_url: str
    env: dict[str, str]
    installation_id: int | None
    stop_builds: bool


@dataclass
class MinifyOptions(EDC):
    bundle: bool
    minify: bool


@dataclass
class SiteProcessingSettingsImages(EDC):
    optimize: bool


@dataclass
class SiteProcessingSettingsHtml(EDC):
    pretty_urls: bool


@dataclass
class SiteProcessingSettings(EDC):
    skip: bool
    css: MinifyOptions
    js: MinifyOptions
    images: SiteProcessingSettingsImages
    html: SiteProcessingSettingsHtml


@dataclass
class Site(EDC):
    id: str
    state: str
    plan: str
    name: str
    custom_domain: str | None
    domain_aliases: list[str]
    password: str | None
    notification_email: str | None
    url: str
    ssl_url: str
    admin_url: str
    screenshot_url: str | None
    created_at: str
    updated_at: datetime.datetime
    user_id: str
    session_id: str | None
    ssl: bool
    force_ssl: bool | None
    managed_dns: bool
    deploy_url: str
    published_deploy: SiteDeploy
    account_name: str
    account_slug: str
    git_provider: str | None
    deploy_hook: str | None
    capabilities: dict[str, Any]
    processing_settings: SiteProcessingSettings
    build_settings: SiteRepoInfo
    id_domain: str
    default_hooks_data: DefaultHooksData | None
    build_image: str
    prerender: str | None
