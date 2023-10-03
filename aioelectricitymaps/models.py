"""Models to the electricitymaps.com API."""
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, LetterCase, config


@dataclass(slots=True, frozen=True)
class CarbonIntensityData(DataClassJsonMixin):
    """Data field."""

    carbon_intensity: float = field(metadata=config(letter_case=LetterCase.CAMEL))
    fossil_fuel_percentage: float = field(metadata=config(letter_case=LetterCase.CAMEL))


@dataclass(slots=True, frozen=True)
class CarbonIntensityUnit(DataClassJsonMixin):
    """Unit field."""

    carbon_intensity: str = field(metadata=config(letter_case=LetterCase.CAMEL))


@dataclass(slots=True, frozen=True)
class CarbonIntensityResponse(DataClassJsonMixin):
    """API response."""

    status: str = field(metadata=config(letter_case=LetterCase.CAMEL))
    country_code: str = field(metadata=config(letter_case=LetterCase.CAMEL))
    data: CarbonIntensityData
    units: CarbonIntensityUnit


@dataclass(slots=True, frozen=True)
class Zone(DataClassJsonMixin):
    """Zone for carbon intensity API."""

    zone_name: str = field(metadata=config(letter_case=LetterCase.CAMEL))
    country_name: str | None = field(
        metadata=config(letter_case=LetterCase.CAMEL), default=None
    )
