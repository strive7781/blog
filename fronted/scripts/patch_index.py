import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
BASE = "https://cyborg2077.github.io"

html_path = PUBLIC / "index.html"
html = html_path.read_text(encoding="utf-8")

# Fix protocol-relative CDN URLs
html = re.sub(r'((?:href|src)=["\'])//', r'\1https://', html)

bootstrap = """
<style id="clone-bootstrap">
:root {
  --theme-color: rgb(57, 197, 187) !important;
  --trans-light: rgba(253, 253, 253, 95%) !important;
  --trans-dark: rgba(25, 25, 25, 95%) !important;
  --blur-num: blur(20px) saturate(120%) !important;
  --backdrop-filter: var(--blur-num);
  --rightside-display: block;
  --default-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg);
  --darkmode-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/night01.jpg);
  --mobileday-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg);
  --mobilenight-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/night01.jpg);
}
.recent-post-item.wow,
.card-widget.wow {
  visibility: visible !important;
}
</style>
"""

if "clone-bootstrap" not in html:
    html = html.replace("</head>", bootstrap + "</head>", 1)

html_path.write_text(html, encoding="utf-8")
print("Patched index.html")

assets = [
    "/img/favicon.png",
    "/assets/r2.jpg",
    "/font/优设好身�?woff2",
    "/live2dw/lib/L2Dwidget.min.js",
    "/live2dw/lib/L2Dwidget.0.min.js",
    "/live2dw/live2d-widget-model.json",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    for rel in assets:
        dest = PUBLIC / rel.lstrip("/")
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            resp = ctx.request.get(BASE + rel, timeout=120000)
            if resp.ok:
                dest.write_bytes(resp.body())
                print("OK", rel, len(resp.body()))
            else:
                print("FAIL", rel, resp.status)
        except Exception as e:
            print("ERR", rel, e)
    browser.close()

print("Done")
