#!/usr/bin/env bash
# Point the site's absolute URLs at the real domain (or back at the vercel one).
#   ./scripts/set_domain.sh uwugf.xyz
# Touches only the crawler-facing head tags: canonical, og:url, og:image,
# twitter:image. og:image must stay ABSOLUTE or the social card breaks.
set -euo pipefail
cd "$(dirname "$0")/.."
NEW="${1:?usage: $0 <domain>   e.g. uwugf.xyz}"
OLD="${2:-uwugf-nft.vercel.app}"

for f in website/index.html website/mint.html; do
  before=$(grep -c "$OLD" "$f" || true)
  python3 - "$f" "$OLD" "$NEW" <<'PY'
import sys
path, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(path, encoding='utf-8').read()
open(path, 'w', encoding='utf-8').write(s.replace(old, new))
PY
  echo "$f: $before occurrence(s) of $OLD -> $NEW"
done

echo
echo "next: commit + push, then confirm the card renders:"
echo "  https://cards-dev.twitter.com/validator   and   https://$NEW/"
