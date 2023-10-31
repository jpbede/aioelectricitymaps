import pytest
from aresponses import ResponsesMockServer

from . import load_fixture


@pytest.fixture
def mock_response(aresponses: ResponsesMockServer) -> None:
    aresponses.add(
        "api-access.electricitymaps.com",
        "/free-tier/home-assistant",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("response.json"),
        ),
    )


@pytest.fixture
def mock_broken_response(aresponses: ResponsesMockServer) -> None:
    aresponses.add(
        "api-access.electricitymaps.com",
        "/free-tier/home-assistant",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"',
        ),
    )
