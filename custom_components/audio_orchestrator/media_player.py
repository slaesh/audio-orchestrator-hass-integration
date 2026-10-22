"""Media Player platform for Audio Orchestrator groups."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, STREAM_ID_DEFAULT
from .coordinator import AudioOrchestratorCoordinator

_LOGGER = logging.getLogger(__name__)

OFF_SOURCE_LABEL = "Aus (Stille)"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Audio Orchestrator media player entities from config entry."""
    coordinator: AudioOrchestratorCoordinator = hass.data[DOMAIN][entry.entry_id]
    known_groups: set[str] = set()

    def update_entities() -> None:
        if not coordinator.data:
            return
        groups = coordinator.data.get("groups")
        if not groups:
            return

        new_entities: list[AudioOrchestratorGroupPlayer] = []
        for group in groups:
            group_id = group.get("id")
            if not group_id or group_id in known_groups:
                continue

            known_groups.add(group_id)
            new_entities.append(AudioOrchestratorGroupPlayer(coordinator, group_id))

        if not new_entities:
            return

        async_add_entities(new_entities)

    update_entities()
    coordinator.async_add_listener(update_entities)


class AudioOrchestratorGroupPlayer(CoordinatorEntity[AudioOrchestratorCoordinator], MediaPlayerEntity):
    """Representation of an Audio Orchestrator group as a Media Player entity."""

    _attr_device_class = MediaPlayerDeviceClass.SPEAKER
    _attr_has_entity_name = True

    def __init__(self, coordinator: AudioOrchestratorCoordinator, group_id: str) -> None:
        """Initialize the media player."""
        super().__init__(coordinator)
        self._group_id = group_id
        self._attr_unique_id = f"audio_orchestrator_group_{group_id}"

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported dynamically based on active stream."""
        features = (
            MediaPlayerEntityFeature.VOLUME_SET
            | MediaPlayerEntityFeature.VOLUME_MUTE
            | MediaPlayerEntityFeature.SELECT_SOURCE
        )

        data = self.group_data
        if not data:
            return features

        stream_id = data.get("streamId", "")
        if stream_id.startswith("spotify_"):
            return (
                features
                | MediaPlayerEntityFeature.PLAY
                | MediaPlayerEntityFeature.PAUSE
                | MediaPlayerEntityFeature.NEXT_TRACK
                | MediaPlayerEntityFeature.PREVIOUS_TRACK
            )

        # For Radio (or Idle): No play/pause/skip buttons, rely on Mute & Source selection
        return features

    @property
    def group_data(self) -> dict[str, Any] | None:
        """Get the current group data dictionary."""
        if not self.coordinator.data:
            return None

        for group in self.coordinator.data.get("groups", []):
            if group.get("id") == self._group_id:
                return group

        return None

    @property
    def name(self) -> str:
        """Return the friendly name of the group."""
        data = self.group_data
        if not data:
            return "Audio Gruppe"
        return data.get("name") or "Audio Gruppe"

    @property
    def state(self) -> MediaPlayerState:
        """Return current playback state."""
        data = self.group_data
        if not data:
            return MediaPlayerState.OFF

        stream_id = data.get("streamId")
        if not stream_id or stream_id == STREAM_ID_DEFAULT:
            return MediaPlayerState.IDLE

        source_info = self._get_active_source_info(stream_id)
        if not source_info:
            return MediaPlayerState.IDLE

        status = source_info.get("status")
        if status == "playing":
            return MediaPlayerState.PLAYING

        return MediaPlayerState.PAUSED

    @property
    def volume_level(self) -> float | None:
        """Return volume level from 0.0 to 1.0."""
        data = self.group_data
        if not data:
            return None
        volume = data.get("masterVolume")
        if volume is None:
            return None
        return max(0.0, min(1.0, volume / 100.0))

    @property
    def is_volume_muted(self) -> bool | None:
        """Return whether group is muted."""
        data = self.group_data
        if not data:
            return None
        return data.get("isMuted", False)

    @property
    def source_list(self) -> list[str]:
        """Return selectable sources (Radios & Spotify Nodes)."""
        if not self.coordinator.data:
            return [OFF_SOURCE_LABEL]

        sources = [OFF_SOURCE_LABEL]

        for radio in self.coordinator.data.get("radioStreams", []):
            name = radio.get("name")
            if name:
                sources.append(f"Radio: {name}")

        for spot in self.coordinator.data.get("spotifySources", []):
            name = spot.get("name")
            if name:
                sources.append(f"Spotify: {name}")

        return sources

    @property
    def source(self) -> str | None:
        """Return currently playing source name."""
        data = self.group_data
        if not data:
            return None

        stream_id = data.get("streamId")
        if not stream_id or stream_id == STREAM_ID_DEFAULT:
            return OFF_SOURCE_LABEL

        for radio in self.coordinator.data.get("radioStreams", []):
            if radio.get("id") == stream_id:
                return f"Radio: {radio.get('name')}"

        for spot in self.coordinator.data.get("spotifySources", []):
            spot_id = spot.get("id")
            if stream_id in (spot_id, f"spotify_{spot_id}"):
                return f"Spotify: {spot.get('name')}"

        return stream_id

    @property
    def media_title(self) -> str | None:
        """Return track or stream title."""
        info = self._get_active_source_info()
        if not info:
            return None
        return info.get("currentTitle")

    @property
    def media_artist(self) -> str | None:
        """Return track or stream artist."""
        info = self._get_active_source_info()
        if not info:
            return None
        return info.get("currentArtist")

    @property
    def media_album_name(self) -> str | None:
        """Return track album."""
        info = self._get_active_source_info()
        if not info:
            return None
        return info.get("currentAlbum")

    @property
    def entity_picture(self) -> str | None:
        """Return cover artwork URL."""
        info = self._get_active_source_info()
        if not info:
            return None
        return info.get("currentCoverUrl")

    def _get_active_source_info(self, stream_id: str | None = None) -> dict[str, Any] | None:
        """Resolve metadata dictionary of the active stream."""
        data = self.group_data
        if not data or not self.coordinator.data:
            return None

        target_id = stream_id or data.get("streamId")
        if not target_id or target_id == STREAM_ID_DEFAULT:
            return None

        for radio in self.coordinator.data.get("radioStreams", []):
            if radio.get("id") == target_id:
                return radio

        for spot in self.coordinator.data.get("spotifySources", []):
            spot_id = spot.get("id")
            if target_id in (spot_id, f"spotify_{spot_id}"):
                return spot

        return None

    # --- Commands ---

    async def async_set_volume_level(self, volume: float) -> None:
        """Set group master volume (0-100)."""
        val = int(volume * 100)
        url = f"{self.coordinator.host}/api/externalcontrol/groups/{self._group_id}/volume"
        async with self.coordinator.session.put(url, json={"value": val}) as resp:
            if resp.status != 200:
                _LOGGER.warning("Failed to set volume: HTTP %s", resp.status)
                return

        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        """Toggle group mute."""
        url = f"{self.coordinator.host}/api/externalcontrol/groups/{self._group_id}/mute"
        async with self.coordinator.session.put(url, json={"value": mute}) as resp:
            if resp.status != 200:
                _LOGGER.warning("Failed to set mute: HTTP %s", resp.status)
                return

        await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str) -> None:
        """Switch audio source/stream for this group."""
        stream_id = STREAM_ID_DEFAULT if source == OFF_SOURCE_LABEL else self._resolve_source_name_to_id(source)
        if not stream_id:
            return

        url = f"{self.coordinator.host}/api/groups/{self._group_id}/stream"
        async with self.coordinator.session.put(url, json={"streamId": stream_id}) as resp:
            if resp.status != 200:
                _LOGGER.warning("Failed to set stream: HTTP %s", resp.status)
                return

        await self.coordinator.async_request_refresh()

    def _resolve_source_name_to_id(self, source_name: str) -> str | None:
        """Helper to find streamId from selected display name."""
        if not self.coordinator.data:
            return None

        clean_name = source_name.replace("Radio: ", "").replace("Spotify: ", "")

        for radio in self.coordinator.data.get("radioStreams", []):
            if radio.get("name") == clean_name:
                return radio.get("id")

        for spot in self.coordinator.data.get("spotifySources", []):
            if spot.get("name") == clean_name:
                spot_id = spot.get("id")
                return f"spotify_{spot_id}" if spot_id else None

        return None

    async def async_media_pause(self) -> None:
        """Pause playback on active stream."""
        source_id = self._get_active_spotify_source_id()
        if source_id:
            url = f"{self.coordinator.host}/api/spotifysources/{source_id}/pause"
            async with self.coordinator.session.post(url):
                pass
            await self.coordinator.async_request_refresh()
            return

        # Radio stream: Pause switches stream to default silence
        await self.async_media_stop()

    async def async_media_stop(self) -> None:
        """Stop playback (switch back to default silence)."""
        url = f"{self.coordinator.host}/api/groups/{self._group_id}/stream"
        async with self.coordinator.session.put(url, json={"streamId": STREAM_ID_DEFAULT}) as resp:
            if resp.status != 200:
                _LOGGER.warning("Failed to stop stream: HTTP %s", resp.status)
                return

        await self.coordinator.async_request_refresh()

    async def async_media_play(self) -> None:
        """Resume playback on active Spotify node."""
        source_id = self._get_active_spotify_source_id()
        if not source_id:
            return

        url = f"{self.coordinator.host}/api/spotifysources/{source_id}/resume"
        async with self.coordinator.session.post(url):
            pass

        await self.coordinator.async_request_refresh()

    async def async_media_next_track(self) -> None:
        """Skip to next track on active Spotify node."""
        source_id = self._get_active_spotify_source_id()
        if not source_id:
            return

        url = f"{self.coordinator.host}/api/spotifysources/{source_id}/next"
        async with self.coordinator.session.post(url):
            pass

        await self.coordinator.async_request_refresh()

    async def async_media_previous_track(self) -> None:
        """Skip to previous track on active Spotify node."""
        source_id = self._get_active_spotify_source_id()
        if not source_id:
            return

        url = f"{self.coordinator.host}/api/spotifysources/{source_id}/previous"
        async with self.coordinator.session.post(url):
            pass

        await self.coordinator.async_request_refresh()

    def _get_active_spotify_source_id(self) -> str | None:
        """Return plain Spotify source ID if active."""
        data = self.group_data
        if not data:
            return None

        sid = data.get("streamId", "")
        if not sid.startswith("spotify_"):
            return None

        return sid.replace("spotify_", "")
