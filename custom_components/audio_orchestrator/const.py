"""Constants for the Audio Orchestrator integration."""
from datetime import timedelta

DOMAIN = "audio_orchestrator"
DEFAULT_HOST = "http://127.0.0.1:5000"
CONF_HOST = "host"

SCAN_INTERVAL = timedelta(seconds=3)
STREAM_ID_DEFAULT = "default"
