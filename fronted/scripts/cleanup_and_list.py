import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

# Remove accidentally downloaded HTML pages saved without extension
for p in PUBLIC.rglob("*"):
    if p.is_file() and p.suffix == "" and p.name not in ("CNAME",):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")[:200]
            if "<!DOCTYPE html>" in text or "<html" in text:
                p.unlink()
                print("removed", p)
        except Exception:
            pass

html = (PUBLIC / "index.html").read_text(encoding="utf-8")
scripts = sorted(set(re.findall(r'src="([^"]+)"', html)))
print("Scripts:")
for s in scripts:
    print(s)
