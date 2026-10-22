"""DataUpdateCoordinator for Audio Orchestrator."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AudioOrchestratorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Audio Orchestrator state from API."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.host = host.rstrip("/")
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch full state from the orchestrator API."""
        url = f"{self.host}/api/fullstate"
        try:
            async with self.session.get(url, timeout=5) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Unexpected status code {response.status} from {url}")
                return await response.json()
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Audio Orchestrator at {url}: {err}") from err
