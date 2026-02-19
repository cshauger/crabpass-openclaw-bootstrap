#!/usr/bin/env python3
import os
import json

owner_id = os.environ.get('OWNER_TELEGRAM_ID', '')
model = os.environ.get('OPENCLAW_MODEL', os.environ.get('MODEL', 'groq/llama-3.3-70b-versatile'))
bot_name = os.environ.get('BOT_NAME', 'Assistant')

# Config with compaction settings
config = {
    "gateway": {"mode": "local"},
    "agents": {
        "defaults": {
            "model": {
                "primary": model
            },
            "compaction": {
                "reserveTokensFloor": 4000
            }
        }
    },
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
state_dir = os.environ.get('OPENCLAW_STATE_DIR', os.path.expanduser('~/.openclaw'))
os.makedirs(state_dir, exist_ok=True)
config_path = os.path.join(state_dir, 'config.json5')
with open(config_path, 'w') as f:
    f.write(config_data)
print(f"Config written to {config_path}:")
print(config_data)

# Create MINIMAL workspace - critical for Groq rate limits
workspace_dir = os.path.join(state_dir, 'workspace')
os.makedirs(workspace_dir, exist_ok=True)

# Tiny SOUL.md
soul_path = os.path.join(workspace_dir, 'SOUL.md')
with open(soul_path, 'w') as f:
    f.write(f"""# {bot_name}
You are a helpful AI assistant. Be concise.
""")
print(f"Created minimal SOUL.md")

# Remove default AGENTS.md and BOOTSTRAP.md if they exist
for fname in ['AGENTS.md', 'BOOTSTRAP.md', 'USER.md', 'MEMORY.md']:
    fpath = os.path.join(workspace_dir, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        print(f"Removed {fname}")
