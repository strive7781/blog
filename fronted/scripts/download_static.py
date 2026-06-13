import re
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://cyborg2077.github.io"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
OUT.mkdir(parents=True, exist_ok=True)

STATIC_EXT = {
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".woff", ".woff2", ".ttf", ".ico", ".json", ".mp3", ".mp4", ".xml",
}

html = (ROOT / "public" / "index.html").read_text(encoding="utf-8") if (ROOT / "public" / "index.html").exists() else (ROOT / "public" / "index.html").read_text(encoding="utf-8")

paths = set()
for m in re.finditer(r'(?:href|src)=["\'](/[^"\']+)["\']', html):
    rel = m.group(1).split("?")[0]
    if any(rel.lower().endswith(ext) for ext in STATIC_EXT):
        paths.add(rel)

paths.update([
    "/css/index.css", "/css/custom.css", "/img/favicon.png",
    "/assets/r1.png", "/assets/r2.jpg",
    "/js/main.js", "/js/utils.js", "/js/fomal.js", "/js/txmap.js",
    "/js/search/local-search.js",
])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    ok, fail = 0, []
    for rel in sorted(paths):
        dest = OUT / rel.lstrip("/")
        if dest.exists() and dest.stat().st_size > 100:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            resp = ctx.request.get(BASE + rel, timeout=120000)
            if resp.ok:
                dest.write_bytes(resp.body())
                ok += 1
            else:
                fail.append((rel, resp.status))
        except Exception as e:
            fail.append((rel, str(e)[:100]))
    browser.close()

print("Downloaded", ok, "failed", len(fail))
for f in fail:
    print(f)
