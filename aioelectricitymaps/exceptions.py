"""Exceptions for ElectricityMaps."""


class ElectricityMapsError(Exception):
    """Generic error occurred in ElectricityMaps package."""


class SwitchedToLegacyAPI(ElectricityMapsError):
    """Error raised when API switched to legacy.

    Caught by retry_legacy decorator.
    """


class InvalidToken(ElectricityMapsError):
    """Given token is invalid."""


class ElectricityMapsDecodeError(ElectricityMapsError):
    """Decoding error occurred in ElectricityMaps package."""
