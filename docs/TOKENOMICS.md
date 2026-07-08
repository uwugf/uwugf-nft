# UwU GF — Tokenomics

Locked from Natsio's plan (team chat, 2026-07-08). "Must be fair for everyone."

## Supply & allocation — 6969 total

| Bucket | Count | How it's enforced |
|---|---:|---|
| **Treasury** (team + 1/1s + KOL gifts) | **169** | `TEAM_RESERVE` constant, minted via `devUwu()` (capped) |
| **Whitelist — Twitter/X** | ~1,000 | off-chain: addresses added to the Merkle guest list |
| **Whitelist — collabs** | ~4,000 | off-chain: addresses added to the Merkle guest list |
| **Public (FCFS)** | ~1,800 | remainder, public phase |
| **Total** | **6,969** | `MAX_CUTIES` hard cap (immutable) |

> `169 + 1,000 + 4,000 + 1,800 = 6,969`. The Twitter/collab split is a **planning target**, not an on-chain
> parameter — the contract only knows "on the guest list or not." Who lands in each bucket is decided when the
> Merkle root is built (`setGuestList`). The team may also mint from their own wallets on the WL "to make more."

## Pricing

| Phase | Price | Contract knob |
|---|---:|---|
| Whitelist (Twitter **and** collabs) | **0.00069 Ξ** | `uwuListPrice` |
| Public | **0.001 Ξ** | `publicPrice` |

- **Same WL price for Twitter and collabs** is structural: there is a single `uwuListPrice` and a single
  `uwuList()` mint path — every guest-list address pays the same, so collab mint price can't be raised above the
  X mint price. This directly satisfies Natsio's "same mp for X and collabs, must be fair."
- Both prices are **owner-editable post-deploy** via `setBagPrices(wl, pub)` — nothing here is locked in stone.

## Per-wallet caps

| Phase | Cap | Contract knob |
|---|---:|---|
| Whitelist | 3 / wallet | `maxPerUwu` |
| Public | 10 / wallet | `maxPerDegen` |

Editable post-deploy via `setCaps(wl, pub)`.

## Notes / open items
- **Treasury = 169** was chosen from Natsio's "69 or 169" (the inclusive option, room for the 12 one-of-ones + 7
  KOL 1/1 gifts + team). It's a `constant`, so switching to 69 needs a redeploy — say the word before launch.
- Royalties: 6.9% (ERC-2981), receiver = owner/loveJar.
- Site still shows **TBA** for supply/price by design (announcement on hold) — publishing these numbers on the
  site is a separate go/no-go.
