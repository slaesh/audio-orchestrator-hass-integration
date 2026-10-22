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

echo "Generating Python TypedDict models via datamodel-code-generator..."
datamodel-codegen \
    --input "$SPEC_FILE" \
    --input-file-type openapi \
    --output custom_components/audio_orchestrator/models.py \
    --output-model-type typing.TypedDict

echo "Formatting models via ruff..."
ruff check --target-version py312 --fix --unsafe-fixes custom_components/audio_orchestrator/models.py || true

echo "Successfully generated and formatted custom_components/audio_orchestrator/models.py!"
