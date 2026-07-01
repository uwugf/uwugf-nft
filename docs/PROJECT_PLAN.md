# UwU GF — project plan & roadmap 🗺️💕

## The goal
Sell out **6969** hand-drawn UwU GF NFTs. Whitelist cheaper than public.
Cute, degen, community-driven. Target prices: **WL 0.001 Ξ**, **public 0.0069 Ξ**.

## Economics (at target prices)
| | qty | price | gross |
|---|---|---|---|
| Reserve (team + 1/1s + KOL) | 100 | — | — |
| Whitelist (est.) | ~2,000 | 0.001 Ξ | 2 Ξ |
| Public | ~4,869 | 0.0069 Ξ | ~33.6 Ξ |
| **Total** | **6,969** | | **~35–36 Ξ** + 6.9% royalties |

> Reality check: a 6969 cheap mint selling out fully is *hard* and depends almost
> entirely on community + hype, not the contract. Plan for a strong WL engine, KOL
> seeding, and patience. The tech here is ready; the distribution is the work.

## Launch phases

**Phase 0 — foundations (DONE / in progress)**
- [x] Repo scaffold + generator pipeline + trait config/worksheet
- [x] Smart contract (ERC-721A + WL + royalties + provenance)
- [x] Marketing drafts + image prompts
- [x] Promo/mint website first draft
- [ ] Finish the art (artist) → see ART_STATUS.md

**Phase 1 — art & generation**
- [ ] Artist finishes Hair, Make-up, Stuffie + remaining Skin/Eyes/Mouth/Hoodie
- [ ] Export **isolated transparent PNGs**, one per trait, all **2000×2000**
- [ ] Sync to `art/layers/`, run `tidy_local.py` QA
- [ ] Tune rarity weights in `data/traits_master.csv`
- [ ] Generate full 6969 + lock provenance hash
- [ ] Build the 12 one-of-ones by hand, reserve token ids for them

**Phase 2 — infra**
- [ ] Upload images → IPFS (Pinata / nft.storage) → get `imagesCID`
- [ ] Rewrite `image` field in metadata to `ipfs://<imagesCID>/<id>.png`
- [ ] Upload metadata → IPFS → get `metadataCID`
- [ ] Make a pre-reveal "hidden" image + metadata → `hiddenCID`
- [ ] Build the WL Merkle tree from approved addresses → `merkleRoot`

**Phase 3 — contract**
- [ ] `forge test` green, deploy to **Sepolia**, full dry-run
- [ ] Deploy to chosen mainnet/L2, verify on explorer
- [ ] `pinkySwear(provenance)` · `setGuestList(root)` · set prices/caps

**Phase 4 — mint**
- [ ] Wire website to the deployed contract address + ABI + chain
- [ ] WL mint window → public mint window
- [ ] `glowUp(metadataCID)` reveal after sellout
- [ ] Confirm OpenSea collection renders (auto-indexes on Ethereum); set banner,
      description, royalties, socials
- [ ] `withdrawLove()` to team multisig

## 🟦 Decisions I need from you
1. ~~Chain~~ ✅ **DECIDED: Ethereum mainnet.** ERC-721A minimises mint gas; we may
   revisit per-wallet caps so a mint is worth the L1 gas. Dry-run on Sepolia first.
2. **Final prices & caps.** Confirm WL 0.001 / public 0.0069, per-wallet caps
   (currently WL 3 / public 10), and WL allocation size.
3. **Whitelist mechanism.** Merkle allowlist (built-in) vs a simpler "WL = public
   but earlier" gate. Merkle = real cheaper-WL but needs a collected address list.
4. **IPFS provider.** Pinata or nft.storage? (Need an API key to script uploads.)
5. **Reveal.** Delayed reveal (recommended — pre-reveal "soon 🥺" image, reveal
   after sellout) vs instant reveal at mint?
6. **Reserve split.** Of the 100 reserve: how many team vs 1/1s (12) vs KOL gifts?
7. **Domain + socials.** `uwugf.xyz` is a placeholder — real domain & X handle?
   (drives bio, metadata `external_url`, deploy config). No Discord — per your call.

## Risks / watch-outs
- **Don't deploy to mainnet without a testnet dry-run + peer review.** Real funds.
- Keep deployer key in a hardware wallet / never in the repo.
- "Retardio" trait name references another project — fine as homage, riskier for
  paid ads (noted in marketing drafts).
- Royalties aren't enforced by most marketplaces anymore — treat as upside, not budget.
