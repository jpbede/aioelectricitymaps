"""Power breakdown response models for the electricitymaps.com API."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime  # noqa: TCH003

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass(slots=True, frozen=True, kw_only=True)
class PowerBreakdown:
    """API response."""

    time: datetime = field(metadata=field_options(alias="datetime"))
    updated_at: datetime = field(metadata=field_options(alias="updatedAt"))
    created_at: datetime = field(metadata=field_options(alias="createdAt"))
    power_consumption_breakdown: dict[str, int | None] = field(
        metadata=field_options(alias="powerConsumptionBreakdown"),
    )
    power_production_breakdown: dict[str, int | None] = field(
        metadata=field_options(alias="powerProductionBreakdown"),
    )
    power_import_breakdown: dict[str, int | None] = field(
        metadata=field_options(alias="powerImportBreakdown"),
    )
    power_export_breakdown: dict[str, int | None] = field(
        metadata=field_options(alias="powerExportBreakdown"),
    )
    fossil_free_percentage: int = field(
        metadata=field_options(alias="fossilFreePercentage"),
    )
    renewable_percentage: int = field(
        metadata=field_options(alias="renewablePercentage"),
    )
    power_consumption_total: int = field(
        metadata=field_options(alias="powerConsumptionTotal"),
    )
    power_production_total: int = field(
        metadata=field_options(alias="powerProductionTotal"),
    )
    power_import_total: int = field(metadata=field_options(alias="powerImportTotal"))
    power_export_total: int = field(metadata=field_options(alias="powerExportTotal"))
    is_estimated: bool = field(metadata=field_options(alias="isEstimated"))
    estimation_method: str = field(metadata=field_options(alias="estimationMethod"))


@dataclass(slots=True, frozen=True, kw_only=True)
class LatestPowerBreakdown(PowerBreakdown, DataClassORJSONMixin):
    """Power breakdown response."""

    zone: str


@dataclass(slots=True, frozen=True, kw_only=True)
class PowerBreakdownHistory(DataClassORJSONMixin):
    """Power breakdown response."""

    zone: str
    history: list[PowerBreakdown]
