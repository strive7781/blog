from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://cyborg2077.github.io/", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(5000)

    styles = page.evaluate(
        """() => {
            const ids = ['themeColor','defineBg','rightSide','transPercent','blurNum','settingStyle','menu_shadow'];
            const out = {};
            ids.forEach(id => {
                const el = document.getElementById(id);
                out[id] = el ? el.innerHTML : '';
            });
            out.theme = document.documentElement.getAttribute('data-theme');
            out.cssVars = getComputedStyle(document.documentElement).getPropertyValue('--theme-color');
            const webBg = document.getElementById('web_bg');
            out.webBgStyle = webBg ? webBg.getAttribute('style') : '';
            return out;
        }"""
    )

    html = page.content()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (ROOT / "runtime-styles.txt").write_text(str(styles), encoding="utf-8")
    page.screenshot(path=str(ROOT / "crawl-output" / "final-render.png"), full_page=False)
    browser.close()

print(styles)
