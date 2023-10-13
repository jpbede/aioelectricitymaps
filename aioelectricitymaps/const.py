API_BASE_URL = "https://api-access.electricitymaps.com/free-tier/"

LEGACY_API_BASE_URL = "https://api.co2signal.com/v1/"


class ApiEndpoints:
    LEGACY_CARBON_INTENSITY = LEGACY_API_BASE_URL + "latest"
    CARBON_INTENSITY = API_BASE_URL + "home-assistant"
    ZONES = "https://api.electricitymap.org/v3/zones"
