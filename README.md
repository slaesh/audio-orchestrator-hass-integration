# Audio Orchestrator Home Assistant Integration

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/default)
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

### Via HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Click the three dots in the top right corner and choose **Custom repositories**.
3. Enter `https://github.com/slaesh/audio-orchestrator-hass-integration` as the URL and select **Integration** as category.
4. Click **Add**, find **Audio Orchestrator**, and click **Download**.
5. Restart Home Assistant.

### Manual Installation
1. Copy the `custom_components/audio_orchestrator` folder into your Home Assistant `/config/custom_components/` directory.
2. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for **Audio Orchestrator**.
3. Enter your Audio Orchestrator host URL (e.g. `http://192.168.178.157:5000` or `http://127.0.0.1:5000`).
4. Click **Submit**.

Your groups (e.g. `media_player.buro_sascha`) will appear automatically!

## License

MIT
