#!/usr/bin/env bash
# Put the UwU GF site live. Two easy options ♡
#
#  A) Vercel  — run from repo root (uses vercel.json -> serves website/):
#        npx vercel deploy --prod --yes
#     first run opens a browser to log in; after that it just deploys.
#     non-interactive with a token (create at vercel.com/account/tokens):
#        VERCEL_TOKEN=xxx ./scripts/deploy_web.sh
#
#  B) Netlify Drop — zero CLI, zero account:
#        drag  uwugf-site.zip  onto  https://app.netlify.com/drop
#
set -e
cd "$(dirname "$0")/.."
if [ -n "$VERCEL_TOKEN" ]; then
  npx --yes vercel deploy --prod --yes --token="$VERCEL_TOKEN"
else
  npx --yes vercel deploy --prod --yes
fi
