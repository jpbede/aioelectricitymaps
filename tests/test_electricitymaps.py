"""Tests for the electricitymaps.com client."""

from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aioelectricitymaps import CoordinatesRequest, ElectricityMaps, ZoneRequest
from aioelectricitymaps.exceptions import (
    ElectricityMapsConnectionError,
    ElectricityMapsConnectionTimeoutError,
    ElectricityMapsError,
    ElectricityMapsInvalidTokenError,
    ElectricityMapsNoDataError,
)

from . import load_fixture


@pytest.mark.usefixtures("mock_response")
async def test_json_request_without_session(snapshot: SnapshotAssertion) -> None:
    """Test JSON response is handled correctly without given session."""
    async with ElectricityMaps(token="abc123") as em:
        assert (
            await em.carbon_intensity_for_home_assistant(ZoneRequest("DE")) == snapshot
        )
        assert em.session is not None

    assert em.session.closed


@pytest.mark.usefixtures("mock_response")
async def test_carbon_intensity_by_coordinates(
    electricitymaps_client: ElectricityMaps,
    snapshot: SnapshotAssertion,
) -> None:
    """Test carbon_intentsity_by_coordinates with given session."""
    assert (
        await electricitymaps_client.carbon_intensity_for_home_assistant(
            CoordinatesRequest(
                lat="53.1357012",
                lon="8.2024685",
            ),
        )
        == snapshot
    )


async def test_catching_client_error(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
) -> None:
    """Test JSON response is handled correctly with given session."""
    responses.get(
        "https://api.electricitymaps.com/v3/home-assistant?zone=DE",
        status=500,
        headers={"Content-Type": "application/json"},
        body="Boooom!",
    )
    with pytest.raises(ElectricityMapsConnectionError):
        await electricitymaps_client.carbon_intensity_for_home_assistant(
            ZoneRequest("DE"),
        )


async def test_zones_request(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test zones request."""
    responses.get(
        "https://api.electricitymaps.com/v3/zones",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("zones.json"),
    )
    assert await electricitymaps_client.zones() == snapshot


async def test_timeout(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
) -> None:
    """Test request timeout."""
    responses.add(
        "https://api.electricitymaps.com/v3/home-assistant?zone=DE",
        timeout=True,
    )
    with pytest.raises(ElectricityMapsConnectionTimeoutError):
        await electricitymaps_client.carbon_intensity_for_home_assistant(
            ZoneRequest("DE"),
        )


async def test_invalid_token(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
) -> None:
    """Test invalid token response."""
    responses.get(
        "https://api.electricitymaps.com/v3/home-assistant?zone=DE",
        status=401,
        headers={"Content-Type": "application/json"},
        body="",
    )
    with pytest.raises(ElectricityMapsInvalidTokenError):
        await electricitymaps_client.carbon_intensity_for_home_assistant(
            ZoneRequest("DE"),
        )


@pytest.mark.parametrize(
    ("filename", "expected_exception"),
    [
        ("no-data-response.json", ElectricityMapsNoDataError),
        ("unknown-response.json", ElectricityMapsError),
    ],
)
async def test_not_ok_responses(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    filename: str,
    expected_exception: type[Exception],
) -> None:
    """Test not-ok responses."""
    responses.get(
        "https://api.electricitymaps.com/v3/home-assistant?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture(filename),
    )
    with pytest.raises(expected_exception):
        await electricitymaps_client.carbon_intensity_for_home_assistant(
            ZoneRequest("DE"),
        )


async def test_latest_power_breakdown(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test latest_power_breakdown."""
    responses.get(
        "https://api.electricitymaps.com/v3/power-breakdown/latest?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("latest_power_breakdown.json"),
    )
    assert (
        await electricitymaps_client.latest_power_breakdown(
            ZoneRequest("DE"),
        )
        == snapshot
    )


async def test_power_breakdown_history(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test power_breakdown_history."""
    responses.get(
        "https://api.electricitymaps.com/v3/power-breakdown/history?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("power_breakdown_history.json"),
    )
    assert (
        await electricitymaps_client.power_breakdown_history(
            ZoneRequest("DE"),
        )
        == snapshot
    )


async def test_latest_carbon_intensity(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test latest_power_breakdown."""
    responses.get(
        "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("latest_carbon_intensity.json"),
    )
    assert (
        await electricitymaps_client.latest_carbon_intensity(
            ZoneRequest("DE"),
        )
        == snapshot
    )


async def test_carbon_intensity_history(
    electricitymaps_client: ElectricityMaps,
    responses: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test power_breakdown_history."""
    responses.get(
        "https://api.electricitymaps.com/v3/carbon-intensity/history?zone=DE",
        status=200,
        headers={"Content-Type": "application/json"},
        body=load_fixture("carbon_intensity_history.json"),
    )
    assert (
        await electricitymaps_client.carbon_intensity_history(
            ZoneRequest("DE"),
        )
        == snapshot
    )
