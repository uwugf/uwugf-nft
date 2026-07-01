# Syncing art from Google Drive ⤵️

The art lives in the shared **"uwu gf"** Drive folder (owner: babydegen.eth).
Source `.procreate` files are big — you only need the **flattened trait PNGs**
locally. Two ways to pull them, easiest first.

## Option A — grab the finished Backgrounds now (gdown)
The 15 Backgrounds are done and clean, so you can pull them immediately and
test the generator on a real layer:
```bash
pip install gdown
python scripts/pull_backgrounds.py
# -> art/layers/01_Background/Asylum.png … Library.png  (named by trait)
```

## Option B — sync the whole layer tree (rclone, recommended for everything else)
`rclone` handles private shared Drive folders properly.
```bash
brew install rclone
rclone config            # n) new remote -> name: gdrive -> type: drive
                         # follow the browser auth; scope: drive.readonly is fine

# the layer-folders parent (id from scripts/drive_manifest.json):
rclone copy "gdrive:" ./art/_source_raw \
  --drive-root-folder-id 1T6ukPbOYVnb4DtAghYo3LuJ7hAvfvvzR \
  --include "*.png" -P

# then organize into art/layers/<NN_Layer>/ matching the names in
# data/traits_master.csv, and QA:
python scripts/tidy_local.py
python generator/build_config.py --scan
```

> `--drive-root-folder-id` values for each layer live in
> `scripts/drive_manifest.json` if you want to pull folders individually.

## Option C — manual (no CLI)
In Google Drive: open the **"uwu gf" → "uwu gf"** layer folder → download the
layer folders you need → unzip into `art/layers/<NN_Layer>/`. Then run
`python scripts/tidy_local.py`.

## After syncing — always
```bash
python scripts/tidy_local.py             # strips .DS_Store, checks size + alpha
python generator/build_config.py --scan  # maps real files + reads rarity tiers
python generator/generate.py --count 20  # spot-check a small real batch first
```

## Naming → trait mapping
- **Backgrounds** are numbered `1.png`–`15.png`; `pull_backgrounds.py` renames them
  to trait names using `scripts/drive_manifest.json`.
- Other layers: name each PNG after its trait (see `data/traits_master.csv`), or
  keep them in `common/ rare/ super_rare/ legendary/` subfolders and let
  `build_config.py --scan` infer the tier.
