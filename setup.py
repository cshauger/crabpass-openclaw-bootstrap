#!/usr/bin/env python3
import os
import base64
import json

config_b64 = os.environ.get('OPENCLAW_CONFIG_B64', '')
owner_id = os.environ.get('OWNER_TELEGRAM_ID', '')

if config_b64:
    config_data = base64.b64decode(config_b64).decode()
else:
    # Build config - NO model key at root (use ANTHROPIC_MODEL env var instead)
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

# Use OPENCLAW_STATE_DIR or default
config_dir = os.environ.get('OPENCLAW_STATE_DIR', os.path.expanduser('~/.openclaw'))
os.makedirs(config_dir, exist_ok=True)
config_path = os.path.join(config_dir, 'config.json5')
with open(config_path, 'w') as f:
    f.write(config_data)
print(f"Config written to {config_path}:")
print(config_data)
