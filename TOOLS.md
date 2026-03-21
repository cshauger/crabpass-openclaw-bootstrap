# TOOLS.md - Local Notes

## Telegram
- Bot: @ShogGPTBot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- URL: https://cloud.clawsign.ai
- Folder: `nextcloud:bots/ShogGPT/`
- Config: ~/.config/rclone/rclone.conf

**List folders:**
```bash
rclone --config ~/.config/rclone/rclone.conf lsd nextcloud:
```

**Sync workspace to Nextcloud (run before redeploys!):**
```bash
rclone --config ~/.config/rclone/rclone.conf sync /home/openclaw/.openclaw/workspace nextcloud:bots/ShogGPT/ --exclude ".git/**"
```

**Download from Nextcloud:**
```bash
rclone --config ~/.config/rclone/rclone.conf copy nextcloud:bots/ShogGPT/MEMORY.md /home/openclaw/.openclaw/workspace/
```

---
Remember to sync to Nextcloud before any redeployment!

**Note:** OneDrive access has been removed. Use Nextcloud only.
