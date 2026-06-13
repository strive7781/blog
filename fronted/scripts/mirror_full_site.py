import os
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

BASE = "https://cyborg2077.github.io"
ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
REPORT = ROOT / "mirror-report.txt"

BOOTSTRAP = """
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

STATIC_EXT = (
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    ".woff", ".woff2", ".ttf", ".ico", ".json", ".xml", ".mp3",
)

SKIP_PATH_PREFIXES = ("/js/", "/css/", "/live2dw/", "/assets/")


def log(msg: str):
    print(msg, flush=True)


def is_page_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc and "cyborg2077.github.io" not in parsed.netloc:
        return False
    path = parsed.path.split("?")[0]
    lower = path.lower()
    if any(lower.endswith(ext) for ext in STATIC_EXT):
        return False
    for prefix in SKIP_PATH_PREFIXES:
        if lower.startswith(prefix.lstrip("/")) or lower.startswith(prefix):
            return False
    if "/assets/" in lower or lower.startswith("/img/"):
        return False
    # skip heading anchor slugs inside articles
    parts = [p for p in lower.strip("/").split("/") if p]
    if len(parts) >= 5 and parts[0].isdigit() and len(parts) > 4:
        slug = parts[4]
        if "%" in slug or any(c in slug for c in "<>=≤≥") or " " in slug:
            return False
    if lower.endswith("/atom.xml") or lower == "/atom.xml":
        return False
    return True


def url_to_local_path(url: str) -> Path:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return PUBLIC / "index.html"
    if path.endswith(".html"):
        return PUBLIC / path
    return PUBLIC / path / "index.html"


def patch_html(html: str) -> str:
    html = re.sub(r'((?:href|src)=["\'])//', r"\1https://", html)
    if "clone-bootstrap" not in html:
        html = html.replace("</head>", BOOTSTRAP + "</head>", 1)
    return html


def collect_static_paths(html: str) -> set[str]:
    paths = set()
    for m in re.finditer(r'(?:href|src)=["\'](/[^"\']+)["\']', html):
        rel = m.group(1).split("?")[0]
        if rel.lower().endswith(STATIC_EXT):
            paths.add(rel)
    return paths


def extract_links(html: str) -> set[str]:
    links = set()
    for m in re.finditer(r'href="(https://cyborg2077\.github\.io/[^"#?]+/?)"', html):
        u = m.group(1).split("#")[0]
        if not u.endswith("/") and not u.endswith(".html"):
            u += "/"
        links.add(u)
    for m in re.finditer(r'href="(/[^"#?]+/?)"', html):
        rel = m.group(1)
        if rel.startswith(SKIP_PATH_PREFIXES):
            continue
        if any(rel.lower().endswith(ext) for ext in STATIC_EXT):
            continue
        u = BASE + rel
        if not u.endswith("/") and not u.endswith(".html"):
            u += "/"
        links.add(u)
    return links


def safe_rglob_html() -> list[Path]:
    results = []
    for dirpath, dirnames, filenames in os.walk(PUBLIC):
        if "index.html" in filenames:
            results.append(Path(dirpath) / "index.html")
    return results


def cleanup_bad_pages():
    removed = 0
    for html in safe_rglob_html():
        rel = html.relative_to(PUBLIC).as_posix()
        if rel.startswith("img/") and rel.endswith("/index.html"):
            parent = html.parent
            try:
                shutil.rmtree(parent)
                removed += 1
            except Exception as e:
                log(f"warn remove {parent}: {e}")
    log(f"Removed {removed} bad img/* pages")


def collect_urls_from_atom() -> set[str]:
    atom = PUBLIC / "atom.xml"
    if not atom.exists():
        return set()
    text = atom.read_text(encoding="utf-8", errors="ignore")
    urls = set(re.findall(r"<link href=\"(https://cyborg2077\.github\.io/[^\"]+)\"", text))
    out = set()
    for u in urls:
        u = u.split("#")[0]
        if not u.endswith("/") and not u.endswith(".html"):
            u += "/"
        out.add(u)
    return out


def collect_urls_from_existing() -> set[str]:
    urls = set()
    for html in safe_rglob_html():
        try:
            urls |= extract_links(html.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass
    return urls


def seed_urls() -> set[str]:
    seeds = {
        f"{BASE}/",
        f"{BASE}/archives/",
        f"{BASE}/tags/",
        f"{BASE}/categories/",
        f"{BASE}/about/",
        f"{BASE}/comments/",
        f"{BASE}/link/",
        f"{BASE}/moments/",
        f"{BASE}/pumpkin/",
        f"{BASE}/secret/",
        f"{BASE}/charts/",
        f"{BASE}/box/fitness/",
        f"{BASE}/box/animation/",
        f"{BASE}/box/nav/",
        f"{BASE}/social/link/",
        f"{BASE}/personal/about/",
    }
    for i in range(2, 16):
        seeds.add(f"{BASE}/page/{i}/")
    seeds |= collect_urls_from_atom()
    seeds |= collect_urls_from_existing()
    return {u for u in seeds if is_page_url(u)}


def mirror_site():
    cleanup_bad_pages()

    todo = seed_urls()
    done: set[str] = set()
    static_paths: set[str] = set()
    fail: list[tuple[str, str]] = []

    for url in list(todo):
        dest = url_to_local_path(url)
        if dest.exists() and dest.stat().st_size > 5000:
            done.add(url)
    todo -= done
    log(f"Resume: {len(done)} done, {len(todo)} todo")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        ctx = browser.new_context()

        while todo:
            url = todo.pop()
            if url in done or not is_page_url(url):
                continue

            dest = url_to_local_path(url)
            if dest.exists() and dest.stat().st_size > 5000:
                done.add(url)
                try:
                    for link in extract_links(dest.read_text(encoding="utf-8", errors="ignore")):
                        if link not in done and is_page_url(link):
                            todo.add(link)
                except Exception:
                    pass
                continue

            saved = False
            for attempt in range(4):
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=90000)
                    page.wait_for_timeout(1000)
                    html = patch_html(page.content())
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(html, encoding="utf-8")
                    static_paths |= collect_static_paths(html)
                    for link in extract_links(html):
                        if link not in done and is_page_url(link):
                            todo.add(link)
                    done.add(url)
                    saved = True
                    log(f"OK [{len(done)}] {dest.relative_to(PUBLIC)} (todo={len(todo)})")
                    break
                except Exception as e:
                    if attempt == 3:
                        fail.append((url, str(e)[:120]))
                        log(f"FAIL {url} -> {e}")
                    else:
                        time.sleep(2 * (attempt + 1))

        log("Downloading static assets...")
        asset_ok = 0
        all_static = static_paths.copy()
        for html in safe_rglob_html():
            try:
                all_static |= collect_static_paths(html.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                pass

        for rel in sorted(all_static):
            dest = PUBLIC / rel.lstrip("/")
            if dest.exists() and dest.stat().st_size > 50:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                resp = ctx.request.get(BASE + rel, timeout=120000)
                if resp.ok:
                    dest.write_bytes(resp.body())
                    asset_ok += 1
            except Exception:
                pass
        browser.close()

    cleanup_bad_pages()
    html_count = len(safe_rglob_html())
    report = (
        f"pages_ok={len(done)}\n"
        f"pages_fail={len(fail)}\n"
        f"assets={asset_ok}\n"
        f"html_files={html_count}\n"
    )
    REPORT.write_text(report, encoding="utf-8")
    log(report)
    if fail:
        for u, e in fail[:30]:
            log(f"FAIL {u} {e}")


if __name__ == "__main__":
    mirror_site()
