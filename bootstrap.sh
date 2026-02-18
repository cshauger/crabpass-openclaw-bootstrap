#!/bin/sh
set -e

echo "=== OpenClaw Bootstrap ==="

# Required vars
: "${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN required}"
: "${OWNER_TELEGRAM_ID:?OWNER_TELEGRAM_ID required}"

# Default model
MODEL="${MODEL:-groq/llama-3.3-70b-versatile}"

# Config goes in home directory
CONFIG_DIR="/home/node/.openclaw"
mkdir -p "$CONFIG_DIR"

# Create config.json5 (OpenClaw uses JSON5, not YAML!)
cat > "$CONFIG_DIR/config.json5" << EOF
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
EOF

echo "Config created at $CONFIG_DIR/config.json5:"
cat "$CONFIG_DIR/config.json5"
echo ""

# Create workspace
WORKSPACE="/home/node/.openclaw/workspace"
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
cd /app
exec node dist/index.js gateway
