# UwU GF — smart contract 💝

ERC-721A collection contract with whitelist (Merkle), public mint, on-chain
provenance, and EIP-2981 royalties. Cute on the surface, boringly-safe
underneath: **supply is capped & immutable, there are no hidden mints, and the
owner can never mint past the 100 reserve.**

## Setup (Foundry)

```bash
# 1. install foundry  (https://book.getfoundry.sh)
curl -L https://foundry.paradigm.xyz | bash && foundryup

# 2. from contract/ install deps
forge install chiru-labs/ERC721A --no-commit
forge install OpenZeppelin/openzeppelin-contracts --no-commit
forge install foundry-rs/forge-std --no-commit

# 3. build + test
forge build
forge test -vvv
```

## Cute-function cheat sheet 🎀

| Theme name | Who | What it does |
|---|---|---|
| `uwuList(proof, qty)` | whitelist | mint at `uwuListPrice` (0.001 Ξ), Merkle-gated |
| `adopt(qty)` | public | mint at `publicPrice` (0.0069 Ξ) |
| `devUwu(to, qty)` | owner | team / 1-of-1 / KOL mint (≤ `TEAM_RESERVE` = 100) |
| `openHerHeart(wl, pub)` | owner | toggle the whitelist / public phases |
| `setGuestList(root)` | owner | set the whitelist Merkle root |
| `glowUp(baseURI)` | owner | **the reveal** — point metadata at the real IPFS CID |
| `pinkySwear(hash)` | owner | lock the provenance hash once (pre-reveal) |
| `setBagPrices(wl, pub)` | owner | adjust prices |
| `setCaps(wl, pub)` | owner | adjust per-wallet caps |
| `withdrawLove()` | owner | send contract ETH to `loveJar` |

## Launch-day runbook

1. **Generate** the collection + provenance hash (`generator/generate.py`).
2. **Upload** images + metadata to IPFS (`scripts/` → get CIDs).
3. **Deploy** with a *hidden* `HIDDEN_URI` so art stays unrevealed at mint:
   ```bash
   cp .env.example .env   # fill PRIVATE_KEY, ROYALTY_RECEIVER, HIDDEN_URI
   forge script script/Deploy.s.sol:Deploy --rpc-url mainnet --broadcast --verify -vvvv
   ```
4. `pinkySwear(provenanceHash)` — commit provenance on-chain.
5. `setGuestList(merkleRoot)` then `openHerHeart(true, false)` — whitelist opens.
6. Later `openHerHeart(true, true)` (or `(false, true)`) — public opens.
7. After sellout, `glowUp("ipfs://<metadataCID>/")` — **reveal** ✨.
8. `withdrawLove()` — to the team multisig.

## Chain: Ethereum mainnet (decided)

Launching on **Ethereum L1**. ERC-721A keeps mint gas about as low as L1 allows
(cheap batch mints), but gas is still real — keep that in mind when finalising
per-wallet caps so a mint is worth it. Always do a **Sepolia** testnet dry-run
before mainnet. The contract is chain-agnostic if you ever revisit an L2 later.

## Security notes
- `MAX_CUTIES` (6969) and `TEAM_RESERVE` (100) are `constant` — cannot be raised.
- No `setSupply`, no unbounded owner mint, no `selfdestruct`, no proxy/upgrade.
- `tx.origin == msg.sender` blocks contract/bot minting (simple, intentional).
- `loveJar` can't be the zero address; provenance can only be set once.
- Before mainnet launch, get a proper audit or at least a peer review +
  testnet dry-run on Sepolia. This is real money on a public chain.
