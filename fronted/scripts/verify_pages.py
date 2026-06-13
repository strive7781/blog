from pathlib import Path
from playwright.sync_api import sync_playwright

PAGES = [
    "/",
    "/archives/",
    "/tags/",
    "/categories/",
    "/about/",
    "/comments/",
    "/link/",
    "/moments/",
    "/pumpkin/",
    "/2026/03/08/Sad/",
    "/page/2/",
]

OUT = Path(__file__).resolve().parent.parent / "crawl-output" / "verify"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    OUT.mkdir(parents=True, exist_ok=True)
    ok, fail = 0, []
    for path in PAGES:
        url = f"http://localhost:5173{path}"
        name = path.strip("/").replace("/", "_") or "home"
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1500)
            status = resp.status if resp else 0
            title = page.title()
            page.screenshot(path=str(OUT / f"{name}.png"))
            if status == 200 and "404" not in title.lower():
                ok += 1
                print(f"OK {path} -> {title[:40]}")
            else:
                fail.append((path, status, title))
                print(f"WARN {path} status={status} title={title}")
        except Exception as e:
            fail.append((path, 0, str(e)))
            print(f"FAIL {path} {e}")
    browser.close()

print(f"Verified: {ok}/{len(PAGES)}")
if fail:
    for item in fail:
        print(" ", item)
