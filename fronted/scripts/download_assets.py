import re
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://cyborg2077.github.io"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
OUT.mkdir(parents=True, exist_ok=True)

html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")

# All /path assets from HTML
paths = set()
for m in re.finditer(r'(?:href|src)=["\'](/[^"\']+)["\']', html):
    paths.add(m.group(1).split("?")[0])

# Common static dirs
extra = [
    "/img/favicon.png",
    "/img/404.jpg",
    "/img/error-page.png",
    "/img/friend_404.gif",
    "/assets/r1.png",
    "/assets/r2.jpg",
    "/assets/r3.jpg",
    "/assets/r4.jpg",
    "/assets/r5.jpg",
    "/assets/r6.jpg",
    "/assets/r7.jpg",
    "/assets/r8.jpg",
    "/assets/r9.jpg",
    "/assets/r10.jpg",
    "/assets/r11.jpg",
    "/assets/r12.jpg",
    "/assets/r13.jpg",
    "/assets/r14.jpg",
    "/assets/r15.jpg",
    "/assets/r16.jpg",
    "/assets/r17.jpg",
    "/assets/r18.jpg",
    "/assets/r19.jpg",
    "/assets/r20.jpg",
]
paths.update(extra)

# JS bundle paths from main.js imports if any
for js in OUT.rglob("*.js"):
    text = js.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r'["\'](/[^"\']+\.js)["\']', text):
        paths.add(m.group(1))

print("Total paths:", len(paths))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    ok, skip, fail = 0, 0, []
    for rel in sorted(paths):
        dest = OUT / rel.lstrip("/")
        if dest.exists() and dest.stat().st_size > 0:
            skip += 1
            continue
        url = BASE + rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            resp = ctx.request.get(url, timeout=120000)
            if resp.ok:
                dest.write_bytes(resp.body())
                ok += 1
                print("OK", rel, dest.stat().st_size)
            else:
                fail.append((rel, resp.status))
        except Exception as e:
            fail.append((rel, str(e)[:120]))
    browser.close()

print(f"Downloaded {ok}, skipped {skip}, failed {len(fail)}")
for item in fail[:40]:
    print(" FAIL", item)
