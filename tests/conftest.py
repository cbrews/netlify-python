import os
from collections.abc import Generator

import pytest


def fixture_from_file(fixture_path: str) -> bytes:
    file_path = os.path.join(os.path.dirname(__file__), "fixtures", fixture_path)
    with open(file_path, "rb") as fd:
        return fd.read()


@pytest.fixture
def json_fixture(request) -> Generator[bytes, None, None]:
    yield fixture_from_file(f"{request.param}.json")
