#!/bin/sh
set -e

echo "=== OpenClaw Bootstrap ==="

# Run Python setup first (creates rclone config)
python3 /setup.py

# Pull secrets from Nextcloud using rclone
echo ""
echo "Fetching secrets from Nextcloud..."
if rclone copy nextcloud:bots/ShogMini/shogmini-secrets.json /tmp/ 2>/dev/null; then
    if [ -f /tmp/shogmini-secrets.json ]; then
        echo "Loading secrets..."
        # Use Python to parse JSON and export vars
        eval $(python3 -c "
import json
with open('/tmp/shogmini-secrets.json') as f:
    secrets = json.load(f)
for k, v in secrets.items():
    # Escape single quotes in values
    v_escaped = str(v).replace(\"'\", \"'\\\"'\\\"'\")
    print(f\"export {k}='{v_escaped}'\")
")
        rm /tmp/shogmini-secrets.json
        echo "Secrets loaded. TELEGRAM_BOT_TOKEN set: $([ -n \"$TELEGRAM_BOT_TOKEN\" ] && echo 'yes' || echo 'no')"
    else
        echo "Warning: secrets file not downloaded."
    fi
else
    echo "Warning: could not fetch secrets from Nextcloud, continuing..."
fi

echo ""
echo "Starting OpenClaw gateway..."
cd /app
exec node dist/index.js gateway
