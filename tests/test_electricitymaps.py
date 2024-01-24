"""Tests for the electricitymaps.com client."""
from unittest.mock import patch

import aiohttp
from aresponses import ResponsesMockServer
import pytest
from syrupy.assertion import SnapshotAssertion

from aioelectricitymaps import ElectricityMaps
from aioelectricitymaps.exceptions import (
    ElectricityMapsDecodeError,
    ElectricityMapsError,
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


@pytest.mark.usefixtures("mock_broken_response")
async def test_broken_json_request() -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)

        with pytest.raises(ElectricityMapsDecodeError):
            await em.latest_carbon_intensity_by_country_code("DE")


async def test_catching_unknown_error() -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        with patch("aiohttp.ClientSession.get", side_effect=Exception):
            em = ElectricityMaps(token="abc123", session=session)

            with pytest.raises(ElectricityMapsError):
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
