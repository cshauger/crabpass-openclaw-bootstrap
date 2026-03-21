# TOOLS.md - Local Notes

## Telegram
- Bot: @CrabFresh99Bot
- Curtis's user ID: 8259734518

## Nextcloud (Primary Storage)
- Remote: `nextcloud:`
- URL: https://cloud.clawsign.ai
- Folder: `nextcloud:bots/Crabfresh/`

**List folders:**
```bash
rclone --config ~/.config/rclone/rclone.conf lsd nextcloud:
```

**Sync workspace to Nextcloud (run before redeploys!):**
```bash
rclone --config ~/.config/rclone/rclone.conf sync /home/openclaw/.openclaw/workspace nextcloud:bots/Crabfresh/ --exclude ".git/**"
```

**Download from Nextcloud:**
```bash
rclone --config ~/.config/rclone/rclone.conf copy nextcloud:bots/Crabfresh/ /home/openclaw/.openclaw/workspace/
```

---
**Note:** OneDrive access removed. Use Nextcloud only.
