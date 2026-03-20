# TOOLS.md - Local Notes

## Telegram
- Bot: @Shog99Bot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- URL: https://cloud.clawsign.ai
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

---
Remember to sync to Nextcloud before any redeployment!
