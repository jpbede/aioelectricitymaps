"""Models to the electricitymaps.com API."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin

from aioelectricitymaps.const import Status
from aioelectricitymaps.exceptions import (
    ElectricityMapsError,
    ElectricityMapsNoDataError,
)


@dataclass(slots=True, frozen=True, kw_only=True)
class HomeAssistantCarbonIntensityResponse(DataClassORJSONMixin):
    """API response."""

    status: str
    country_code: str = field(metadata=field_options(alias="countryCode"))
    data: HomeAssistantCarbonIntensityData
    units: HomeAssistantCarbonIntensityUnit

    @classmethod
    def __pre_deserialize__(
        cls: type[Self],
        d: dict[Any, Any],
    ) -> dict[Any, Any]:
        """Check if the status is ok otherwise raise an error."""
        status = d.get("status")
        if status == Status.OK:
            return d

        if status == Status.NO_DATA:
            msg = "No data available for selected location"
            raise ElectricityMapsNoDataError(msg)

        msg = f"Unknown response status occurred: {status}"
        raise ElectricityMapsError(msg)


@dataclass(slots=True, frozen=True, kw_only=True)
class HomeAssistantCarbonIntensityData:
    """Data field."""

    carbon_intensity: float = field(metadata=field_options(alias="carbonIntensity"))
    fossil_fuel_percentage: float = field(
        metadata=field_options(alias="fossilFuelPercentage"),
    )


@dataclass(slots=True, frozen=True, kw_only=True)
class HomeAssistantCarbonIntensityUnit:
    """Unit field."""

    carbon_intensity: str = field(metadata=field_options(alias="carbonIntensity"))
