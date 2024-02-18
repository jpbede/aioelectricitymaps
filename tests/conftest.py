"""Fixtures for aioelectricitymaps tests."""
from collections.abc import AsyncGenerator, Generator
import re

import aiohttp
from aioresponses import aioresponses
import pytest

from aioelectricitymaps import ElectricityMaps

from . import load_fixture


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses


@pytest.fixture(name="mock_response")
def _mock_response(responses: aioresponses) -> None:
    """Mock an API response."""
    url_pattern = re.compile(
        r"^https://api\.electricitymap\.org/v3/home-assistant\?.*$",
    )
    responses.get(
        url_pattern,
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("response.json"),
    )


@pytest.fixture(name="mock_broken_response")
def _mock_broken_response(responses: aioresponses) -> None:
    """Mock a bad API response."""
    responses.get(
        "https://api.electricitymap.org/v3/home-assistant",
        status=200,
        headers={"Content-Type": "application/json"},
        body='{"status": "ok"',
    )


@pytest.fixture(name="electricitymaps_client")
async def client() -> AsyncGenerator[ElectricityMaps, None]:
    """Return a ElectricityMaps client."""
    async with aiohttp.ClientSession() as session, ElectricityMaps(
        token="abc123",
        session=session,
    ) as electricitymaps_client:
        yield electricitymaps_client
