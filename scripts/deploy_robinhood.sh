#!/usr/bin/env bash
# Deploy UwU GF to Robinhood Chain (EVM L2, gas paid in ETH).
#
#   ./scripts/deploy_robinhood.sh            # testnet dress rehearsal (chain 46630)
#   ./scripts/deploy_robinhood.sh mainnet    # the real launch (chain 4663)
#
# Reads contract/.env (PRIVATE_KEY, HIDDEN_URI, ROYALTY_RECEIVER,
# ROBINHOOD_RPC_URL, ROBINHOOD_TESTNET_RPC_URL).
#
# Testnet run opens both mint phases so the site is immediately clickable.
# Mainnet run deploys + sets the guest list only: opening the mint stays a
# separate, deliberate command (see the runbook it prints at the end).
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.foundry/bin:$PATH"
set -a; source contract/.env; set +a

NET="${1:-testnet}"
case "$NET" in
  testnet)
    CHAIN_ID=46630
    RPC="${ROBINHOOD_TESTNET_RPC_URL:-https://rpc.testnet.chain.robinhood.com}"
    EXPLORER="https://explorer.testnet.chain.robinhood.com"
    CFG_KEY="robinhoodTestnet"
    ;;
  mainnet)
    CHAIN_ID=4663
    RPC="${ROBINHOOD_RPC_URL:-https://rpc.mainnet.chain.robinhood.com}"
    EXPLORER="https://robinhoodchain.blockscout.com"
    CFG_KEY="robinhood"
    ;;
  *) echo "usage: $0 [testnet|mainnet]"; exit 2;;
esac
VERIFIER_URL="$EXPLORER/api/"

# ── preflight: is the RPC actually reachable, and is it the chain we think? ──
# (some ISPs DNS-block *.robinhood.com — this catches that before spending gas)
echo "── preflight: $RPC"
SEEN=$(cast chain-id --rpc-url "$RPC" 2>/dev/null || true)
if [ -z "$SEEN" ]; then
  echo "!! cannot reach $RPC"
  echo "   dig +short ${RPC#https://}  — if that returns 158.140.186.3 / block.myrepublic.co.id,"
  echo "   it is the ISP DNS-blocking *.robinhood.com, not the chain being down."
  echo "   fix: set DNS to 1.1.1.1, or add the real IPs to /etc/hosts (see contract/.env.example),"
  echo "   or for mainnet: ROBINHOOD_RPC_URL=https://rpc.arrowrpc.com $0 $NET"
  exit 4
fi
[ "$SEEN" = "$CHAIN_ID" ] || { echo "!! rpc reports chain id $SEEN, expected $CHAIN_ID — wrong endpoint"; exit 4; }

DEPLOYER=$(cast wallet address --private-key "$PRIVATE_KEY")
BAL=$(cast balance "$DEPLOYER" --rpc-url "$RPC")
echo "   chain $CHAIN_ID ok · deployer $DEPLOYER · balance $(cast from-wei "$BAL") ETH"
[ "$BAL" != "0" ] || { echo "!! deployer has no ETH on this chain — bridge some over first"; exit 5; }

if python3 -c "import re,sys;s=open('website/mint-config.js').read();b=s.split('$CFG_KEY:')[1];sys.exit(0 if 'contract: \"0x' in b.split('},')[0] else 1)"; then
  echo "!! mint-config.js already has a $CFG_KEY address — clear it to force a redeploy"; exit 3
fi

if [ "$NET" = "mainnet" ]; then
  echo
  echo "  ⚠️  MAINNET DEPLOY — Robinhood Chain (4663). Real ETH, permanent contract."
  echo "      royalties → ${ROYALTY_RECEIVER}"
  echo "      hidden uri → ${HIDDEN_URI}"
  read -r -p "  type LAUNCH to continue: " OK
  [ "$OK" = "LAUNCH" ] || { echo "aborted"; exit 1; }
fi

GUEST_ROOT=$(node -p "require('./website/wl/proofs.json').root")

echo "── deploying UwU GF to Robinhood Chain ($NET)…"
cd contract
forge script script/Deploy.s.sol:Deploy --rpc-url "$RPC" --broadcast 2>&1 \
  | tee /tmp/uwugf-deploy-robinhood.log | grep -E "deployed at|owner"
ADDR=$(python3 -c "import json;print([t['contractAddress'] for t in json.load(open('broadcast/Deploy.s.sol/$CHAIN_ID/run-latest.json'))['transactions'] if t['transactionType']=='CREATE'][0])")
cd ..
echo "ADDR=$ADDR"

# run-latest.json records the SIMULATED address even when the broadcast fails, and
# the grep above hides forge's error. Confirm there is really code on chain before
# firing owner txs at an address that may not exist (this bit us on sepolia once).
[ "$(cast code "$ADDR" --rpc-url "$RPC")" != "0x" ] || {
  echo "!! no code at $ADDR — the broadcast did not land. Full log: /tmp/uwugf-deploy-robinhood.log"; exit 6; }

echo "── setGuestList($GUEST_ROOT)"
cast send "$ADDR" "setGuestList(bytes32)" "$GUEST_ROOT" --private-key "$PRIVATE_KEY" --rpc-url "$RPC" > /dev/null

if [ "$NET" = "testnet" ]; then
  echo "── openHerHeart(true, true)   # both phases open for the dry-run"
  cast send "$ADDR" "openHerHeart(bool,bool)" true true --private-key "$PRIVATE_KEY" --rpc-url "$RPC" > /dev/null
fi

# wire the site: address into this network's block, and make it the active one
python3 - "$CFG_KEY" "$ADDR" <<'PY'
import re, sys
key, addr = sys.argv[1], sys.argv[2]
p = "website/mint-config.js"
s = open(p).read()
head, _, tail = s.partition(f"{key}: {{")
body, close, rest = tail.partition("\n  },")
body = re.sub(r'contract: ""', f'contract: "{addr}"', body, count=1)
s = head + f"{key}: {{" + body + close + rest
s = re.sub(r'const UWUGF_ACTIVE = "[^"]*";', f'const UWUGF_ACTIVE = "{key}";', s)
open(p, "w").write(s)
print(f"── website/mint-config.js → {key} = {addr}")
PY

# Blockscout verification: no API key, but the verifier must be named explicitly
forge verify-contract "$ADDR" src/UwUGF.sol:UwUGF \
  --root contract --chain-id "$CHAIN_ID" \
  --verifier blockscout --verifier-url "$VERIFIER_URL" 2>&1 | tail -3 \
  || echo "(blockscout verify failed — non-fatal, retry later with the same command)"

echo
echo "── done ♡  $EXPLORER/address/$ADDR"
if [ "$NET" = "mainnet" ]; then
  cat <<EOF

  next, in order:
    cast send $ADDR "pinkySwear(string)" "<provenanceHash>" --private-key \$PRIVATE_KEY --rpc-url $RPC
    cast send $ADDR "openHerHeart(bool,bool)" true false --private-key \$PRIVATE_KEY --rpc-url $RPC   # wl opens
    cast send $ADDR "openHerHeart(bool,bool)" true true  --private-key \$PRIVATE_KEY --rpc-url $RPC   # public opens
    cast send $ADDR "glowUp(string)" "ipfs://<metadataCID>/" --private-key \$PRIVATE_KEY --rpc-url $RPC  # reveal
EOF
fi
