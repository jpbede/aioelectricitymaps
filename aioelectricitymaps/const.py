"""Constants for aioelectricitymaps."""
from enum import StrEnum

API_BASE_URL = "https://api.electricitymap.org/v3"


class ApiEndpoints:
    """Class holding API endpoints."""

    CARBON_INTENSITY_HA = API_BASE_URL + "/home-assistant"
    ZONES = API_BASE_URL + "/zones"
    LATEST_CARBON_INTENSITY = API_BASE_URL + "/carbon-intensity/latest"
    HISTORY_CARBON_INTENSITY = API_BASE_URL + "/carbon-intensity/history"
    LATEST_POWER_BREAKDOWN = API_BASE_URL + "/power-breakdown/latest"
    HISTORY_POWER_BREAKDOWN = API_BASE_URL + "/power-breakdown/history"


class Status(StrEnum):
    """Enum for status."""

    OK = "ok"
    NO_DATA = "no-data"
