"""Tests for the electricitymaps.com client."""
from unittest.mock import patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aioelectricitymaps import ElectricityMaps
from aioelectricitymaps.exceptions import (
    ElectricityMapsDecodeError,
    ElectricityMapsError,
)
from tests import load_fixture


@pytest.mark.asyncio
async def test_json_request_without_session(mock_response, snapshot) -> None:
    """Test JSON response is handled correctly without given session."""
    em = ElectricityMaps(token="abc123")
    assert await em.latest_carbon_intensity_by_country_code("DE") == snapshot


@pytest.mark.asyncio
async def test_json_request_with_session(mock_response, snapshot) -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert await em.latest_carbon_intensity_by_country_code("DE") == snapshot


@pytest.mark.asyncio
async def test_carbon_intensity_by_coordinates(mock_response, snapshot) -> None:
    """Test carbon_intentsity_by_coordinates with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert (
            await em.latest_carbon_intensity_by_coordinates(
                lat="53.1357012", lon="8.2024685"
            )
            == snapshot
        )


@pytest.mark.asyncio
async def test_broken_json_request(mock_broken_response) -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)

        with pytest.raises(ElectricityMapsDecodeError):
            await em.latest_carbon_intensity_by_country_code("DE")


@pytest.mark.asyncio
async def test_catching_unknown_error() -> None:
    """Test JSON response is handled correctly with given session."""
    async with aiohttp.ClientSession() as session:
        with patch("aiohttp.ClientSession.get", side_effect=Exception):
            em = ElectricityMaps(token="abc123", session=session)

            with pytest.raises(ElectricityMapsError):
                await em.latest_carbon_intensity_by_country_code("DE")


@pytest.mark.asyncio
async def test_zones_request(aresponses: ResponsesMockServer, snapshot) -> None:
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
