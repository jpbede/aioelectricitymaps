"""Models to the electricitymaps.com API."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass(slots=True, frozen=True, kw_only=True)
class CarbonIntensityResponse(DataClassORJSONMixin):
    """API response."""

    status: str
    country_code: str = field(metadata=field_options(alias="countryCode"))
    data: CarbonIntensityData
    units: CarbonIntensityUnit


@dataclass(slots=True, frozen=True, kw_only=True)
class ZonesResponse(DataClassORJSONMixin):
    """Zones API response."""

    zones: dict[str, Zone]

    @classmethod
    def __pre_deserialize__(
        cls: type[Self],
        d: dict[Any, Any],
    ) -> dict[Any, Any]:
        """Wrap data in a dict for deserialization."""
        return {"zones": d}


@dataclass(slots=True, frozen=True, kw_only=True)
class CarbonIntensityData:
    """Data field."""

    carbon_intensity: float = field(metadata=field_options(alias="carbonIntensity"))
    fossil_fuel_percentage: float = field(
        metadata=field_options(alias="fossilFuelPercentage"),
    )


@dataclass(slots=True, frozen=True, kw_only=True)
class CarbonIntensityUnit:
    """Unit field."""

    carbon_intensity: str = field(metadata=field_options(alias="carbonIntensity"))


@dataclass(slots=True, frozen=True, kw_only=True)
class Zone:
    """Zone for carbon intensity API."""

    zone_name: str = field(metadata=field_options(alias="zoneName"))
    country_name: str | None = field(
        metadata=field_options(alias="countryName"),
        default=None,
    )
