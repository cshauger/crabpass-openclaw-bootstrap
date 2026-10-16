#!/usr/bin/env python3
"""
Page Monitor - Takes screenshots and can be used with vision AI for verification
Usage: python3 page_monitor.py <url> [output_path]
"""
import sys
from playwright.sync_api import sync_playwright

def capture_page(url: str, output_path: str = "/tmp/screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.screenshot(path=output_path, full_page=False)
        title = page.title()
        browser.close()
        return title, output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 page_monitor.py <url> [output_path]")
        sys.exit(1)
    
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "/tmp/screenshot.png"
    
    title, path = capture_page(url, output)
    print(f"Title: {title}")
    print(f"Screenshot saved: {path}")
