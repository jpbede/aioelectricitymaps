"""Models to the electricitymaps.com API."""
from typing import TypedDict


class CarbonIntensityData(TypedDict):
    """Data field."""

    carbonIntensity: float
    fossilFuelPercentage: float


class CarbonIntensityUnit(TypedDict):
    """Unit field."""

    carbonIntensity: str


class CarbonIntensityResponse(TypedDict):
    """API response."""

    status: str
    countryCode: str
    data: CarbonIntensityData
    units: CarbonIntensityUnit
