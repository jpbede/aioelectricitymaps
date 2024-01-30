"""Fixtures for aioelectricitymaps tests."""
from aresponses import ResponsesMockServer
import pytest

from . import load_fixture


@pytest.fixture(name="mock_response")
def _mock_response(aresponses: ResponsesMockServer) -> None:
    """Mock an API response."""
    aresponses.add(
        "api.electricitymap.org",
        "/v3/home-assistant",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("response.json"),
        ),
    )


@pytest.fixture(name="mock_broken_response")
def _mock_broken_response(aresponses: ResponsesMockServer) -> None:
    """Mock a bad API response."""
    aresponses.add(
        "api.electricitymap.org",
        "/v3/home-assistant",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"',
        ),
    )
