"""Tests for the electricitymaps.com client."""
import asyncio

import aiohttp
from aiohttp import ClientResponse
from aresponses import ResponsesMockServer
import pytest
from syrupy.assertion import SnapshotAssertion

from aioelectricitymaps import ElectricityMaps
from aioelectricitymaps.exceptions import (
    ElectricityMapsConnectionError,
    ElectricityMapsConnectionTimeoutError,
    ElectricityMapsInvalidTokenError,
)

from . import load_fixture


@pytest.mark.usefixtures("mock_response")
async def test_asyncio_protocol() -> None:
    """Test the asyncio protocol implementation."""
    async with ElectricityMaps(token="abc123") as em:
        assert await em.latest_carbon_intensity_by_country_code("DE")


@pytest.mark.usefixtures("mock_response")
async def test_json_request_without_session(snapshot: SnapshotAssertion) -> None:
    """Test JSON response is handled correctly without given session."""
    em = ElectricityMaps(token="abc123")
    assert await em.latest_carbon_intensity_by_country_code("DE") == snapshot


@pytest.mark.usefixtures("mock_response")
async def test_json_request_with_session(snapshot: SnapshotAssertion) -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert await em.latest_carbon_intensity_by_country_code("DE") == snapshot


@pytest.mark.usefixtures("mock_response")
async def test_carbon_intensity_by_coordinates(snapshot: SnapshotAssertion) -> None:
    """Test carbon_intentsity_by_coordinates with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert (
            await em.latest_carbon_intensity_by_coordinates(
                lat="53.1357012",
                lon="8.2024685",
            )
            == snapshot
        )


async def test_catching_client_error(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly with given session."""
    aresponses.add(
        "api.electricitymap.org",
        "/v3/home-assistant",
        "GET",
        aresponses.Response(
            status=500,
            headers={"Content-Type": "application/json"},
            text="Boooom!",
        ),
    )

    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)

        with pytest.raises(ElectricityMapsConnectionError):
            await em.latest_carbon_intensity_by_country_code("DE")


async def test_zones_request(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
) -> None:
    """Test zones request."""
    aresponses.add(
        "api.electricitymap.org",
        "/v3/zones",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixture("zones.json"),
        ),
    )

    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert await em.zones() == snapshot


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> aresponses.Response:
        """Response handler for this test."""
        await asyncio.sleep(8)
        return aresponses.Response(
            status=200,
            text=load_fixture("response.json"),
        )

    aresponses.add(
        "api.electricitymap.org",
        "/v3/home-assistant",
        "GET",
        response_handler,
    )
    async with ElectricityMaps(token="abc123", request_timeout=1) as em:
        with pytest.raises(ElectricityMapsConnectionTimeoutError):
            await em.latest_carbon_intensity_by_country_code("DE")


async def test_invalid_token(aresponses: ResponsesMockServer) -> None:
    """Test invalid token response."""
    aresponses.add(
        "api.electricitymap.org",
        "/v3/home-assistant",
        "GET",
        aresponses.Response(
            status=403,
            headers={"Content-Type": "application/json"},
            text="",
        ),
    )
    async with ElectricityMaps(token="abc123", request_timeout=1) as em:
        with pytest.raises(ElectricityMapsInvalidTokenError):
            await em.latest_carbon_intensity_by_country_code("DE")
