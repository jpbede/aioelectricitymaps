"""Async Python client for electricitymaps.com."""
from __future__ import annotations

from dataclasses import dataclass
import logging
import socket
from typing import TYPE_CHECKING, Self

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import ApiEndpoints
from .exceptions import (
    ElectricityMapsConnectionError,
    ElectricityMapsConnectionTimeoutError,
    ElectricityMapsInvalidTokenError,
)
from .models import (
    CarbonIntensityHistory,
    HomeAssistantCarbonIntensityResponse,
    LatestCarbonIntensity,
    LatestPowerBreakdown,
    PowerBreakdownHistory,
    Zone,
    ZonesResponse,
)

if TYPE_CHECKING:
    from .request import BaseRequest, CoordinatesRequest, ZoneRequest

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
        request: BaseRequest | None = None,
        unauthenticated: bool = False,
    ) -> str:
        """Execute a GET request against the API."""
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        headers = {} if unauthenticated else {"auth-token": self.token}

        _LOGGER.debug("Doing request: GET %s %s", url, str(request))

        params = {}
        if request:
            params = request.get_request_parameters()

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

    async def carbon_intensity_for_home_assistant(
        self,
        request: CoordinatesRequest | ZoneRequest,
    ) -> HomeAssistantCarbonIntensityResponse:
        """Get carbon intensity."""
        result = await self._get(
            url=ApiEndpoints.CARBON_INTENSITY_HA,
            request=request,
        )
        return HomeAssistantCarbonIntensityResponse.from_json(result)

    async def latest_carbon_intensity(
        self,
        request: CoordinatesRequest | ZoneRequest,
    ) -> LatestCarbonIntensity:
        """Get latest carbon intensity."""
        result = await self._get(
            url=ApiEndpoints.LATEST_CARBON_INTENSITY,
            request=request,
        )
        return LatestCarbonIntensity.from_json(result)

    async def carbon_intensity_history(
        self,
        request: CoordinatesRequest | ZoneRequest,
    ) -> CarbonIntensityHistory:
        """Get carbon intensity history."""
        result = await self._get(
            url=ApiEndpoints.HISTORY_CARBON_INTENSITY,
            request=request,
        )
        return CarbonIntensityHistory.from_json(result)

    async def latest_power_breakdown(
        self,
        request: CoordinatesRequest | ZoneRequest,
    ) -> LatestPowerBreakdown:
        """Get latest power breakdown."""
        result = await self._get(
            url=ApiEndpoints.LATEST_POWER_BREAKDOWN,
            request=request,
        )
        return LatestPowerBreakdown.from_json(result)

    async def power_breakdown_history(
        self,
        request: CoordinatesRequest | ZoneRequest,
    ) -> PowerBreakdownHistory:
        """Get power breakdown history."""
        result = await self._get(
            url=ApiEndpoints.HISTORY_POWER_BREAKDOWN,
            request=request,
        )
        return PowerBreakdownHistory.from_json(result)

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
