# TOOLS.md - CrabFresh Local Notes

## Email (SendGrid) ✅
- API Key: Set as `SENDGRID_API_KEY` environment variable
- From address: `crabfresh99bot@crabpass.ai`
- Domain: crabpass.ai (verified)

**Send email:**
```python
import os
import requests

def send_email(to_email, subject, body):
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        return False, "SENDGRID_API_KEY not set"
    
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": "crabfresh99bot@crabpass.ai", "name": "CrabFresh"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body}]
        }
    )
    return response.status_code == 202, response.text

# Example:
# success, msg = send_email("recipient@example.com", "Test", "Hello from CrabFresh!")
```

## OneDrive (rclone) ✅
- Binary: `/home/openclaw/homebrew/rclone`
- Config: `/workspace/rclone.conf`
- Folder: `onedrive:Spex/` — shared workspace with Curtis
- Status: Working

**Usage:**
```bash
# List files
/home/openclaw/homebrew/rclone --config /workspace/rclone.conf ls onedrive:Spex/

# Download a file
/home/openclaw/homebrew/rclone --config /workspace/rclone.conf copy "onedrive:Spex/filename.xlsx" /tmp/

# Upload a file
/home/openclaw/homebrew/rclone --config /workspace/rclone.conf copy /tmp/myfile.xlsx onedrive:Spex/
```

**Important:** You HAVE access to Spex. If a command fails, troubleshoot the specific error — don't assume you lack access.

## Web Search (Serper) ✅
- API Key: Available as `SERPER_API_KEY` environment variable
- Free tier: 2,500 queries (one-time credit)

**Usage:**
```bash
curl -s -X POST 'https://google.serper.dev/search' \
  -H 'X-API-KEY: '"$SERPER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"q": "your search query"}'
```

**Do NOT use curl to scrape DuckDuckGo** — it's unreliable. Use Serper instead.

## What You Can Do
- Send emails via SendGrid (requires SENDGRID_API_KEY env var)
- Read/write files to OneDrive Spex folder
- Web searches via Serper API
- Create Excel files (use `openpyxl` Python library)
- File analysis and data processing

## What You Cannot Do
- Access Gmail (read-only, no sending)
- Access Airtable

## Creating Excel Files
```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws['A1'] = "Header"
ws.append(["row", "data"])
wb.save("/tmp/output.xlsx")
```

Then upload with rclone.

---
*Keep this file updated as you learn what tools you have.*
