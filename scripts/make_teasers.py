#!/usr/bin/env python3
"""
Build website teaser images from real character composites + real backgrounds.
If a character PNG is transparent, drop it onto a themed background scene so the
teaser shows the FULL nft look. Output web-optimised jpgs into website/assets/.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BG = ROOT / "art" / "layers" / "01_Background"

# (character png, themed background trait)
PAIRS = [
    ("website/assets/peek-1.png", "Rainbow Sky"),   # purple fuzzy + diamond eyes + teddy
    ("website/assets/peek-2.png", "Casino"),        # white hoodie + harley makeup
    ("website/assets/peek-3.png", "Pink Cafe"),     # white hoodie + pink hair
]

for rel, bg_name in PAIRS:
    char_p = ROOT / rel
    char = Image.open(char_p).convert("RGBA")
    a = char.split()[-1]
    w, h = char.size
    corners = [a.getpixel(c) for c in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]]
    transparent = max(corners) < 24
    bg_p = BG / f"{bg_name}.png"
    if transparent and bg_p.exists():
        base = Image.open(bg_p).convert("RGBA").resize(char.size, Image.LANCZOS)
        note = f"on {bg_name}"
    else:
        base = Image.new("RGBA", char.size, (255, 238, 247, 255))  # soft pink card
        note = "on pink (not transparent)"
    comp = Image.alpha_composite(base, char).convert("RGB").resize((900, 900), Image.LANCZOS)
    out = char_p.with_suffix(".jpg")
    comp.save(out, quality=86, optimize=True)
    print(f"✓ {out.name}  {note}  (corner alpha {corners})")

# drop the big source pngs so the deploy stays light
for rel, _ in PAIRS:
    (ROOT / rel).unlink(missing_ok=True)
print("done — teasers in website/assets/*.jpg")
