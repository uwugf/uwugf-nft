#!/usr/bin/env bash
# Show / hide the mint page on the live site (uwugf.netlify.app).
#
#   scripts/mint_page.sh on      → mint.html reachable + "mint ♡" in the index nav
#   scripts/mint_page.sh off     → mint urls 302 to the homepage, nav link removed
#   scripts/mint_page.sh status
#
# Flips website/_redirects comments and patches the bundled index.html nav.
# Changes are LOCAL — review with `git diff`, then commit + push to deploy.
set -euo pipefail
cd "$(dirname "$0")/.."
R=website/_redirects
MODE="${1:-status}"

nav_link() { # add|remove|check the mint link inside the __bundler/template JSON
  node -e '
    const fs = require("fs");
    const f = "website/index.html";
    const mode = process.argv[1];
    const lines = fs.readFileSync(f, "utf8").split("\n");
    const i = lines.findIndex(l => l.startsWith("\"<!DOCTYPE"));
    if (i < 0) { console.error("bundler template line not found"); process.exit(1); }
    let tpl = JSON.parse(lines[i]);
    const link = `<a href="mint.html" style="text-decoration:none;color:var(--hot-pink);font-weight:700;">mint ♡</a>\n      `;
    const anchor = `<a href="#about" style="text-decoration:none;color:var(--muted);">about</a>`;
    const has = tpl.includes("mint.html");
    if (mode === "check") { console.log(has ? "nav link: present" : "nav link: absent"); process.exit(0); }
    if (mode === "add" && !has) {
      if (!tpl.includes(anchor)) { console.error("nav anchor not found"); process.exit(1); }
      tpl = tpl.replace(anchor, link + anchor);
    } else if (mode === "remove" && has) {
      tpl = tpl.split(link).join("");
    } else { console.log("nav link already " + (mode === "add" ? "present" : "absent")); process.exit(0); }
    // escape "/" so no raw </script> can terminate the inline bundle block
    lines[i] = JSON.stringify(tpl).split("/").join("\\u002F");
    if (lines[i].includes("</script>")) { console.error("escape failure"); process.exit(1); }
    JSON.parse(lines[i]); // round-trip sanity
    fs.writeFileSync(f, lines.join("\n"));
    console.log("nav link " + (mode === "add" ? "added" : "removed"));
  ' "$1"
}

case "$MODE" in
  on)
    sed -i '' -e 's|^# MINT:OFF$|# MINT:ON|' -e 's|^/mint.html|# /mint.html|' -e 's|^/mint-config.js|# /mint-config.js|' -e 's|^/wl/\*|# /wl/*|' "$R"
    nav_link add
    echo "mint page: ON (open). now: git add -A website && git commit && git push" ;;
  off)
    sed -i '' -e 's|^# MINT:ON$|# MINT:OFF|' -e 's|^# /mint.html|/mint.html|' -e 's|^# /mint-config.js|/mint-config.js|' -e 's|^# /wl/\*|/wl/*|' "$R"
    nav_link remove
    echo "mint page: OFF (hidden). now: git add -A website && git commit && git push" ;;
  status)
    grep -q '^# MINT:ON$' "$R" && echo "redirects: OPEN (mint reachable)" || echo "redirects: HIDDEN (302 → home)"
    nav_link check ;;
  *) echo "usage: $0 on|off|status"; exit 1 ;;
esac
