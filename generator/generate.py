#!/usr/bin/env python3
"""
UwU GF — generative NFT engine  ⊹ ࣪ ˖ (◍•ᴗ•◍)♡ ˖ ࣪ ⊹

Reads generator/traits.config.json and produces:
  images/<id>.png            layered artwork (or labelled placeholders)
  metadata/<id>.json         OpenSea-standard metadata (one file per token)
  metadata/_all.json         every token's metadata in one array
  metadata/rarity.csv        rarity score + rank per token
  metadata/provenance.json   sha256 provenance record (proves no post-hoc swap)
  images/_contact_sheet.png  montage for quick visual QA

Run the FULL pipeline today with placeholders (no art needed):
    python generator/generate.py --placeholder --count 50

Once art is synced into art/layers/ (see scripts/ + build_config.py --scan):
    python generator/build_config.py --scan
    python generator/generate.py --count 6969 --only-available

Flags:
    --count N         how many to generate (default = collection supply)
    --start N         first token id (default 1)
    --seed N          RNG seed for reproducible runs (default 6969)
    --size N          output px (default = config image_size)
    --placeholder     ignore art, draw labelled placeholders
    --only-available  only roll traits whose art_done == true
    --no-contact      skip the contact sheet
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  pip install -r generator/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "generator" / "traits.config.json"
IMG_DIR = ROOT / "images"
META_DIR = ROOT / "metadata"
ART = ROOT / "art" / "layers"

_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]


def load_font(size: int):
    for p in _FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def pastel(name: str) -> tuple[int, int, int]:
    """Deterministic kawaii pastel colour from a trait name."""
    h = hashlib.md5(name.encode()).digest()
    # mix toward white for that soft uwu look
    return tuple(160 + (b % 96) for b in h[:3])  # type: ignore


def weighted_choice(rng: random.Random, options: list[dict], none_weight: int):
    """Pick one option (or None) by weight. Returns option dict or None."""
    pool = list(options)
    weights = [o["weight"] for o in options]
    if none_weight > 0:
        pool.append(None)
        weights.append(none_weight)
    return rng.choices(pool, weights=weights, k=1)[0]


def roll_dna(rng: random.Random, layers: dict, only_available: bool):
    """Return ordered list of (folder, category, option_or_None)."""
    dna = []
    for folder, cfg in layers.items():
        opts = cfg["options"]
        if only_available:
            opts = [o for o in opts if o.get("art_done")]
        if not opts:                       # nothing drawable in this layer yet
            if cfg["required"] and not only_available:
                pass                       # fall through -> placeholder
            dna.append((folder, cfg["category"], None))
            continue
        choice = weighted_choice(rng, opts, cfg["none_weight"] if not cfg["required"] else 0)
        dna.append((folder, cfg["category"], choice))
    return dna


def dna_hash(dna) -> str:
    key = "|".join(f"{cat}:{(opt['name'] if opt else 'None')}" for _, cat, opt in dna)
    return hashlib.sha1(key.encode()).hexdigest()


def draw_placeholder_layer(base: Image.Image, category: str, name: str, size: int):
    """Rough face-shaped blocks so placeholder tokens look distinct & layered."""
    d = ImageDraw.Draw(base)
    c = pastel(name)
    s = size
    if category == "Background":
        d.rectangle([0, 0, s, s], fill=c)
    elif category == "Skin":
        d.ellipse([s * 0.18, s * 0.12, s * 0.82, s * 0.78], fill=c)          # head
    elif category == "Hoodie":
        d.rounded_rectangle([s * 0.12, s * 0.66, s * 0.88, s], radius=s * 0.08, fill=c)  # body
    elif category == "Hair":
        d.pieslice([s * 0.14, s * 0.06, s * 0.86, s * 0.62], 180, 360, fill=c)  # bangs
    elif category == "Eyes":
        for cx in (0.38, 0.62):
            d.ellipse([s * (cx - 0.06), s * 0.36, s * (cx + 0.06), s * 0.47], fill=c)
    elif category == "Mouth":
        d.rounded_rectangle([s * 0.43, s * 0.55, s * 0.57, s * 0.61], radius=s * 0.02, fill=c)
    elif category == "Make-up":
        for cx in (0.30, 0.70):
            d.ellipse([s * (cx - 0.05), s * 0.48, s * (cx + 0.05), s * 0.55], fill=c)  # cheeks
    elif category == "Choker":
        d.rectangle([s * 0.34, s * 0.74, s * 0.66, s * 0.79], fill=c)
    elif category == "Stuffie":
        d.ellipse([s * 0.70, s * 0.74, s * 0.93, s * 0.97], fill=c)          # held plushie
    else:
        d.rectangle([s * 0.4, s * 0.4, s * 0.6, s * 0.6], fill=c)


def render(dna, size: int, placeholder: bool):
    base = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    legend = []
    for folder, category, opt in dna:
        if opt is None:
            continue
        legend.append((category, opt["name"]))
        art_path = None
        if not placeholder and opt.get("file"):
            p = ART / folder / opt["file"]
            if p.exists():
                art_path = p
        if art_path:
            layer = Image.open(art_path).convert("RGBA")
            if layer.size != (size, size):
                layer = layer.resize((size, size), Image.LANCZOS)
            base = Image.alpha_composite(base, layer)
        else:
            draw_placeholder_layer(base, category, opt["name"], size)
    if placeholder:
        _draw_legend(base, legend, size)
    return base


def _draw_legend(base: Image.Image, legend, size: int):
    d = ImageDraw.Draw(base)
    font = load_font(max(14, size // 64))
    pad = size // 50
    lines = [f"{c}: {n}" for c, n in legend]
    lh = font.size + 6
    box_h = lh * len(lines) + pad
    d.rectangle([0, size - box_h, size, size], fill=(20, 12, 24, 180))
    for i, line in enumerate(lines):
        d.text((pad, size - box_h + pad // 2 + i * lh), line, fill=(255, 230, 245), font=font)


def build_metadata(token_id: int, dna, collection: dict) -> dict:
    attrs = [{"trait_type": cat, "value": opt["name"]} for _, cat, opt in dna if opt]
    return {
        "name": f"{collection['name']} #{token_id}",
        "description": collection["description"],
        "image": f"ipfs://__IMAGES_CID__/{token_id}.png",   # rewritten at IPFS upload
        "external_url": f"{collection['external_url']}/gf/{token_id}",
        "edition": token_id,
        "dna": dna_hash(dna),
        "attributes": attrs,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--seed", type=int, default=6969)
    ap.add_argument("--size", type=int)
    ap.add_argument("--placeholder", action="store_true")
    ap.add_argument("--only-available", action="store_true")
    ap.add_argument("--no-contact", action="store_true")
    args = ap.parse_args()

    if not CONFIG.exists():
        sys.exit("Missing config. Run:  python generator/build_config.py --scan")
    config = json.loads(CONFIG.read_text())
    collection = config["collection"]
    layers = config["layers"]
    size = args.size or collection["image_size"]
    count = args.count or collection["supply"]
    rng = random.Random(args.seed)

    IMG_DIR.mkdir(exist_ok=True)
    META_DIR.mkdir(exist_ok=True)

    print(f"♡ generating {count} UwU GFs @ {size}px "
          f"({'placeholder' if args.placeholder else 'art'} mode, seed {args.seed})")

    seen: set[str] = set()
    all_meta: list[dict] = []
    image_hashes: list[str] = []
    thumbs: list[Image.Image] = []
    MAX_RETRIES = 50

    tid = args.start
    made = 0
    while made < count:
        dna = roll_dna(rng, layers, args.only_available)
        h = dna_hash(dna)
        retries = 0
        while h in seen and retries < MAX_RETRIES:
            dna = roll_dna(rng, layers, args.only_available)
            h = dna_hash(dna)
            retries += 1
        if h in seen:
            print(f"⚠ exhausted unique combos after {made}. "
                  f"Add traits or lower --count.")
            break
        seen.add(h)

        img = render(dna, size, args.placeholder)
        out = IMG_DIR / f"{tid}.png"
        img.convert("RGBA").save(out)
        image_hashes.append(hashlib.sha256(out.read_bytes()).hexdigest())

        meta = build_metadata(tid, dna, collection)
        (META_DIR / f"{tid}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        all_meta.append(meta)

        if not args.no_contact and len(thumbs) < 100:
            thumbs.append(img.convert("RGB").resize((200, 200), Image.LANCZOS))

        made += 1
        tid += 1
        if made % 250 == 0:
            print(f"  ...{made}/{count}")

    # ---- rarity scoring (trait rarity = 1 / frequency; token score = sum) ----
    freq: dict[str, int] = {}
    for m in all_meta:
        for a in m["attributes"]:
            freq[f"{a['trait_type']}:{a['value']}"] = freq.get(f"{a['trait_type']}:{a['value']}", 0) + 1
    n = len(all_meta) or 1
    scored = []
    for m in all_meta:
        score = sum(n / freq[f"{a['trait_type']}:{a['value']}"] for a in m["attributes"])
        scored.append((m["edition"], round(score, 2), len(m["attributes"])))
    scored.sort(key=lambda x: x[1], reverse=True)

    rarity_csv = ["token_id,rarity_score,trait_count,rank"]
    for rank, (eid, score, tc) in enumerate(scored, start=1):
        rarity_csv.append(f"{eid},{score},{tc},{rank}")
    (META_DIR / "rarity.csv").write_text("\n".join(rarity_csv))
    (META_DIR / "_all.json").write_text(json.dumps(all_meta, indent=2, ensure_ascii=False))

    provenance = hashlib.sha256("".join(image_hashes).encode()).hexdigest()
    (META_DIR / "provenance.json").write_text(json.dumps({
        "collection": collection["name"],
        "count": made,
        "seed": args.seed,
        "combined_provenance_hash": provenance,
        "image_hashes": image_hashes,
    }, indent=2))

    if thumbs and not args.no_contact:
        cols = 10
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 200, rows * 200), (255, 245, 250))
        for i, t in enumerate(thumbs):
            sheet.paste(t, ((i % cols) * 200, (i // cols) * 200))
        sheet.save(IMG_DIR / "_contact_sheet.png")

    print(f"✓ {made} tokens -> images/ + metadata/")
    print(f"✓ rarity.csv, _all.json, provenance.json written")
    print(f"  provenance hash: {provenance[:24]}…")
    if thumbs and not args.no_contact:
        print(f"✓ images/_contact_sheet.png ({len(thumbs)} preview)")


if __name__ == "__main__":
    main()
