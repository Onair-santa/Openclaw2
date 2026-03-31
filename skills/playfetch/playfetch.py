#!/usr/bin/env python3
"""playfetch - загрузка страниц через Playwright"""
import sys
from playwright.sync_api import sync_playwright

if len(sys.argv) < 2:
    print("Usage: playfetch <url>", file=sys.stderr)
    sys.exit(1)

url = sys.argv[1]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=30000)
    print(page.content())
    browser.close()
