# UwU GF — art status 🎨

Snapshot from the shared Drive ("uwu gf", owner babydegen.eth) + the trait sheet.
TRUE/FALSE = the artist's "done?" flag on the sheet. This is what the artist still
needs to finish before a clean 6969 generation.

## Per-layer status

| # | Layer | Traits | Drive folder? | Status | Notes |
|---|---|---|---|---|---|
| 01 | Background | 15 | ✅ `Background/` (1–15.png) | ✅ **DONE** | flat PNGs, our cleanest set |
| 02 | Skin | 8 | ✅ `Skin/` (rarity subfolders) | 🟨 in progress | confirm all 8 exported |
| 03 | Hoodie | ~16 (+3 pending) | 🟨 `Hoodies/` (7 composites) | 🟨 needs isolation | files look like **composites**, need isolated transparent hoodie layers |
| 04 | Choker | 4 | ✅ `Choker/` (rarity subfolders) | 🟨 in progress | |
| 05 | Mouth | 14 | ✅ `Lips/` (rarity subfolders) | 🟨 in progress | folder is named "Lips" |
| 06 | Eyes | 24 | ✅ `Eyes/` (rarity subfolders) | 🟨 in progress | biggest set, confirm all 24 |
| 07 | Make-up | 6 | ❌ none | ❌ **not drawn** | sheet says TRUE but no art folder |
| 08 | Hair | 15 | ❌ none | ❌ **not drawn** | all FALSE on sheet |
| 09 | Stuffie | 5 | ❌ none | ❌ **not drawn** | all FALSE on sheet |

**One-of-ones (12):** EXIT LIQUIDITY, PUNK, PUDGY, OPENSEA, HARRY POTTER, DEGEN,
WHALE, MCDO, GRADUATION, GEISHA, DUBAI CHOCOLATE, SPIDERMAN — hand-built, not part
of the generative roll; reserve token ids for them.

## What the artist needs to deliver (export spec)
For the generator to composite cleanly, every trait must be:
1. **One isolated PNG per trait** (not a flattened/composite canvas).
2. **Transparent background** (RGBA) — except the Background layer.
3. **Same square canvas for every layer**, ideally **2000×2000**, perfectly aligned
   (a GF's eyes must sit in the same spot across every eye PNG).
4. Named by trait, e.g. `Bright-Blue.png`, `Heart Choker.png` — or kept in the
   `common/ rare/ super_rare/ legendary/` subfolders (the generator reads tier
   from the subfolder automatically).

Drop them into `art/layers/<NN_Layer>/` (or the rarity subfolders), then:
```bash
python scripts/tidy_local.py            # QA: flags wrong size / missing alpha
python generator/build_config.py --scan # re-reads real files + tiers
```

## ⚠️ The Hoodie issue
The `Hoodies/` folder holds `Final_Canvas-*.png` that appear to be **full-character
composites**, not isolated hoodie layers. Compositing those would double-draw the
face/body. The artist should re-export hoodies as **transparent, body-only** layers
that align with the skin/face stack. Flagging early so it's not a launch-day surprise.

## Cleanup done / suggested
- `.DS_Store` junk is scattered through the Drive folders — `tidy_local.py` strips
  these locally. (Harmless, just messy.)
- Lots of `Untitled_Artwork (n).procreate` working files in the root — these are
  source files; keep in Drive, no need to sync locally.
