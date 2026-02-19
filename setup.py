#!/usr/bin/env python3
import os
import json

owner_id = os.environ.get('OWNER_TELEGRAM_ID', '')

# Minimal config - just gateway and channels
config = {
    "gateway": {"mode": "local"},
    "channels": {
        "telegram": {
            "enabled": True,
            "dmPolicy": os.environ.get('DM_POLICY', 'allowlist'),
        }
    }
}
if owner_id:
    config["channels"]["telegram"]["allowFrom"] = [owner_id]

config_data = json.dumps(config, indent=2)

# Write config
config_dir = os.environ.get('OPENCLAW_STATE_DIR', os.path.expanduser('~/.openclaw'))
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'config.json5')
with open(config_path, 'w') as f:
    f.write(config_data)
print(f"Config written to {config_path}:")
print(config_data)
