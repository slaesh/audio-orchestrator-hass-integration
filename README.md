# Audio Orchestrator Home Assistant Integration

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/default)
[![Validate](https://github.com/slaesh/audio-orchestrator-hass-integration/actions/workflows/validate.yml/badge.svg)](https://github.com/slaesh/audio-orchestrator-hass-integration/actions/workflows/validate.yml)
[![CI](https://github.com/slaesh/audio-orchestrator-hass-integration/actions/workflows/ci.yml/badge.svg)](https://github.com/slaesh/audio-orchestrator-hass-integration/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Home Assistant Custom Integration for **[Audio Orchestrator](https://github.com/slaesh/audio-orchestrator)**.

Exposes every Audio Orchestrator group as a native Home Assistant `media_player` entity.

## Features

- 🔊 **Group Master Volume & Mute**: Smooth bi-directional volume control mapped to each group.
- 📻 **Dynamic Source Selection**: Instantly switch between Radio streams (Audalaxy / Sunshine Live, etc.) and Spotify Connect nodes.
- 🎶 **Live Metadata & Cover Art**: Displays track title, artist, album, and live artwork from active streams.
- ⏯️ **Playback Control**: Play, pause, next, and previous track controls for Spotify sources.
- ⚡ **Automations & Voice Assistants**: Control multi-room audio through Home Assistant automations, scenes, Apple HomeKit, Google Assistant, or Alexa.

## Installation

### Via HACS / Home Assistant Marketplace (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=slaesh&repository=audio-orchestrator-hass-integration&category=integration)

1. Click the button above to open the repository directly in HACS.
2. Alternatively:
   - In Home Assistant, open **HACS** > Integrations.
   - Click the three dots in the top right corner and choose **Custom repositories**.
   - Enter `https://github.com/slaesh/audio-orchestrator-hass-integration` as the URL and select **Integration** as category.
   - Click **Add**, find **Audio Orchestrator**, and click **Download**.
3. Restart Home Assistant if prompted.

### Manual Installation

1. Copy the `custom_components/audio_orchestrator` folder into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.

## Configuration

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=audio_orchestrator)

1. Click the button above or navigate in Home Assistant to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for **Audio Orchestrator**.
3. Enter your Audio Orchestrator host URL (e.g. `http://192.168.178.157:5000` or `http://127.0.0.1:5000`).
4. Click **Submit**.

Your groups (e.g. `media_player.buro_sascha`) will appear automatically!

## License

MIT
