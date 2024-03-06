"""Models for the electricitymaps.com zone API."""
from dataclasses import dataclass, field
from typing import Any, Self

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass(slots=True, frozen=True, kw_only=True)
class Zone:
    """Zone for carbon intensity API."""

    zone_name: str = field(metadata=field_options(alias="zoneName"))
    country_name: str | None = field(
        metadata=field_options(alias="countryName"),
        default=None,
    )


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
