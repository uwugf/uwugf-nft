#!/usr/bin/env python3
"""
Pull the 15 finished Background layers from Drive and name them by trait.

Backgrounds are the one fully-finished, clean layer set, so this gets you a
real layer to test the generator with. Everything else needs the artist to
finish + export isolated transparent PNGs (see docs/SYNC_ART.md + ART_STATUS.md).

Requires gdown:   pip install gdown
Run:              python scripts/pull_backgrounds.py
Output:           art/layers/01_Background/<Trait Name>.png
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "scripts" / "drive_manifest.json"
DEST = ROOT / "art" / "layers" / "01_Background"

try:
    import gdown  # noqa: F401
except ImportError:
    sys.exit("gdown not installed.  pip install gdown   (then re-run)")

DEST.mkdir(parents=True, exist_ok=True)
bg = json.loads(MANIFEST.read_text())["backgrounds"]
print(f"♡ pulling {len(bg)} backgrounds into {DEST.relative_to(ROOT)}/")
for b in bg:
    out = DEST / f"{b['name']}.png"
    if out.exists():
        print(f"  · {b['name']} (exists, skipping)")
        continue
    url = f"https://drive.google.com/uc?id={b['id']}"
    try:
        gdown.download(url, str(out), quiet=True)
        ok = out.exists() and out.stat().st_size > 1000
    except Exception:
        ok = False
    print(f"  {'✓' if ok else '✗'} {b['name']}")
print("done. now run:  python generator/build_config.py --scan")
