#!/usr/bin/env bash
# Flip the homepage between the pre-launch TBA card and the live mint console.
#
#   ./scripts/set_mint_live.sh on    # console visible, TBA card hidden
#   ./scripts/set_mint_live.sh off   # TBA card visible, console hidden (pre-launch)
#
# The console markup always stays in the page; only which block is displayed
# changes, so turning the mint on at launch is this one command plus a deploy.
# With it off the wiring never boots: no chain reads, no contract address shown.
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:?usage: $0 on|off}"
python3 - "$MODE" <<'PY'
import json, sys
mode = sys.argv[1]
if mode not in ("on", "off"):
    sys.exit("usage: set_mint_live.sh on|off")
SLASH = chr(92) + 'u002F'
esc = lambda t: json.dumps(t, ensure_ascii=False)[1:-1].replace('/', SLASH)
p = 'website/index.html'
s = open(p, encoding='utf-8').read()

pairs = [('<div id="mintLive" style="display:none;">', '<div id="mintLive" style="display:block;">'),
         ('<div id="mintTba" style="text-align:center;',  '<div id="mintTba" style="display:none;text-align:center;')]
for hidden_live, shown_live in [pairs[0]]:
    a, b = (hidden_live, shown_live) if mode == "on" else (shown_live, hidden_live)
    if esc(a) in s:
        s = s.replace(esc(a), esc(b))
shown_tba, hidden_tba = pairs[1]
a, b = (shown_tba, hidden_tba) if mode == "on" else (hidden_tba, shown_tba)
if esc(a) in s:
    s = s.replace(esc(a), esc(b))

open(p, 'w', encoding='utf-8').write(s)
lines = s.split('\n')
i = [k for k, l in enumerate(lines) if l.startswith('"<!DOCTYPE html>')][0]
json.loads(lines[i])                       # bundle must stay parseable
print(f"mint console: {'LIVE' if mode == 'on' else 'hidden (TBA card shown)'}")
PY
echo "remember: with the console on, set the contract in website/mint-config.js"
