#!/usr/bin/env bash
# Pack the collection into deterministic CARs and pin them on Filebase.
#
#   ./scripts/ipfs_pack_upload.sh
#
# CIDs are computed locally by kubo, not assigned by the provider, so the same
# bytes always produce the same CID and the set can be mirrored to another
# pinning service (4EVERLAND) under the identical CID later.
#
# Reads FILEBASE_* from contract/.env. Requires kubo and boto3.
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; source contract/.env; set +a
: "${FILEBASE_KEY:?}" "${FILEBASE_SECRET:?}" "${FILEBASE_BUCKET:?}" "${FILEBASE_ENDPOINT:?}"

WORK="${WORK:-/tmp/uwugf-ipfs}"; mkdir -p "$WORK"
ADD=(ipfs add -r --cid-version=1 --raw-leaves --chunker=size-262144 --pin=true --offline -Q)

echo "── images"
IMG_CID=$("${ADD[@]}" output/upload/images)
echo "   $IMG_CID"

echo "── metadata (rewriting __IMAGES_CID__ first)"
python3 - "$IMG_CID" <<'PY'
import sys, json, os, glob, shutil
cid = sys.argv[1]
dst = 'output/upload/metadata'
shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst, exist_ok=True)
for f in glob.glob('metadata/*.json'):
    base = os.path.basename(f)
    if not base[:-5].isdigit():          # skip _all / provenance / trait_distribution
        continue
    d = json.load(open(f))
    d['image'] = d['image'].replace('__IMAGES_CID__', cid)
    json.dump(d, open(f'{dst}/{base}', 'w'), indent=2, ensure_ascii=False)
PY
META_CID=$("${ADD[@]}" output/upload/metadata)
echo "   $META_CID"

for pair in "images:$IMG_CID" "metadata:$META_CID"; do
  name="${pair%%:*}"; cid="${pair##*:}"
  echo "── packing + pinning $name"
  ipfs dag export --progress=false "$cid" > "$WORK/$name.car"
  python3 scripts/filebase_upload.py "$WORK/$name.car" "$name.car"
done

cat <<SUMMARY

  images   ipfs://$IMG_CID
  metadata ipfs://$META_CID   <- glowUp("ipfs://$META_CID/")

  Keep these private until reveal. Filebase IPFS buckets are public: anyone
  holding a CID can fetch it, they just cannot enumerate the bucket.
SUMMARY
