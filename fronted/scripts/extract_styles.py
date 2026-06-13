import re
from pathlib import Path

html = Path(r"d:\JavaAfterEnd\blog\index.html").read_text(encoding="utf-8")

for style_id in ["themeColor", "defineBg", "rightSide", "transPercent", "blurNum", "settingStyle", "menu_shadow"]:
    m = re.search(rf'<style id="{style_id}">(.*?)</style>', html, re.DOTALL)
    if m:
        print(f"=== {style_id} ===")
        print(m.group(1)[:1200])
        print()
