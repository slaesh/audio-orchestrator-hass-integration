"""Config flow for Audio Orchestrator integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_HOST, DEFAULT_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)


class AudioOrchestratorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Audio Orchestrator."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self._show_user_form()

        host = user_input[CONF_HOST].rstrip("/")
        session = async_get_clientsession(self.hass)

        try:
            async with session.get(f"{host}/api/fullstate", timeout=5) as resp:
                if resp.status != 200:
                    return self._show_user_form({"base": "cannot_connect"})
        except (ClientError, TimeoutError):
            return self._show_user_form({"base": "cannot_connect"})

        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title="Audio Orchestrator",
            data={CONF_HOST: host},
        )

    def _show_user_form(self, errors: dict[str, str] | None = None) -> FlowResult:
        """Helper to render configuration form."""
        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors or {},
        )
