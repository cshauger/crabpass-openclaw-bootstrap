# TOOLS.md - Local Notes

## Telegram
- Bot: @Shog99Bot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- Folder: `nextcloud:bots/Shog99Bot/`
- Config: /home/openclaw/.config/rclone/rclone.conf

**Sync workspace to Nextcloud (run before redeploys!):**
```bash
rclone sync /home/openclaw/.openclaw/workspace nextcloud:bots/Shog99Bot/ --exclude ".git/**"
```

**Download from Nextcloud:**
```bash
rclone copy nextcloud:bots/Shog99Bot/MEMORY.md /home/openclaw/.openclaw/workspace/
```

## SendGrid
- Domain: crabpass.ai (verified)
- API key: Set via SENDGRID_API_KEY env var

## GitHub
- Token: Set via GITHUB_TOKEN env var

---

All secrets via Railway env vars.
Remember to sync to Nextcloud before any redeployment!
