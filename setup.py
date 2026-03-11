#!/usr/bin/env python3
import os
import json
import base64

owner_id = os.environ.get('OWNER_TELEGRAM_ID', '')
model = os.environ.get('OPENCLAW_MODEL', os.environ.get('MODEL', 'groq/llama-3.3-70b-versatile'))
bot_name = os.environ.get('BOT_NAME', 'Assistant')
bot_username = os.environ.get('BOT_USERNAME', '')

config = {
    "gateway": {"mode": "local"},
    "agents": {
        "defaults": {
            "model": {"primary": model},
            "compaction": {"reserveTokensFloor": 4000}
        }
    },
    "channels": {
        "telegram": {
            "enabled": True,
            "dmPolicy": os.environ.get('DM_POLICY', 'allowlist'),
        }
    }
}

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

config_data = json.dumps(config, indent=2)

state_dir = os.environ.get('OPENCLAW_STATE_DIR', '/home/openclaw/.openclaw')
os.makedirs(state_dir, exist_ok=True)
config_path = os.path.join(state_dir, 'config.json5')
with open(config_path, 'w') as f:
    f.write(config_data)
print(f"Config written to {config_path}")

workspace_dir = os.path.join(state_dir, 'workspace')
os.makedirs(workspace_dir, exist_ok=True)

# Create memory directory
memory_dir = os.path.join(workspace_dir, 'memory')
os.makedirs(memory_dir, exist_ok=True)

email_address = f"{bot_username.lower()}@crabpass.ai" if bot_username else "yourbot@crabpass.ai"

# AGENTS.md - Only create if doesn't exist
agents_path = os.path.join(workspace_dir, 'AGENTS.md')
if not os.path.exists(agents_path):
    with open(agents_path, 'w') as f:
        f.write(f"""# AGENTS.md

## Memory System
You wake up fresh each session. These files are your continuity:

1. **Read on startup:** SOUL.md, MEMORY.md, memory/YYYY-MM-DD.md (today)
2. **Write important things** to memory/YYYY-MM-DD.md as you go
3. **Update MEMORY.md** with key long-term info

## File Locations
- `SOUL.md` - Your identity and capabilities
- `MEMORY.md` - Long-term memory (curated)
- `memory/YYYY-MM-DD.md` - Daily logs

## Rules
- Write things down IMMEDIATELY - don't rely on "mental notes"
- If someone says "remember this", write it to a file
- Update memory files before session ends
""")
    print("Created AGENTS.md")
else:
    print("AGENTS.md exists, preserving")

# MEMORY.md - Only create if doesn't exist
memory_path = os.path.join(workspace_dir, 'MEMORY.md')
if not os.path.exists(memory_path):
    with open(memory_path, 'w') as f:
        f.write(f"""# MEMORY.md - Long-Term Memory

## Identity
- Name: {bot_name}
- Username: @{bot_username}
- Email: {email_address}

## Key Info
*(Add important things to remember here)*

## Lessons Learned
*(Add lessons from interactions)*

---
*Updated: (date)*
""")
    print("Created MEMORY.md")
else:
    print("MEMORY.md exists, preserving")

# SOUL.md - Only create if doesn't exist
soul_path = os.path.join(workspace_dir, 'SOUL.md')
if not os.path.exists(soul_path):
    with open(soul_path, 'w') as f:
        f.write(f"""# {bot_name}

You are a helpful AI assistant powered by CrabPass.

## Your Email
Your email address is: **{email_address}**

## Checking Email
```bash
curl -s "https://email-webhook-production-887d.up.railway.app/emails?bot_username={bot_username or 'YOUR_BOT_USERNAME'}&unread_only=true"
```

## Important
- Read AGENTS.md for memory instructions
- Read TOOLS.md for available integrations
- Write important info to memory files

## Personality
Be helpful, concise, and friendly.
""")
    print("Created SOUL.md")
else:
    print("SOUL.md exists, preserving")

# Email skill
skills_dir = os.path.join(workspace_dir, 'skills', 'email')
os.makedirs(skills_dir, exist_ok=True)
skill_path = os.path.join(skills_dir, 'SKILL.md')
with open(skill_path, 'w') as f:
    f.write(f"""# Email Skill

## Your Email Address
`{email_address}`

## Check Emails
```bash
curl -s "https://email-webhook-production-887d.up.railway.app/emails?bot_username={bot_username or 'YOUR_BOT_USERNAME'}"
```
Add `&unread_only=true` for unread only.

## Mark as Read
```bash
curl -s -X POST "https://email-webhook-production-887d.up.railway.app/emails/EMAIL_ID/read"
```
""")
print("Created/updated email skill")

# Only remove BOOTSTRAP.md (not needed after first boot)
bootstrap_path = os.path.join(workspace_dir, 'BOOTSTRAP.md')
if os.path.exists(bootstrap_path):
    os.remove(bootstrap_path)
    print("Removed BOOTSTRAP.md")

# Setup rclone if provided
rclone_config_b64 = os.environ.get('RCLONE_CONFIG_B64', '')
if rclone_config_b64:
    rclone_dir = os.path.expanduser('~/.config/rclone')
    os.makedirs(rclone_dir, exist_ok=True)
    rclone_path = os.path.join(rclone_dir, 'rclone.conf')
    try:
        rclone_config = base64.b64decode(rclone_config_b64).decode('utf-8')
        with open(rclone_path, 'w') as f:
            f.write(rclone_config)
        print("Wrote rclone config")
    except Exception as e:
        print(f"Failed to write rclone config: {e}")
