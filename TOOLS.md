# TOOLS.md - CrabFresh Local Notes

## OneDrive (rclone) ✅
- Binary: `/home/openclaw/homebrew/rclone`
- Config: `/workspace/rclone.conf`
- Folder: `onedrive:Spex/` — this is your shared workspace with Curtis
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

**Important:** You HAVE access to Spex. Don't second-guess this. If a command fails, troubleshoot the specific error — don't assume you lack access.

## What You Can Do
- Read/write files to OneDrive Spex folder
- Create Excel files (use `openpyxl` Python library)
- Web searches and research
- File analysis and data processing

## What You Cannot Do
- Send emails (no SendGrid configured)
- Access Gmail
- Access Airtable
- Access other cloud services

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
