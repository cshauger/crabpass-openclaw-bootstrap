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
        # Write to env file and source it
        jq -r 'to_entries[] | "export " + .key + "=" + (.value | @sh)' /tmp/shogmini-secrets.json > /tmp/secrets.env
        . /tmp/secrets.env
        rm /tmp/shogmini-secrets.json /tmp/secrets.env
        echo "Secrets loaded. TELEGRAM_BOT_TOKEN length: ${#TELEGRAM_BOT_TOKEN}"
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
