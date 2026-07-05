#!/usr/bin/env bash
# Deploy UwU GF to Sepolia + configure for the testnet dry-run.
# Reads contract/.env (PRIVATE_KEY, HIDDEN_URI, ROYALTY_RECEIVER, SEPOLIA_RPC_URL).
# Idempotent-ish: refuses to redeploy if website/mint-config.js already has an address.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.foundry/bin:$PATH"
set -a; source contract/.env; set +a
RPC="${SEPOLIA_RPC_URL:-https://ethereum-sepolia-rpc.publicnode.com}"
ROOT_FILE="website/wl/proofs.json"
GUEST_ROOT=$(node -p "require('./$ROOT_FILE').root")

if grep -q 'contract: "0x' website/mint-config.js; then
  echo "mint-config.js already has a contract address — aborting (edit it out to force redeploy)"; exit 3
fi

echo "── deploying UwU GF to Sepolia…"
cd contract
forge script script/Deploy.s.sol:Deploy --rpc-url "$RPC" --broadcast 2>&1 | tee /tmp/uwugf-deploy.log | grep -E "deployed at|owner"
ADDR=$(python3 -c "import json;print([t['contractAddress'] for t in json.load(open('broadcast/Deploy.s.sol/11155111/run-latest.json'))['transactions'] if t['transactionType']=='CREATE'][0])")
cd ..
echo "ADDR=$ADDR"

echo "── setGuestList($GUEST_ROOT)"
cast send "$ADDR" "setGuestList(bytes32)" "$GUEST_ROOT" --private-key "$PRIVATE_KEY" --rpc-url "$RPC" > /dev/null
echo "── openHerHeart(true, true)   # both phases open for the dry-run"
cast send "$ADDR" "openHerHeart(bool,bool)" true true --private-key "$PRIVATE_KEY" --rpc-url "$RPC" > /dev/null

# wire the site to the deployed address
sed -i '' "s|contract: \"\"|contract: \"$ADDR\"|" website/mint-config.js
echo "── website/mint-config.js updated"

# keyless source verification so the ABI is readable in a UI
forge verify-contract "$ADDR" src/UwUGF.sol:UwUGF \
  --root contract --verifier sourcify --chain 11155111 2>&1 | tail -2 || echo "(sourcify verify failed — non-fatal)"

echo "── done ♡  https://sepolia.etherscan.io/address/$ADDR"
