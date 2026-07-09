#!/usr/bin/env python3
"""Color-harmony logic for the UwU GF generator.

Every trait PNG is analyzed once (dominant hue, saturation, pastel-ness,
multi-color detection) into palette.json. harmony_score() rates any trait
combo 0..1 using color-wheel relationships between the layers that visually
interact (hoodie <-> background <-> hair, plus colorful skins/makeup).
roll_harmonious() keeps the weighted-rarity roll but rejection-samples until
a combo clears the aesthetic threshold, so rarity stays intact while clashy
combos (e.g. saturated red hoodie on saturated green bg) never mint.

CLI:
  python generator/harmony.py --analyze          rebuild palette.json
  python generator/harmony.py --classify         print per-trait classification
  python generator/harmony.py --sample 12        render sample grid of accepted rolls
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import random
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art" / "layers"
CONFIG = ROOT / "generator" / "traits.config.json"
PALETTE = ROOT / "generator" / "palette.json"

# names we KNOW are neutral no matter what the pixels say (natural hair reads
# slightly warm; skin tones must never participate in hue scoring)
FORCE_NEUTRAL = {
    "Hair": {"Bangs Black", "Bangs Blonde", "Bangs Brown",
             "Full Bangs Black", "Full Bangs Brown",
             "Curtain Bangs Black", "Curtain Bangs Blonde", "Curtain Bangs Brown"},
    "Skin": {"Pale", "Pale Ivory", "Ivory", "Porcelain", "Sienna", "Limestone", "Espresso"},
}

# how much each pairing matters to the final score (hood + bg dominate the canvas)
PAIR_WEIGHTS = [
    (("Hoodie", "Background"), 0.40),
    (("Hair",   "Hoodie"),     0.30),
    (("Hair",   "Background"), 0.15),
    (("Skin",   "Hoodie"),     0.15),   # only scores when skin is colorful (Zombie)
]

ACCEPT = 0.85          # accept a roll at/above this score (max floor that keeps every trait mintable)
MAX_TRIES = 50         # rejection-sampling budget; then best-seen wins

# ── stylist rule: sunglasses only ride on plain, everyday eyes ──────────────
# Every "statement" eye (hearts, diamonds, side-eye, alien, ghost, dead, dazed,
# sniper, lucky, uwu) IS the gf — the stylist refuses to hide them behind shades.
# So glasses are only allowed on the standard open eyes: Bright-<color> and
# Rolling-<color>. This is an ALLOW-LIST (not tier-based, since --scan flattens
# tiers): any eye that isn't plainly one of these can never wear glasses, and a
# new/unknown eye fails safe to "no glasses". Hoodie still composites above glasses.
import re as _re
GLASSES_OK_EYE = _re.compile(r"^(Bright|Rolling)-(Green|Blue|Brown|Gold)$")

def glasses_allowed_on(eye_name: str | None) -> bool:
    return bool(eye_name and GLASSES_OK_EYE.match(eye_name))


# ---------------------------------------------------------------- analysis --

def _analyze_png(path: Path, is_bg: bool) -> dict:
    im = Image.open(path).convert("RGBA")
    im.thumbnail((196, 196))
    px = list(im.getdata())
    hist = [0.0] * 12                     # 30-degree hue buckets, weighted by s*v
    sat_sum = val_sum = colorful = opaque = 0.0
    for r, g, b, a in px:
        if a < 200 and not is_bg:
            continue
        opaque += 1
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        sat_sum += s
        val_sum += v
        if s > 0.25 and v > 0.18:
            colorful += 1
            hist[int(h * 12) % 12] += s * v
    if not opaque:
        return {"neutral": True, "hue": None, "sat": 0, "multi": False, "pastel": True}
    mean_sat = sat_sum / opaque
    colorful_frac = colorful / opaque
    total = sum(hist) or 1.0
    strong = [i for i, w in enumerate(hist) if w / total > 0.16]
    # circular weighted mean of the dominant bucket neighborhood
    best = max(range(12), key=lambda i: hist[i])
    ang_x = sum(w * math.cos(math.radians(i * 30 + 15)) for i, w in enumerate(hist))
    ang_y = sum(w * math.sin(math.radians(i * 30 + 15)) for i, w in enumerate(hist))
    hue = (math.degrees(math.atan2(ang_y, ang_x)) % 360) if total > 0 else None
    # multi-color = several well-separated strong buckets (rainbow, tie-dye)
    multi = len(strong) >= 3
    if multi:  # circular mean is meaningless for rainbows
        hue = None
    neutral = colorful_frac < 0.18 or mean_sat < 0.16
    # mean saturation of the COLORFUL pixels tells pastel vs neon
    col_sat = (sum(hist) / max(colorful, 1)) if colorful else 0
    pastel = mean_sat < 0.45 if not neutral else True
    return {
        "neutral": bool(neutral and not multi),
        "hue": None if neutral else hue,
        "sat": round(mean_sat, 3),
        "multi": bool(multi),
        "pastel": bool(pastel),
        "dom_bucket": best,
    }


def analyze(write: bool = True) -> dict:
    cfg = json.loads(CONFIG.read_text())
    pal: dict[str, dict] = {}
    for folder, layer in cfg["layers"].items():
        cat = layer["category"]
        is_bg = cat == "Background"
        for o in layer["options"]:
            if not o.get("file"):
                continue
            p = ART / folder / o["file"]
            if not p.exists():
                continue
            info = _analyze_png(p, is_bg)
            if o["name"] in FORCE_NEUTRAL.get(cat, set()):
                info.update({"neutral": True, "hue": None, "multi": False})
            pal[f"{cat}/{o['name']}"] = info
    if write:
        PALETTE.write_text(json.dumps(pal, indent=1))
    return pal


# ----------------------------------------------------------------- scoring --

def _pair_score(a: dict, b: dict) -> float:
    """Harmony of two trait palettes on the color wheel."""
    if a["neutral"] or b["neutral"]:
        return 0.85                                   # neutrals go with anything
    if a["multi"] or b["multi"]:
        other = b if a["multi"] else a
        if a["multi"] and b["multi"]:
            return 0.50                               # two rainbows fight
        return 0.80 if other.get("pastel") else 0.60  # rainbow likes calm partners
    d = abs(a["hue"] - b["hue"])
    d = min(d, 360 - d)
    both_soft = a["pastel"] and b["pastel"]
    if d <= 35:   base = 0.95                         # analogous / tonal
    elif d <= 70: base = 0.72                         # neighbors (pink+purple etc.)
    elif d < 150: base = 0.42                         # the awkward zone
    else:         base = 0.85                         # complementary pop
    if both_soft:                                     # pastels forgive everything
        base = max(base, 0.70)
    return base


def harmony_score(combo: dict[str, str], pal: dict) -> float:
    """combo: {category: trait_name}. Returns 0..1."""
    def info(cat):
        name = combo.get(cat)
        return pal.get(f"{cat}/{name}") if name else None
    total = weight = 0.0
    for (ca, cb), w in PAIR_WEIGHTS:
        a, b = info(ca), info(cb)
        if a is None or b is None:
            continue
        if ca == "Skin" and a["neutral"]:
            continue                                   # natural skins don't vote
        total += _pair_score(a, b) * w
        weight += w
    # loud makeup on a loud hoodie is a lot — nudge, don't veto
    mk, hd = info("Make-up"), info("Hoodie")
    if mk and hd and not mk["neutral"] and not mk["multi"] and not hd["neutral"] and not hd.get("pastel"):
        total += _pair_score(mk, hd) * 0.10
        weight += 0.10
    # shades are small but a loud frame shouldn't fight a loud hood — gentle nudge
    sg = info("Sunglasses")
    if sg and hd and not sg["neutral"] and not sg["multi"] and not hd["neutral"]:
        total += _pair_score(sg, hd) * 0.08
        weight += 0.08
    return total / weight if weight else 1.0


# ------------------------------------------------------------------ rolling --

def load_layers():
    cfg = json.loads(CONFIG.read_text())
    return cfg["layers"], cfg


def roll_once(rng: random.Random, layers: dict) -> dict[str, tuple]:
    """One weighted roll over traits whose art exists. {cat: (folder, option)}"""
    out = {}
    for folder, c in layers.items():
        opts = [o for o in c["options"] if o.get("file") and (ART / folder / o["file"]).exists()]
        if not opts:
            continue
        pool: list = list(opts)
        weights = [o["weight"] for o in opts]
        if not c["required"]:
            pool.append(None)
            weights.append(c.get("none_weight", 0))
        pick = rng.choices(pool, weights=weights, k=1)[0]
        if pick is not None:
            out[c["category"]] = (folder, pick)
    # stylist rule: shades only ride on plain eyes; statement eyes stay visible
    if "Sunglasses" in out:
        eye = out["Eyes"][1]["name"] if "Eyes" in out else None
        if not glasses_allowed_on(eye):
            del out["Sunglasses"]
    return out


def roll_harmonious(rng: random.Random, layers: dict, pal: dict,
                    accept: float = ACCEPT, max_tries: int = MAX_TRIES):
    """Weighted roll, re-rolled until the combo clears the harmony bar."""
    best, best_score = None, -1.0
    for _ in range(max_tries):
        combo = roll_once(rng, layers)
        score = harmony_score({c: o["name"] for c, (f, o) in combo.items()}, pal)
        if score >= accept:
            return combo, score
        if score > best_score:
            best, best_score = combo, score
    return best, best_score


def render(combo: dict, size: int = 1080) -> Image.Image:
    base = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    for cat, (folder, o) in combo.items():             # dict preserves layer order
        im = Image.open(ART / folder / o["file"]).convert("RGBA")
        if im.size != base.size:
            im = im.resize(base.size, Image.LANCZOS)
        base = Image.alpha_composite(base, im)
    return base.convert("RGB").resize((size, size), Image.LANCZOS)


# --------------------------------------------------------------------- cli --

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--classify", action="store_true")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    if args.analyze or not PALETTE.exists():
        pal = analyze()
        print(f"analyzed {len(pal)} traits -> {PALETTE.relative_to(ROOT)}")
    else:
        pal = json.loads(PALETTE.read_text())

    if args.classify:
        for k, v in pal.items():
            kind = "multi" if v["multi"] else ("neutral" if v["neutral"] else f"hue {v['hue']:.0f}")
            print(f"{k:45s} {kind:10s} sat={v['sat']:.2f} {'pastel' if v['pastel'] else 'LOUD'}")

    if args.sample:
        layers, _ = load_layers()
        rng = random.Random(args.seed)
        n = args.sample
        cols = 4
        cell = 340
        rows = (n + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * (cell + 26)), (250, 244, 250))
        from PIL import ImageDraw
        d = ImageDraw.Draw(sheet)
        for i in range(n):
            combo, score = roll_harmonious(rng, layers, pal)
            im = render(combo, cell)
            x, y = (i % cols) * cell, (i // cols) * (cell + 26)
            sheet.paste(im, (x, y))
            names = {c: o["name"] for c, (f, o) in combo.items()}
            d.text((x + 6, y + cell + 4),
                   f"{score:.2f}  {names.get('Hoodie','-')[:14]} / {names.get('Hair','-')[:16]}",
                   fill=(70, 40, 90))
            print(f"#{i+1} score={score:.2f} " +
                  "  ".join(f"{c}={o['name']}" for c, (f, o) in combo.items()))
        out = Path(args.out) if args.out else ROOT / "output" / "harmony_sample.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out)
        print(f"grid -> {out}")


if __name__ == "__main__":
    main()
