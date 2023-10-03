"""Async Python client for electricitymaps.com."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from .const import ApiEndpoints
from .exceptions import ElectricityMapsDecodeError, ElectricityMapsError
from .marshmallow import ZoneList
from .models import CarbonIntensityResponse, Zone


@dataclass
class ElectricityMaps:
    token: str
    session: ClientSession | None = None

    _close_session: bool = False

    async def _get(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Execute a GET request against the API."""

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        headers = {"auth-token": self.token}

        try:
            async with self.session.get(
                url, headers=headers, params=params
            ) as response:
                response.raise_for_status()
                return await response.json()
        except json.JSONDecodeError as exception:
            raise ElectricityMapsDecodeError(
                f"JSON decoding failed: {exception}"
            ) from exception
        except Exception as exc:
            raise ElectricityMapsError(
                f"Unknown error occurred while fetching data: {exc}"
            ) from exc

    async def latest_carbon_intensity_by_coordinates(
        self, lat: str, lon: str
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by coordinates."""
        result = await self._get(
            ApiEndpoints.CARBON_INTENSITY, {"lat": lat, "lon": lon}
        )
        return CarbonIntensityResponse.from_dict(result)

    async def latest_carbon_intensity_by_country_code(
        self, code: str
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by country code."""
        result = await self._get(ApiEndpoints.CARBON_INTENSITY, {"countryCode": code})
        return CarbonIntensityResponse.from_dict(result)

    async def zones(self) -> dict[str, Zone]:
        """Get list of zones where carbon intensity is available."""
        result = await self._get(ApiEndpoints.ZONES)
        return ZoneList.from_dict({"zones": result}).zones

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> ElectricityMaps:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()
