#!/usr/bin/env bash
# Put the UwU GF site live on Vercel (uses vercel.json -> serves website/).
# Normally not needed: pushing to main auto-deploys via the GitHub integration.
# Manual deploy from repo root:
#        npx vercel deploy --prod --yes
# non-interactive with a token (create at vercel.com/account/tokens):
#        VERCEL_TOKEN=xxx ./scripts/deploy_web.sh
set -e
cd "$(dirname "$0")/.."
if [ -n "$VERCEL_TOKEN" ]; then
  npx --yes vercel deploy --prod --yes --token="$VERCEL_TOKEN"
else
  npx --yes vercel deploy --prod --yes
fi
