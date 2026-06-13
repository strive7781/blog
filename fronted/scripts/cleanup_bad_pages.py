import os
import re
import shutil
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

BAD_PREFIXES = ("assets/", "img/", "css/", "js/", "live2dw/")
BAD_PATTERNS = (
    re.compile(r"%[0-9A-Fa-f]{2}"),  # URL-encoded anchor slugs
    re.compile(r"[≤≥<>=]"),           # heading anchor fragments
    re.compile(r"\s"),                # spaces in path
)


def is_bad_page(rel: str) -> bool:
    if rel == "index.html":
        return False
    lower = rel.lower()
    for p in BAD_PREFIXES:
        if lower.startswith(p):
            return True
    # article/heading anchor: YYYY/MM/DD/slug/subslug/index.html where subslug is weird
    parts = lower.split("/")
    if len(parts) >= 5 and parts[0].isdigit():
        sub = parts[4] if len(parts) > 4 else ""
        for pat in BAD_PATTERNS:
            if pat.search(sub):
                return True
    if "assets/" in lower and lower.endswith("/index.html"):
        return True
    return False


def cleanup():
    removed = 0
    for dirpath, dirnames, filenames in os.walk(PUBLIC):
        if "index.html" not in filenames:
            continue
        html = Path(dirpath) / "index.html"
        rel = html.relative_to(PUBLIC).as_posix()
        if is_bad_page(rel):
            try:
                shutil.rmtree(dirpath)
                removed += 1
                print("removed", rel)
            except Exception as e:
                print("err", rel, e)
    print(f"total removed: {removed}")


if __name__ == "__main__":
    cleanup()
