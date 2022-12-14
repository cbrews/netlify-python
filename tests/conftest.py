import os
from typing import Generator

import pytest


def fixture_from_file(fixture_path: str) -> bytes:
    file_path = os.path.join(os.path.dirname(__file__), "fixtures", fixture_path)
    with open(file_path, "rb") as fd:
        return fd.read()


@pytest.fixture
def current_user_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("current_user_response.json")


@pytest.fixture
def site_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("site_response.json")


@pytest.fixture
def list_sites_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("list_sites_response.json")


@pytest.fixture
def list_site_files_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("list_site_files_response.json")


@pytest.fixture
def site_by_file_path_name_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("site_file_by_path_name_response.json")


@pytest.fixture
def site_deploy_response() -> Generator[bytes, None, None]:
    yield fixture_from_file("site_deploy_response.json")
