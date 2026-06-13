from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:5173/", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(5000)
    page.evaluate("window.scrollTo(0, 900)")
    page.wait_for_timeout(2000)
    out = Path(__file__).resolve().parent.parent / "crawl-output" / "local-clone-content.png"
    page.screenshot(path=str(out))
    browser.close()
    print("Saved", out)
