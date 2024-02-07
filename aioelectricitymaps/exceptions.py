"""Exceptions for ElectricityMaps."""


class ElectricityMapsError(Exception):
    """Generic error occurred in ElectricityMaps package."""


class ElectricityMapsNoDataError(ElectricityMapsError):
    """There is no data available for the given location."""


class ElectricityMapsConnectionError(ElectricityMapsError):
    """Error occurred while communicating to the Electricity Maps API."""


class ElectricityMapsConnectionTimeoutError(ElectricityMapsError):
    """Timeout occurred while connecting to the Electricity Maps API."""


class ElectricityMapsInvalidTokenError(ElectricityMapsError):
    """Given token is invalid."""
