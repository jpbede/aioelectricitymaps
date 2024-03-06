"""Models for the electricitymaps.com carbon intensity API."""
from dataclasses import dataclass, field
from datetime import datetime

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass(slots=True, frozen=True, kw_only=True)
class CarbonIntensity:
    """API response."""

    carbon_intensity: int = field(metadata=field_options(alias="carbonIntensity"))
    timestamp: datetime = field(metadata=field_options(alias="datetime"))
    updated_at: datetime = field(metadata=field_options(alias="updatedAt"))
    emission_factor_type: str = field(
        metadata=field_options(alias="emissionFactorType"),
    )
    is_estimated: bool = field(metadata=field_options(alias="isEstimated"))
    estimation_method: str = field(metadata=field_options(alias="estimationMethod"))


@dataclass(slots=True, frozen=True, kw_only=True)
class LatestCarbonIntensity(CarbonIntensity, DataClassORJSONMixin):
    """Carbon intensity response."""

    zone: str


@dataclass(slots=True, frozen=True, kw_only=True)
class CarbonIntensityHistory(DataClassORJSONMixin):
    """Carbon intensity history response."""

    zone: str
    history: list[CarbonIntensity]
