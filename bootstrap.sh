#!/bin/sh
set -e

echo "=== OpenClaw Bootstrap ==="

# Required vars
: "${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN required}"
: "${OWNER_TELEGRAM_ID:?OWNER_TELEGRAM_ID required}"

# Default model
MODEL="${MODEL:-groq/llama-3.3-70b-versatile}"

# Config goes in home directory  
CONFIG_DIR="$HOME/.openclaw"
mkdir -p "$CONFIG_DIR"

# Create config.json5
cat > "$CONFIG_DIR/config.json5" << CONF
{
  model: "$MODEL",
  channels: {
    telegram: {
      enabled: true,
      botToken: "$TELEGRAM_BOT_TOKEN",
      dmPolicy: "allowlist",
      allowFrom: ["$OWNER_TELEGRAM_ID"]
    }
  }
}
CONF

echo "Config created:"
cat "$CONFIG_DIR/config.json5"

echo ""
echo "Starting OpenClaw gateway..."
cd /app
exec node dist/index.js gateway
