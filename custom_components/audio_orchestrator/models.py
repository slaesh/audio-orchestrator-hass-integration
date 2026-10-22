"""Typed models for Audio Orchestrator corresponding to AudioOrchestrator.json OpenAPI spec."""
from __future__ import annotations

from typing import TypedDict


class RoomDto(TypedDict, total=False):
    """Room details."""
    id: str
    name: str
    friendlyName: str | None
    hostName: str | None
    connected: bool
    volumePercent: int
    volumeMuted: bool
    mixVolume: int


class GroupDto(TypedDict, total=False):
    """Group details from AudioOrchestrator."""
    id: str
    name: str
    streamId: str | None
    rooms: list[RoomDto]
    masterVolume: int
    isMuted: bool


class StreamDto(TypedDict, total=False):
    """Radio/Snapcast stream details."""
    id: str
    name: str
    status: str
    url: str | None
    currentTitle: str | None
    currentArtist: str | None
    currentCoverUrl: str | None
    errorMessage: str | None
    currentVersion: str | None
    latestCompatibleVersion: str | None
    hasUpdate: bool
    pluginId: str | None
    containerRunning: bool


class SpotifySourceDto(TypedDict, total=False):
    """Spotify source details."""
    id: str
    name: str
    isActive: bool
    isConnected: bool
    status: str
    masterVolume: int
    maxVolume: int
    currentTrackId: str | None
    currentTitle: str | None
    currentArtist: str | None
    currentAlbum: str | None
    currentDurationMs: int | None
    currentCoverUrl: str | None
    currentPositionMs: int | None
    heartbeatIntervalMs: int | None
    lastUpdateTimestamp: int | None
    errorMessage: str | None


class FullStateDto(TypedDict, total=False):
    """Root full state response from /api/fullstate."""
    groups: list[GroupDto]
    radioStreams: list[StreamDto]
    spotifySources: list[SpotifySourceDto]
    snapcastStreams: list[StreamDto]
    volumeProfile: str
