"""Async Python client for electricitymaps.com."""
from __future__ import annotations

from dataclasses import dataclass
import logging
import socket
from typing import Any, Self

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import ApiEndpoints
from .exceptions import (
    ElectricityMapsConnectionError,
    ElectricityMapsConnectionTimeoutError,
    ElectricityMapsInvalidTokenError,
)
from .models import CarbonIntensityResponse, Zone, ZonesResponse

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class ElectricityMaps:
    """ElectricityMaps API client."""

    token: str
    session: ClientSession | None = None

    _close_session: bool = False

    async def _get(
        self,
        *,
        url: str,
        params: dict[str, Any] | None = None,
        unauthenticated: bool = False,
    ) -> str:
        """Execute a GET request against the API."""
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        headers = {} if unauthenticated else {"auth-token": self.token}

        _LOGGER.debug("Doing request: GET %s %s", url, str(params))

        try:
            async with self.session.get(
                url,
                headers=headers,
                params=params,
            ) as response:
                response.raise_for_status()
                response_text = await response.text()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Electricity Maps API"
            raise ElectricityMapsConnectionTimeoutError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            if isinstance(exception, ClientResponseError) and exception.status == 401:
                msg = "The given token is invalid"
                raise ElectricityMapsInvalidTokenError(msg) from exception

            msg = "Error occurred while communicating to the Electricity Maps API"
            raise ElectricityMapsConnectionError(msg) from exception

        _LOGGER.debug(
            "Got response with status %s and body: %s",
            response.status,
            response_text,
        )

        return response_text

    async def latest_carbon_intensity_by_coordinates(
        self,
        lat: str,
        lon: str,
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by coordinates."""
        result = await self._get(
            url=ApiEndpoints.CARBON_INTENSITY,
            params={"lat": lat, "lon": lon},
        )
        return CarbonIntensityResponse.from_json(result)

    async def latest_carbon_intensity_by_country_code(
        self,
        code: str,
    ) -> CarbonIntensityResponse:
        """Get carbon intensity by country code."""
        result = await self._get(
            url=ApiEndpoints.CARBON_INTENSITY,
            params={"zone": code.upper()},
        )
        return CarbonIntensityResponse.from_json(result)

    async def zones(self) -> dict[str, Zone]:
        """Get a dict of zones where carbon intensity is available."""
        result = await self._get(url=ApiEndpoints.ZONES, unauthenticated=True)
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
