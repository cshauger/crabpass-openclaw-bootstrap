# TOOLS.md - Local Notes

## Telegram
- Bot: @ShogGPTBot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- URL: https://cloud.clawsign.ai
- Folder: `nextcloud:bots/ShogGPT/`
- Config: /home/openclaw/.config/rclone/rclone.conf

**Sync workspace to Nextcloud (run before redeploys!):**
```bash
rclone sync /home/openclaw/.openclaw/workspace nextcloud:bots/ShogGPT/ --exclude ".git/**"
```

**Download from Nextcloud:**
```bash
rclone copy nextcloud:bots/ShogGPT/MEMORY.md /home/openclaw/.openclaw/workspace/
```

---
Remember to sync to Nextcloud before any redeployment!

**Note:** OneDrive access has been removed. Use Nextcloud only.
