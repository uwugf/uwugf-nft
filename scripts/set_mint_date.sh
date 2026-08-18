#!/usr/bin/env bash
# Set the mint date and switch the homepage countdown back on.
#   ./scripts/set_mint_date.sh 2026-09-05T17:00:00Z
# Pass an ISO-8601 UTC timestamp. The countdown is hidden while no date is set,
# because a target in the past renders 00:00:00:00 and the surrounding copy then
# reads as "the whitelist is closed".
set -euo pipefail
cd "$(dirname "$0")/.."
NEW="${1:?usage: $0 <ISO8601-UTC>   e.g. 2026-09-05T17:00:00Z}"

case "$NEW" in
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
  *) echo "!! not ISO-8601 UTC (want 2026-09-05T17:00:00Z)"; exit 2;;
esac
python3 - "$NEW" <<'PY'
import json, sys, datetime
new = sys.argv[1]
when = datetime.datetime.strptime(new, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
if when <= datetime.datetime.now(datetime.timezone.utc):
    sys.exit(f"!! {new} is in the past — that is exactly the bug this script exists to prevent")

SLASH = chr(92) + 'u002F'
esc = lambda t: json.dumps(t)[1:-1].replace('/', SLASH)
p = 'website/index.html'
s = open(p, encoding='utf-8').read()

old_dates = s.count('2026-08-15T17:00:00Z')
s = s.replace('2026-08-15T17:00:00Z', new)

hidden = esc('<div data-cd-row="" style="display:none;')
shown  = esc('<div data-cd-row="" style="display:flex;')
unhid  = s.count(hidden)
s = s.replace(hidden, shown)

teaser = esc("mint date drops very soon \U0001f552 get on the guest list first, she's picking her besties now ♡")
live   = esc("whitelist closes when the timer hits zero. don't wait to be a delulu, apply now!")
copies = s.count(teaser)
s = s.replace(teaser, live)

open(p, 'w', encoding='utf-8').write(s)
lines = s.split('\n')
json.loads(lines[201]); json.loads(lines[193])          # bundle must stay parseable
print(f"date set ({old_dates} refs) · countdown unhidden ({unhid}) · copy restored ({copies})")
PY

echo "now: git add website/index.html && git commit && git push"
