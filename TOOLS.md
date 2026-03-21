# TOOLS.md - Local Notes

## Telegram
- Bot: @CrabFresh99Bot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- URL: https://cloud.clawsign.ai
- Folder: `nextcloud:bots/Crabfresh/`
- Config: /home/openclaw/.config/rclone/rclone.conf

**Sync workspace to Nextcloud (run before redeploys!):**
```bash
rclone sync /home/openclaw/.openclaw/workspace nextcloud:bots/Crabfresh/ --exclude ".git/**"
```

**Download from Nextcloud:**
```bash
rclone copy nextcloud:bots/Crabfresh/MEMORY.md /home/openclaw/.openclaw/workspace/
```

---
Remember to sync to Nextcloud before any redeployment!
