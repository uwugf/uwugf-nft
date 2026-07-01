# UwU GF 🎀 ( ｡♥‿♥｡ )

> 6969 hand-drawn uwu girlfriends, on-chain & oh-so-cute.

Monorepo for the UwU GF NFT launch: art pipeline, generator, smart contract,
mint site, and marketing. Built to take the project from raw art → sold out.

```
uwu-gf/
├── art/            layer art (synced from Drive — not committed)
│   └── layers/     01_Background … 09_Stuffie  (the compositing stack)
├── generator/      🐍 the generative engine
│   ├── build_config.py   trait spec → traits.config.json + worksheet
│   ├── generate.py       weighted rolls → images + metadata + rarity + provenance
│   └── traits.config.json
├── data/           traits_master.csv  (editable rarity worksheet)
├── images/         ⤵ generated art        (gitignored)
├── metadata/       ⤵ generated metadata   (gitignored)
├── contract/       💝 Foundry / ERC-721A contract (UwUGF.sol)
├── website/        🌐 promo + whitelist + mint site
├── marketing/      🐦 X/Twitter drafts + image prompts
├── scripts/        🛠 Drive sync + art QA tooling
└── docs/           📋 plan, art status, sync guide
```

## Quickstart

```bash
# 1. env
python3 -m venv .venv && source .venv/bin/activate
pip install -r generator/requirements.txt

# 2. build the trait config + worksheet from the spec
python generator/build_config.py --scan

# 3. run the WHOLE pipeline today with placeholders (no art needed)
python generator/generate.py --placeholder --count 50
open images/_contact_sheet.png      # see 50 sample GFs + metadata + rarity

# 4. when real art lands in art/layers/ :
python scripts/tidy_local.py        # QA the layers (size/alpha checks)
python generator/build_config.py --scan
python generator/generate.py --count 6969 --only-available
```

## Where things stand
- ✅ **Generator + metadata + rarity + provenance pipeline** — built & tested.
- ✅ **Trait spec** — all ~110 traits + 12 one-of-ones transcribed to config + CSV.
- ✅ **Smart contract** — written (ERC-721A, WL, royalties, cute fns). Needs `forge` to build/test.
- ✅ **Marketing drafts** — launch thread, WL push, mint-day, image prompts.
- ✅ **Promo/mint website** — first draft in `website/`.
- 🟨 **Art** — Backgrounds done; Skin/Eyes/Mouth/Choker/Hoodie in progress;
  Hair/Make-up/Stuffie not drawn yet. See [docs/ART_STATUS.md](docs/ART_STATUS.md).
- ⏳ **IPFS upload / deploy / OpenSea** — pipeline-ready, waiting on final art + your keys.

👉 **Read [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) for the roadmap + the decisions I need from you.**
