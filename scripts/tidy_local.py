#!/usr/bin/env python3
"""
Tidy + QA the local art/layers tree before a real generation run.

  - deletes macOS junk (.DS_Store) anywhere under art/
  - reports every PNG's dimensions / colour mode / alpha
  - FLAGS anything that will break a clean composite:
      • not square            (layers must share one square canvas)
      • inconsistent size     (all layers should match, e.g. 2000x2000)
      • no alpha channel      (non-background layers need transparency)

Run:  python scripts/tidy_local.py
"""
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow needed:  pip install -r generator/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art"
LAYERS = ART / "layers"

# remove junk
junk = list(ART.rglob(".DS_Store"))
for j in junk:
    j.unlink()
if junk:
    print(f"🧹 removed {len(junk)} .DS_Store file(s)")

if not LAYERS.exists():
    raise SystemExit("no art/layers yet — sync art first (see docs/SYNC_ART.md)")

sizes = Counter()
flags = []
total = 0
for layer_dir in sorted(p for p in LAYERS.iterdir() if p.is_dir()):
    pngs = list(layer_dir.rglob("*.png"))
    if not pngs:
        continue
    print(f"\n▸ {layer_dir.name}  ({len(pngs)} png)")
    is_bg = "Background" in layer_dir.name
    for p in sorted(pngs):
        total += 1
        with Image.open(p) as im:
            w, h = im.size
            mode = im.mode
            has_alpha = mode in ("RGBA", "LA") or "transparency" in im.info
        sizes[(w, h)] += 1
        rel = p.relative_to(LAYERS)
        problems = []
        if w != h:
            problems.append("NOT SQUARE")
        if not has_alpha and not is_bg:
            problems.append("NO ALPHA")
        tag = "  ⚠ " + ", ".join(problems) if problems else ""
        if problems:
            flags.append(f"{rel}: {', '.join(problems)}")
        print(f"   {rel}  {w}x{h} {mode}{tag}")

print(f"\n── summary ──  {total} layer png(s)")
if len(sizes) > 1:
    print("⚠ MULTIPLE canvas sizes (layers must all match):")
    for (w, h), n in sizes.most_common():
        print(f"    {w}x{h}: {n}")
else:
    for (w, h), n in sizes.items():
        print(f"✓ all {n} layers are {w}x{h}")
if flags:
    print(f"⚠ {len(flags)} file(s) need fixing before a clean run.")
else:
    print("✓ no problems — ready to generate ♡")
