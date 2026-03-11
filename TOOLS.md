# TOOLS.md - Local Notes

## Telegram
- Bot: @CrabFresh99Bot / @Shog99Bot (depending on deployment)
- Curtis's user ID: 8259734518

## OneDrive (rclone)
- Remote: `onedrive:`
- Folder: `onedrive:Spex/` (Curtis's boundary - only access this folder)
- Config: Auto-configured from RCLONE_CONFIG_B64 env var

**List files:**
```bash
rclone ls onedrive:Spex/
```

**Upload file:**
```bash
rclone copy /path/to/file.txt onedrive:Spex/
```

**Download file:**
```bash
rclone copy onedrive:Spex/file.txt /local/path/
```

## Nextcloud (Alternative)
- Server: 64.23.225.208
- WebDAV URL: https://64.23.225.208/remote.php/dav/files/admin/
- Credentials: Set NEXTCLOUD_USER and NEXTCLOUD_PASS env vars

## SendGrid
- Domain: crabpass.ai (verified)
- API key: Set via SENDGRID_API_KEY env var

## GitHub
- Token: Set via GITHUB_TOKEN env var

## Airtable
- Base: Stock Tracker (appp0mQjoNFff9lCU)
- Token: Set via AIRTABLE_API_KEY env var

---

All secrets via Railway env vars.
