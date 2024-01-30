"""Async Python client for electricitymaps.com."""
from __future__ import annotations

from dataclasses import dataclass
import json
import logging
from typing import Any, Self

from aiohttp import ClientSession

from .const import ApiEndpoints
from .exceptions import ElectricityMapsDecodeError, ElectricityMapsError, InvalidToken
from .models import CarbonIntensityResponse, Zone, ZonesResponse

_LOGGER = logging.getLogger(__name__)


@dataclass
class ElectricityMaps:
    """ElectricityMaps API client."""

    token: str
    session: ClientSession | None = None

    _close_session: bool = False
    _is_legacy_token: bool = False

    async def _get(self, url: str, params: dict[str, Any] | None = None) -> str:
        """Execute a GET request against the API."""
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        headers = {"auth-token": self.token}

        _LOGGER.debug("Doing request: GET %s %s", url, str(params))

        try:
            async with self.session.get(
                url,
                headers=headers,
                params=params,
            ) as response:
                parsed = await response.json()
        except json.JSONDecodeError as exception:
            msg = f"JSON decoding failed: {exception}"
            raise ElectricityMapsDecodeError(
                msg,
            ) from exception
        except Exception as exc:
            msg = f"Unknown error occurred while fetching data: {exc}"
            raise ElectricityMapsError(
                msg,
            ) from exc

        _LOGGER.debug(
            "Got response with status %s and body: %s",
            response.status,
            await response.text(),
        )

        # check for invalid token
        if (
            "message" in parsed
            and response.status == 404
            and (
                "No data product found" in parsed["message"]
                or "Invalid authentication" in parsed["message"]
            )
        ):
            raise InvalidToken

        return await response.text()

    async def latest_carbon_intensity_by_coordinates(
        self,
        lat: str,
        lon: str,
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by coordinates."""
        result = await self._get(
            ApiEndpoints.CARBON_INTENSITY,
            {"lat": lat, "lon": lon},
        )
        return CarbonIntensityResponse.from_json(result)

    async def latest_carbon_intensity_by_country_code(
        self,
        code: str,
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by country code."""
        result = await self._get(ApiEndpoints.CARBON_INTENSITY, {"zone": code})
        return CarbonIntensityResponse.from_json(result)

    async def zones(self) -> dict[str, Zone]:
        """Get a dict of zones where carbon intensity is available."""
        result = await self._get(ApiEndpoints.ZONES)
        return ZonesResponse.from_json(result).zones

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()
