"""Exceptions for ElectricityMaps."""


class ElectricityMapsError(Exception):
    """Generic error occurred in ElectricityMaps package."""


class InvalidToken(ElectricityMapsError):
    """Given token is invalid."""


class ElectricityMapsDecodeError(ElectricityMapsError):
    """Decoding error occurred in ElectricityMaps package."""
