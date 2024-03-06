"""Request model for electricitymaps API."""
from dataclasses import asdict, dataclass


@dataclass
class BaseRequest:
    """Base request model."""

    def get_request_parameters(self) -> dict[str, str]:
        """Get request parameters."""
        return asdict(self)

    def __str__(self) -> str:
        """Return string representation of the request."""
        return str(asdict(self))


@dataclass
class ZoneRequest(BaseRequest):
    """Zone request model."""

    zone: str


@dataclass(kw_only=True)
class CoordinatesRequest(BaseRequest):
    """Coordinates request model."""

    lat: str
    lon: str
