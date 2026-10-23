#!/usr/bin/env python3
import os
import json
import base64

owner_id = os.environ.get('OWNER_TELEGRAM_ID', '')
model = os.environ.get('OPENCLAW_MODEL', os.environ.get('MODEL', 'groq/llama-3.3-70b-versatile'))
bot_name = os.environ.get('BOT_NAME', 'Assistant')
bot_username = os.environ.get('BOT_USERNAME', '')

config = {"gateway": {"mode": "local"}, "agents": {"defaults": {"model": {"primary": model}}}, "channels": {"telegram": {"enabled": True, "dmPolicy": os.environ.get('DM_POLICY', 'allowlist')}}}

allowed_users = []
if owner_id:
    allowed_users.append(owner_id)
extra_users = os.environ.get('ALLOWED_USERS', '')
if extra_users:
    for uid in extra_users.split(','):
        uid = uid.strip()
        if uid and uid not in allowed_users:
            allowed_users.append(uid)
if allowed_users:
    config["channels"]["telegram"]["allowFrom"] = allowed_users

state_dir = os.environ.get('OPENCLAW_STATE_DIR', '/home/openclaw/.openclaw')
os.makedirs(state_dir, exist_ok=True)
with open(os.path.join(state_dir, 'config.json5'), 'w') as f:
    f.write(json.dumps(config, indent=2))
print(f"Config written to {state_dir}/config.json5")

workspace_dir = os.path.join(state_dir, 'workspace')
os.makedirs(workspace_dir, exist_ok=True)
os.makedirs(os.path.join(workspace_dir, 'memory'), exist_ok=True)

rclone_config_b64 = os.environ.get('RCLONE_CONFIG_B64', '')
if rclone_config_b64:
    try:
        rclone_config = base64.b64decode(rclone_config_b64).decode('utf-8')
        rclone_dir = os.path.expanduser('~/.config/rclone')
        os.makedirs(rclone_dir, exist_ok=True)
        with open(os.path.join(rclone_dir, 'rclone.conf'), 'w') as f:
            f.write(rclone_config)
        with open(os.path.join(workspace_dir, 'rclone.conf'), 'w') as f:
            f.write(rclone_config)
        print("Wrote rclone config")
    except Exception as e:
        print(f"Failed to write rclone config: {e}")

nextcloud_url = os.environ.get('NEXTCLOUD_URL', '')
nextcloud_user = os.environ.get('NEXTCLOUD_USER', '')

tools = f"""# TOOLS.md - Storage

## Nextcloud (via rclone)
**URL:** {nextcloud_url}

**List files:**
```bash
rclone ls nextcloud:
rclone ls nextcloud:bots/{bot_username}/
```

**Sync to Nextcloud:**
```bash
rclone sync ./ nextcloud:bots/{bot_username}/ --exclude rclone.conf
```

**Restore from Nextcloud:**
```bash
rclone copy nextcloud:bots/{bot_username}/ ./
```
"""

with open(os.path.join(workspace_dir, 'TOOLS.md'), 'w') as f:
    f.write(tools)
print("Created TOOLS.md")

if not os.path.exists(os.path.join(workspace_dir, 'AGENTS.md')):
    with open(os.path.join(workspace_dir, 'AGENTS.md'), 'w') as f:
        f.write("# AGENTS.md\n\nSync to Nextcloud periodically.\n")
    print("Created AGENTS.md")
else:
    print("AGENTS.md exists")

if not os.path.exists(os.path.join(workspace_dir, 'MEMORY.md')):
    with open(os.path.join(workspace_dir, 'MEMORY.md'), 'w') as f:
        f.write(f"# MEMORY.md\n\n## Identity\n- Name: {bot_name}\n- Username: @{bot_username}\n")
    print("Created MEMORY.md")
else:
    print("MEMORY.md exists")

if not os.path.exists(os.path.join(workspace_dir, 'SOUL.md')):
    with open(os.path.join(workspace_dir, 'SOUL.md'), 'w') as f:
        f.write(f"# {bot_name}\n\nYou are a helpful AI assistant.\n")
    print("Created SOUL.md")
else:
    print("SOUL.md exists")

print("Bootstrap complete!")
