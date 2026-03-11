# TOOLS.md - Local Notes

## Telegram
- Bot: @CrabFresh99Bot / @Shog99Bot (depending on deployment)
- Curtis's user ID: 8259734518

## Nextcloud (File Storage)
- Server: 64.23.225.208
- Admin: admin / ClawSign2026!
- WebDAV URL: https://64.23.225.208/remote.php/dav/files/admin/

**Upload file:**
```bash
curl -k -u "admin:ClawSign2026!" \
  -T /path/to/file.txt \
  "https://64.23.225.208/remote.php/dav/files/admin/file.txt"
```

**List files:**
```bash
curl -k -u "admin:ClawSign2026!" \
  -X PROPFIND \
  "https://64.23.225.208/remote.php/dav/files/admin/"
```

**Download file:**
```bash
curl -k -u "admin:ClawSign2026!" \
  -o output.txt \
  "https://64.23.225.208/remote.php/dav/files/admin/file.txt"
```

Note: -k flag for self-signed cert (if applicable)

## SendGrid
- Domain: crabpass.ai (verified)
- API key: Set via SENDGRID_API_KEY env var

## GitHub
- Token: Set via GITHUB_TOKEN env var

## Airtable
- Base: Stock Tracker (appp0mQjoNFff9lCU)
- Token: Set via AIRTABLE_API_KEY env var

---

Credentials are in Railway env vars for secrets. Nextcloud creds here for convenience (internal use only).
