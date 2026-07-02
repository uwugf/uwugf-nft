#!/usr/bin/env python3
"""
UwU GF — trait spec -> config + worksheet builder  (｡♥‿♥｡)

Single source of truth for the collection's traits, transcribed from the team
trait sheet in Google Drive. Run this to (re)generate:

  - generator/traits.config.json   machine config consumed by generate.py
  - data/traits_master.csv         human-editable worksheet (opens in Excel/Sheets)

If real layer art exists under art/layers/<NN_Category>/, the script also scans
it to attach real source filenames and infer rarity tiers from
common/ rare/ super_rare/ legendary/ subfolders (overriding the defaults below).

Usage:
    python generator/build_config.py
    python generator/build_config.py --scan    # also scan art/layers for files
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art" / "layers"
CONFIG_OUT = ROOT / "generator" / "traits.config.json"
CSV_OUT = ROOT / "data" / "traits_master.csv"

# Relative weight per rarity tier (higher = appears more often). Tune to taste.
TIER_WEIGHTS = {"common": 100, "rare": 30, "super_rare": 10, "legendary": 3}

COLLECTION = {
    "name": "UwU GF",
    "symbol": "UWUGF",
    "description": (
        "6969 hand-drawn UwU girlfriends living rent-free on the blockchain. "
        "she's cute, she's degen, she's your exit liquidity (jk... unless?) ♡"
    ),
    "supply": 6969,
    "image_size": 1080,        # px, square (matches source art native res)
    "external_url": "https://uwugf.xyz",
    "royalty_bps": 690,         # 6.9% creator royalty (ERC-2981)
}

# Compositing order, bottom -> top. VERIFY against the real art once synced.
#   folder, category label, required?, none_weight (relative weight of "no trait"
#   for optional layers; 0 => always present)
LAYERS = [
    ("01_Background", "Background", True,  0),
    ("02_Skin",       "Skin",       True,  0),
    ("07_Makeup",     "Make-up",    False, 70),
    ("05_Mouth",      "Mouth",      True,  0),
    ("06_Eyes",       "Eyes",       True,  0),
    ("08_Hair",       "Hair",       True,  0),
    ("04_Choker",     "Choker",     False, 40),
    ("03_Hoodie",     "Hoodie",     True,  0),   # hood is the top layer -> frames the face
    ("09_Stuffie",    "Stuffie",    False, 80),
]

# Trait spec transcribed from the team sheet.
#   done:     category-level art status (TRUE/FALSE column on the sheet)
#   traits:   ordered list of trait names (Background order == 1.png..15.png)
#   tiers:    per-trait rarity overrides (default = "common"). STARTING POINTS.
#   not_done: traits whose art isn't finished yet (overrides category `done`)
SPEC: dict[str, dict] = {
    "Background": {
        "done": True,
        "numbered_files": True,  # current files are 1.png .. 15.png in this order
        "traits": [
            "Asylum", "Haunted House", "Chinese Restaurant", "Casino", "School",
            "Sunflower Field", "Nightclub", "Rainbow Sky", "Pink Cafe", "Unicorn Cafe",
            "Wedding Arch", "Candy Shop", "Playground", "Pub", "Library",
        ],
        "tiers": {"Rainbow Sky": "super_rare", "Unicorn Cafe": "super_rare", "Casino": "rare"},
    },
    "Skin": {
        "done": True,
        "traits": ["Pale", "Pale Ivory", "Ivory", "Porcelain", "Sienna", "Limestone", "Espresso", "Zombie"],
        "tiers": {"Zombie": "super_rare"},
    },
    "Eyes": {
        "done": True,
        "traits": [
            "Bright-Green", "Bright-Blue", "Bright-Brown", "Bright-Gold",
            "Bright-Heart-Green", "Bright-Heart-Blue", "Bright-Heart-Brown", "Bright-Heart-Gold",
            "Dead", "Alien", "Ghost", "Dazed",
            "Rolling-Green", "Rolling-Blue", "Rolling-Brown", "Rolling-Gold",
            "SideEye-Green", "SideEye-Blue", "SideEye-Brown", "SideEye-Gold",
            "Diamonds", "Sniper", "Lucky", "Uwu",
        ],
        "tiers": {
            "Uwu": "legendary", "Diamonds": "legendary",
            "Alien": "super_rare", "Ghost": "super_rare", "Sniper": "super_rare", "Lucky": "super_rare",
            "Dead": "rare", "Dazed": "rare",
            "SideEye-Green": "rare", "SideEye-Blue": "rare", "SideEye-Brown": "rare", "SideEye-Gold": "rare",
        },
    },
    "Mouth": {
        "done": True,   # lives in the "Lips" folder on Drive
        "traits": [
            "Straight Plump", "Smile", "Kiss", "Pout", "Angry", "Tongue", "Goth",
            "Smile with teeth", "Vampire", "Braces", "Lip bite", "Stitched mouth",
            "Vampire 2", "Bubblegum",
        ],
        "tiers": {
            "Vampire": "super_rare", "Vampire 2": "super_rare",
            "Goth": "rare", "Stitched mouth": "rare", "Braces": "rare",
        },
    },
    "Make-up": {
        "done": True,   # uploaded to Drive "Make Up" folder 2026-07-02
        "traits": ["Retardio", "Bowie", "Kiss", "Harley Quinn", "Heart Cheeks", "Mime"],
        "tiers": {"Harley Quinn": "rare", "Mime": "rare", "Bowie": "rare"},
    },
    "Choker": {
        "done": True,
        "traits": ["Heart Choker", "UWU Choker", "Star Choker", "XX Choker"],
        "tiers": {},
    },
    "Hair": {
        "done": True,   # all 18 uploaded to Drive 2026-07-02 ("done with all hair")
        # actual drawn set is 18 (sheet had 15): Full Bangs Red replaces the planned
        # Blonde, plus extra Curtain Bangs Blue/Pink/Purple.
        "traits": [
            "Bangs Black", "Bangs Blonde", "Bangs Brown", "Bangs Pink", "Bangs Purple",
            "Full Bangs Black", "Full Bangs Blue", "Full Bangs Brown", "Full Bangs Orange", "Full Bangs Red",
            "Curtain Bangs Black", "Curtain Bangs Blonde", "Curtain Bangs Blue", "Curtain Bangs Brown",
            "Curtain Bangs Green", "Curtain Bangs Pink", "Curtain Bangs Purple", "Curtain Bangs Red",
        ],
        # natural shades common; fashion colors rare (starting points, tune in sheet)
        "tiers": {
            "Bangs Pink": "rare", "Bangs Purple": "rare",
            "Full Bangs Blue": "rare", "Full Bangs Orange": "rare", "Full Bangs Red": "rare",
            "Curtain Bangs Blue": "rare", "Curtain Bangs Green": "rare",
            "Curtain Bangs Pink": "rare", "Curtain Bangs Purple": "rare", "Curtain Bangs Red": "rare",
        },
    },
    "Hoodie": {
        "done": True,
        # 16 drawn hoodies, names re-verified against the art one-by-one (2026-07-02):
        # the sheet's original Og Violet + Joker DO exist (earlier fc_XX renaming had
        # scrambled them). Solana/Weed/Uwu dropped per babydegen; Pepe Suit replaces
        # them (gab drawing it).
        "traits": [
            "Og White", "Og Neon Pink", "Og Red", "Og Yellow", "Og Neon Green", "Og Violet",
            "Tangerine", "Joker",
            "Fuzzy Pink", "Fuzzy Purple", "Fuzzy Periwinkle", "Stars Purple", "Stars Blue", "Clouds",
            "Black & Gold", "Rainbow",
            "Pepe Suit",  # pending art (gab)
        ],
        "tiers": {
            "Rainbow": "legendary", "Black & Gold": "legendary",
            "Fuzzy Pink": "super_rare", "Fuzzy Purple": "super_rare", "Fuzzy Periwinkle": "super_rare",
            "Stars Purple": "super_rare", "Stars Blue": "super_rare", "Clouds": "super_rare",
            "Joker": "rare", "Pepe Suit": "rare",
        },
        "not_done": ["Pepe Suit"],
    },
    "Stuffie": {
        "done": False,  # all FALSE on sheet — art not drawn yet
        "traits": ["Nub", "Pepe", "Wif", "Teddy Bear", "Voodoo Doll"],
        "tiers": {"Voodoo Doll": "rare", "Pepe": "rare"},
    },
}

# 1/1 specials (hand-built, not part of the generative roll). Tracked here for
# planning; minted from a reserved range. KOL handles are whitelist/collab notes.
ONE_OF_ONES = [
    "EXIT LIQUIDITY", "PUNK", "PUDGY", "OPENSEA", "HARRY POTTER", "DEGEN",
    "WHALE", "MCDO", "GRADUATION", "GEISHA", "DUBAI CHOCOLATE", "SPIDERMAN",
]
KOLS = [
    "https://x.com/jerezizzz", "https://x.com/breyonchain", "https://x.com/Tma_420",
    "https://x.com/CryptoGorilla", "https://x.com/CrypSaf", "https://x.com/BR4ted",
    "https://x.com/crypto_czar_eth",
]

TIER_DIRS = {"common", "rare", "super_rare", "legendary"}


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def scan_art(category_folder: str) -> dict[str, dict]:
    """Return {slug(trait): {file, tier}} discovered under art/layers/<folder>/."""
    found: dict[str, dict] = {}
    base = ART / category_folder
    if not base.is_dir():
        return found
    # flat PNGs (tier = common)
    for p in sorted(base.glob("*.png")):
        found[_slug(p.stem)] = {"file": p.name, "tier": "common", "path": str(p.relative_to(ROOT))}
    # tier subfolders
    for tier in TIER_DIRS:
        sub = base / tier
        if sub.is_dir():
            for p in sorted(sub.glob("*.png")):
                found[_slug(p.stem)] = {"file": f"{tier}/{p.name}", "tier": tier, "path": str(p.relative_to(ROOT))}
    return found


def build(scan: bool = False):
    layers_cfg: dict[str, dict] = {}
    rows: list[dict] = []

    for idx, (folder, label, required, none_weight) in enumerate(LAYERS, start=1):
        spec = SPEC[label]
        traits = spec["traits"]
        tiers = spec.get("tiers", {})
        not_done = set(spec.get("not_done", []))
        cat_done = spec["done"]
        numbered = spec.get("numbered_files", False)
        scanned = scan_art(folder) if scan else {}

        options = []
        for i, name in enumerate(traits, start=1):
            tier = tiers.get(name, "common")
            done = cat_done and name not in not_done
            src = ""
            if numbered:
                src = f"{i}.png"
            hit = scanned.get(_slug(name))
            if hit:                       # real art overrides defaults
                src, tier, done = hit["file"], hit["tier"], True
            weight = TIER_WEIGHTS[tier]
            options.append({
                "name": name, "file": src, "tier": tier,
                "weight": weight, "art_done": done,
            })
            rows.append({
                "layer_order": idx, "category": label, "trait_name": name,
                "source_file": src, "rarity_tier": tier, "weight": weight,
                "art_done": "TRUE" if done else "FALSE",
                "notes": "" if done else "art pending",
            })

        layers_cfg[folder] = {
            "category": label,
            "required": required,
            "none_weight": none_weight,
            "options": options,
        }

    config = {
        "collection": COLLECTION,
        "tier_weights": TIER_WEIGHTS,
        "layer_order": [f for f, *_ in LAYERS],
        "layers": layers_cfg,
        "one_of_ones": ONE_OF_ONES,
        "kols": KOLS,
    }

    CONFIG_OUT.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    with CSV_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "layer_order", "category", "trait_name", "source_file",
            "rarity_tier", "weight", "art_done", "notes",
        ])
        w.writeheader()
        w.writerows(rows)

    # quick summary
    done = sum(1 for r in rows if r["art_done"] == "TRUE")
    print(f"✓ wrote {CONFIG_OUT.relative_to(ROOT)}")
    print(f"✓ wrote {CSV_OUT.relative_to(ROOT)}")
    print(f"  {len(rows)} generative traits across {len(LAYERS)} layers "
          f"({done} art-ready, {len(rows)-done} pending)")
    print(f"  + {len(ONE_OF_ONES)} one-of-ones, {len(KOLS)} KOL slots")
    combos = 1
    for folder, cfg in layers_cfg.items():
        n = sum(1 for o in cfg["options"] if o["art_done"]) or 1
        if cfg["none_weight"] > 0:
            n += 1
        combos *= n
    print(f"  art-ready combinatorial space ≈ {combos:,} (target supply {COLLECTION['supply']:,})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true", help="scan art/layers for real files + tiers")
    build(**vars(ap.parse_args()))
