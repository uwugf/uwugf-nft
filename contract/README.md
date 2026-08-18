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
| `uwuList(proof, qty)` | whitelist | mint at `uwuListPrice` (0.00069 Ξ), Merkle-gated |
| `mint(qty)` | public | mint at `publicPrice` (0.001 Ξ) |
| `devUwu(to, qty)` | owner | team / 1-of-1 / KOL mint (≤ `TEAM_RESERVE` = 169) |
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
   ../scripts/deploy_robinhood.sh testnet    # dress rehearsal, then:
   ../scripts/deploy_robinhood.sh mainnet
   ```
4. `pinkySwear(provenanceHash)` — commit provenance on-chain.
5. `setGuestList(merkleRoot)` then `openHerHeart(true, false)` — whitelist opens.
6. Later `openHerHeart(true, true)` (or `(false, true)`) — public opens.
7. After sellout, `glowUp("ipfs://<metadataCID>/")` — **reveal** ✨.
8. `withdrawLove()` — to the team multisig.

## Chain: Robinhood Chain (decided)

Launching on **Robinhood Chain**, a permissionless EVM L2 that pays gas in ETH.
Nothing in the contract changes: same Solidity, same ERC-721A, same ETH prices,
standard Foundry tooling. What changes is that gas is L2-cheap, so the per-wallet
caps (3 wl / 10 public) are comfortable rather than gas-limited.

| | mainnet | testnet |
|---|---|---|
| chain id | `4663` | `46630` |
| rpc | `https://rpc.mainnet.chain.robinhood.com` | `https://rpc.testnet.chain.robinhood.com` |
| explorer | `https://robinhoodchain.blockscout.com` | `https://explorer.testnet.chain.robinhood.com` |
| gas token | ETH | ETH |
| verification | Blockscout (no API key) | Blockscout (no API key) |

Deploy with `scripts/deploy_robinhood.sh [testnet|mainnet]`. Always do the
**testnet dress rehearsal first**: it runs the identical code path and opens both
mint phases so the site is clickable end to end.

Gas reality check, measured on mainnet (block 36,639,534): base fee **0.0395 gwei**.
Our deploy is ~2.29M gas, so **deploying costs about 0.00009 ETH**, and a mint is
cents. The old L1 worry about "is a 0.001 Ξ mint even worth the gas" is gone.

Two things to sort before mint day:
- **Bridged ETH.** Minters need ETH *on Robinhood Chain*, not on L1. The mint page
  says so; make sure the socials do too.
- **Public RPC limits.** `rpc.mainnet.chain.robinhood.com` is shared and rate
  limited, and the mint page polls every 15s. Put a dedicated endpoint in
  `ROBINHOOD_RPC_URL` (and in `website/mint-config.js`) before launch.

The contract stays chain-agnostic, so an L1 or Base deploy is still one env var away.

## Security notes
- `MAX_CUTIES` (6969) and `TEAM_RESERVE` (169) are `constant` — cannot be raised.
- No `setSupply`, no unbounded owner mint, no `selfdestruct`, no proxy/upgrade.
- **No `tx.origin == msg.sender` gate** (removed 2026-08-18, deliberate call).
  It would have blocked every smart-contract wallet (Safe, ERC-4337, in-app
  embedded wallets) along with the bots, and on an app-centric L2 that is most
  of the audience. Contract minting is therefore possible: the per-wallet caps
  (`maxPerUwu` 3 / `maxPerDegen` 10) are what limit any single minter, and a
  determined bot can still spread across wallets. That is the accepted trade.
- `loveJar` can't be the zero address; provenance can only be set once.
- Before mainnet launch, get a proper audit or at least a peer review + a
  testnet dry-run on Robinhood Chain testnet. This is real money on a public chain.
