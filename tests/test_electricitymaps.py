"""Tests for the electricitymaps.com client."""
import aiohttp
from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aioelectricitymaps import ElectricityMaps
from aioelectricitymaps.exceptions import (
    ElectricityMapsConnectionError,
    ElectricityMapsConnectionTimeoutError,
    ElectricityMapsError,
    ElectricityMapsInvalidTokenError,
    ElectricityMapsNoDataError,
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


async def test_catching_client_error(responses: aioresponses) -> None:
    """Test JSON response is handled correctly with given session."""
    responses.get(
        "https://api.electricitymap.org/v3/home-assistant?zone=DE",
        status=500,
        headers={"Content-Type": "application/json"},
        body="Boooom!",
    )

    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)

        with pytest.raises(ElectricityMapsConnectionError):
            await em.latest_carbon_intensity_by_country_code("DE")


async def test_zones_request(
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test zones request."""
    responses.get(
        "https://api.electricitymap.org/v3/zones",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("zones.json"),
    )

    async with aiohttp.ClientSession() as session:
        em = ElectricityMaps(token="abc123", session=session)
        assert await em.zones() == snapshot


async def test_timeout(responses: aioresponses) -> None:
    """Test request timeout."""
    responses.add(
        "https://api.electricitymap.org/v3/home-assistant?zone=DE",
        timeout=True,
    )
    async with ElectricityMaps(token="abc123") as em:
        with pytest.raises(ElectricityMapsConnectionTimeoutError):
            await em.latest_carbon_intensity_by_country_code("DE")


async def test_invalid_token(responses: aioresponses) -> None:
    """Test invalid token response."""
    responses.get(
        "https://api.electricitymap.org/v3/home-assistant?zone=DE",
        status=401,
        headers={"Content-Type": "application/json"},
        body="",
    )
    async with ElectricityMaps(token="abc123") as em:
        with pytest.raises(ElectricityMapsInvalidTokenError):
            await em.latest_carbon_intensity_by_country_code("DE")


@pytest.mark.parametrize(
    ("filename", "expected_exception"),
    [
        ("no-data-response.json", ElectricityMapsNoDataError),
        ("unknown-response.json", ElectricityMapsError),
    ],
)
async def test_not_ok_responses(
    responses: aioresponses,
    filename: str,
    expected_exception: type[Exception],
) -> None:
    """Test not-ok responses."""
    responses.get(
        "https://api.electricitymap.org/v3/home-assistant?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture(filename),
    )
    async with ElectricityMaps(token="abc123") as em:
        with pytest.raises(expected_exception):
            await em.latest_carbon_intensity_by_country_code("DE")
