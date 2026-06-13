from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://cyborg2077.github.io"
PUBLIC = Path(__file__).resolve().parent.parent / "public"

paths = [
    "/live2dw/assets/koharu.model.json",
    "/img/favicon.png",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
    for rel in paths:
        dest = PUBLIC / rel.lstrip("/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(3):
            try:
                resp = page.request.get(BASE + rel, timeout=120000)
                if resp.ok:
                    dest.write_bytes(resp.body())
                    print("OK", rel, len(resp.body()))
                    break
                print("FAIL", rel, resp.status, "attempt", attempt + 1)
            except Exception as e:
                print("ERR", rel, attempt + 1, str(e)[:80])
    browser.close()

# Screenshot local clone
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:5173/", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(6000)
    out = Path(__file__).resolve().parent.parent / "crawl-output" / "local-clone.png"
    page.screenshot(path=str(out))
    browser.close()
    print("Saved", out)
