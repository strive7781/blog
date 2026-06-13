import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://cyborg2077.github.io"
PUBLIC = Path(__file__).resolve().parent.parent / "public"
model_root = PUBLIC / "live2dw/assets"

paths = [
    "/live2dw/assets/koharu.model.json",
    "/live2dw/assets/koharu.physics.json",
    "/live2dw/assets/moc/koharu.moc",
    "/live2dw/assets/moc/koharu.2048/texture_00.png",
    "/live2dw/assets/mtn/idle.mtn",
    "/live2dw/assets/mtn/01.mtn",
    "/live2dw/assets/mtn/02.mtn",
    "/live2dw/assets/mtn/03.mtn",
    "/live2dw/assets/mtn/04.mtn",
    "/live2dw/assets/mtn/05.mtn",
    "/live2dw/assets/mtn/06.mtn",
    "/live2dw/assets/mtn/07.mtn",
    "/live2dw/assets/mtn/08.mtn",
    "/live2dw/assets/mtn/09.mtn",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    for rel in paths:
        dest = PUBLIC / rel.lstrip("/")
        if dest.exists() and dest.stat().st_size > 50:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(3):
            try:
                resp = ctx.request.get(BASE + rel, timeout=120000)
                if resp.ok:
                    dest.write_bytes(resp.body())
                    print("OK", rel, len(resp.body()))
                    break
                print("FAIL", rel, resp.status)
            except Exception as e:
                if attempt == 2:
                    print("ERR", rel, e)
    browser.close()

print("Model files ready")
