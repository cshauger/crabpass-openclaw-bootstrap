#!/bin/sh
set -e

echo "=== OpenClaw Bootstrap ==="

# Required vars
: "${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN required}"
: "${OWNER_TELEGRAM_ID:?OWNER_TELEGRAM_ID required}"

# Default model
MODEL="${MODEL:-groq/llama-3.3-70b-versatile}"

# Use the STATE_DIR from env (set in Dockerfile)
CONFIG_DIR="${OPENCLAW_STATE_DIR:-/data/.openclaw}"
mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/config.json5"

# Create config.json5
cat > "$CONFIG_FILE" << EOF
{
  model: "$MODEL",
  gateway: {
    mode: "local"
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "$TELEGRAM_BOT_TOKEN",
      dmPolicy: "allowlist",
      allowFrom: ["$OWNER_TELEGRAM_ID"]
    }
  }
}
EOF

echo "Config created at $CONFIG_FILE:"
cat "$CONFIG_FILE"
echo ""

# Export config path so OpenClaw finds it
export OPENCLAW_CONFIG_PATH="$CONFIG_FILE"

# Create workspace
WORKSPACE="$CONFIG_DIR/workspace"
mkdir -p "$WORKSPACE"

if [ ! -f "$WORKSPACE/SOUL.md" ]; then
  cat > "$WORKSPACE/SOUL.md" << 'SOUL'
# Your AI Assistant

You are a helpful personal AI assistant.

## Personality
- Friendly and helpful
- Concise but thorough when needed
- Honest about limitations

## Guidelines
- Be genuinely useful
- Remember context from conversation
- Ask for clarification when needed
SOUL
  echo "Created default SOUL.md"
fi

echo "Starting OpenClaw gateway..."
echo "OPENCLAW_STATE_DIR=$OPENCLAW_STATE_DIR"
echo "OPENCLAW_CONFIG_PATH=$OPENCLAW_CONFIG_PATH"

cd /app
exec node dist/index.js gateway
