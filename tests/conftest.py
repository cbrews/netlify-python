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
