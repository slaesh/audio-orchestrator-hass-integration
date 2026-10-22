#!/usr/bin/env bash
set -euo pipefail

SPEC_FILE="AudioOrchestrator.json"
LOCAL_PATH="../audio-orchestrator/apps/orchestrator/AudioOrchestrator.json"
REMOTE_URL="https://raw.githubusercontent.com/slaesh/audio-orchestrator/main/apps/orchestrator/AudioOrchestrator.json"

if [ -f "$LOCAL_PATH" ]; then
    echo "Syncing OpenAPI spec from local audio-orchestrator repository..."
    cp "$LOCAL_PATH" "$SPEC_FILE"
else
    echo "Downloading OpenAPI spec from GitHub..."
    curl -fsSL "$REMOTE_URL" -o "$SPEC_FILE"
fi

echo "Successfully synchronized $SPEC_FILE!"
