#!/bin/sh
set -e

echo "=== OpenClaw Bootstrap ==="

# Run Python setup to create config
python3 /setup.py

echo ""
echo "Starting OpenClaw gateway..."
cd /app
exec node dist/index.js gateway
