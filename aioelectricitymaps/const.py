"""Constants for aioelectricitymaps."""
API_BASE_URL = "https://api.electricitymap.org/v3"


class ApiEndpoints:
    """Class holding API endpoints."""

    CARBON_INTENSITY = API_BASE_URL + "/home-assistant"
    ZONES = API_BASE_URL + "/zones"
