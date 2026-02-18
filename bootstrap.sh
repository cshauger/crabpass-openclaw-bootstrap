#!/bin/sh
set -e

CONFIG_DIR="${OPENCLAW_STATE_DIR:-/data/.openclaw}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR:-/data/workspace}"

echo "=== OpenClaw Bootstrap ==="
echo "Config: $CONFIG_DIR"
echo "Workspace: $WORKSPACE_DIR"

# Required vars
: "${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN required}"
: "${OWNER_TELEGRAM_ID:?OWNER_TELEGRAM_ID required}"

# Default model - use Groq free tier
MODEL="${MODEL:-groq/llama-3.3-70b-versatile}"

# Create config.yaml
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_DIR/config.yaml" << EOF
model: $MODEL

channels:
  telegram:
    token: $TELEGRAM_BOT_TOKEN
    allowedUsers:
      - "$OWNER_TELEGRAM_ID"
EOF

# Add API keys if provided
if [ -n "$GROQ_API_KEY" ]; then
  echo "groqApiKey: $GROQ_API_KEY" >> "$CONFIG_DIR/config.yaml"
fi
if [ -n "$ANTHROPIC_API_KEY" ]; then
  echo "anthropicApiKey: $ANTHROPIC_API_KEY" >> "$CONFIG_DIR/config.yaml"
fi
if [ -n "$OPENAI_API_KEY" ]; then
  echo "openaiApiKey: $OPENAI_API_KEY" >> "$CONFIG_DIR/config.yaml"
fi

echo "Config generated:"
cat "$CONFIG_DIR/config.yaml"
echo ""

# Create workspace files if not exist
mkdir -p "$WORKSPACE_DIR"
if [ ! -f "$WORKSPACE_DIR/SOUL.md" ]; then
  cat > "$WORKSPACE_DIR/SOUL.md" << 'SOUL'
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
