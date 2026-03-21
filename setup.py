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

# Add minimax provider if API key is set and model is minimax
minimax_api_key = os.environ.get('MINIMAX_API_KEY', '')
if minimax_api_key and model.startswith('minimax/'):
    config["models"] = {
        "mode": "merge",
        "providers": {
            "minimax": {
                "baseUrl": "https://api.minimax.io/anthropic",
                "apiKey": minimax_api_key,
                "api": "anthropic-messages",
                "models": [
                    {
                        "id": "MiniMax-M2.1",
                        "name": "MiniMax M2.1",
                        "reasoning": False,
                        "input": ["text"],
                        "cost": {"input": 15, "output": 60, "cacheRead": 2, "cacheWrite": 10},
                        "contextWindow": 200000,
                        "maxTokens": 8192
                    }
                ]
            }
        }
    }
    print("Added MiniMax provider config")

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

memory_dir = os.path.join(workspace_dir, 'memory')
os.makedirs(memory_dir, exist_ok=True)

email_address = f"{bot_username.lower()}@crabpass.ai" if bot_username else "yourbot@crabpass.ai"

# Setup rclone if provided - write to BOTH locations
rclone_config_b64 = os.environ.get('RCLONE_CONFIG_B64', '')
rclone_available = False
if rclone_config_b64:
    try:
        rclone_config = base64.b64decode(rclone_config_b64).decode('utf-8')
        # Write to standard location
        rclone_dir = os.path.expanduser('~/.config/rclone')
        os.makedirs(rclone_dir, exist_ok=True)
        with open(os.path.join(rclone_dir, 'rclone.conf'), 'w') as f:
            f.write(rclone_config)
        # Also write to workspace for reference
        with open(os.path.join(workspace_dir, 'rclone.conf'), 'w') as f:
            f.write(rclone_config)
        print("Wrote rclone config")
        rclone_available = True
    except Exception as e:
        print(f"Failed to write rclone config: {e}")

# Get Nextcloud settings
nextcloud_url = os.environ.get('NEXTCLOUD_URL', '')
nextcloud_user = os.environ.get('NEXTCLOUD_USER', '')
nextcloud_pass = os.environ.get('NEXTCLOUD_PASS', '')
nextcloud_available = bool(nextcloud_url and nextcloud_user and nextcloud_pass)

# TOOLS.md - preserve if exists
tools_content = f"""# TOOLS.md - Storage & Integrations

## Storage Access

"""

if rclone_available:
    tools_content += """### OneDrive (via rclone) ✅
**Status:** Configured

**List files:**
```bash
rclone ls onedrive:Spex/
```

**Copy file to OneDrive:**
```bash
rclone copy localfile.txt onedrive:Spex/
```

**Copy file from OneDrive:**
```bash
rclone copy onedrive:Spex/remotefile.txt ./
```

**Sync folder:**
```bash
rclone sync ./localfolder onedrive:Spex/remotefolder
```

"""
else:
    tools_content += """### OneDrive (via rclone) ❌
**Status:** Not configured - RCLONE_CONFIG_B64 not set

"""

if nextcloud_available:
    tools_content += f"""### Nextcloud ✅
**Status:** Configured
**URL:** {nextcloud_url}
**User:** {nextcloud_user}

**List files (WebDAV):**
```bash
curl -u "{nextcloud_user}:$NEXTCLOUD_PASS" "{nextcloud_url}/remote.php/dav/files/{nextcloud_user}/"
```

**Upload file:**
```bash
curl -u "{nextcloud_user}:$NEXTCLOUD_PASS" -T localfile.txt "{nextcloud_url}/remote.php/dav/files/{nextcloud_user}/remotefile.txt"
```

**Download file:**
```bash
curl -u "{nextcloud_user}:$NEXTCLOUD_PASS" -o localfile.txt "{nextcloud_url}/remote.php/dav/files/{nextcloud_user}/remotefile.txt"
```

**Note:** Nextcloud password is in NEXTCLOUD_PASS env var.

"""
else:
    tools_content += """### Nextcloud ❌
**Status:** Not configured - missing NEXTCLOUD_URL, NEXTCLOUD_USER, or NEXTCLOUD_PASS

"""

tools_content += """## Memory Persistence

**Important:** Your workspace is ephemeral! Save important files to OneDrive or Nextcloud.

**Before important work:**
1. Save current MEMORY.md to OneDrive: `rclone copy MEMORY.md onedrive:Spex/bots/{botname}/`
2. Save memory folder: `rclone sync memory/ onedrive:Spex/bots/{botname}/memory/`

**On startup:**
1. Check for saved memory: `rclone ls onedrive:Spex/bots/{botname}/`
2. Restore if exists: `rclone copy onedrive:Spex/bots/{botname}/ ./`

"""

tools_path = os.path.join(workspace_dir, "TOOLS.md")
if not os.path.exists(tools_path):
    with open(tools_path, "w") as f:
        f.write("# TOOLS.md\n\nNo storage configured yet.")
    print("Created placeholder TOOLS.md")
else:
    print("TOOLS.md exists, preserving")

# AGENTS.md - Only create if doesn't exist
agents_path = os.path.join(workspace_dir, 'AGENTS.md')
if not os.path.exists(agents_path):
    with open(agents_path, 'w') as f:
        f.write("""# AGENTS.md

## Memory System
You wake up fresh each session. These files are your continuity:

1. **Read on startup:** SOUL.md, MEMORY.md, TOOLS.md, memory/YYYY-MM-DD.md (today)
2. **Write important things** to memory/YYYY-MM-DD.md as you go
3. **Update MEMORY.md** with key long-term info
4. **Sync to OneDrive** periodically (see TOOLS.md)

## File Locations
- `SOUL.md` - Your identity and capabilities
- `MEMORY.md` - Long-term memory (curated)
- `TOOLS.md` - Storage and integration instructions
- `memory/YYYY-MM-DD.md` - Daily logs

## Rules
- Write things down IMMEDIATELY - don't rely on "mental notes"
- If someone says "remember this", write it to a file
- Sync important files to OneDrive before sessions end
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

You are a helpful AI assistant.

## Your Email
Your email address is: **{email_address}**

## Important
- Read AGENTS.md for memory instructions
- Read TOOLS.md for storage access (OneDrive, Nextcloud)
- Write important info to memory files
- Sync to OneDrive to persist across restarts

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
""")
print("Created/updated email skill")

# Remove BOOTSTRAP.md
bootstrap_path = os.path.join(workspace_dir, 'BOOTSTRAP.md')
if os.path.exists(bootstrap_path):
    os.remove(bootstrap_path)
    print("Removed BOOTSTRAP.md")

print("Bootstrap complete!")
