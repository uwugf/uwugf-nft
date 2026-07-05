#!/usr/bin/env bash
# Show / hide the mint page on the live site (uwugf-nft.vercel.app).
#
#   scripts/mint_page.sh on      → mint page reachable + "mint ♡" in the index nav
#   scripts/mint_page.sh off     → /mint, /mint.html, /mint-config.js, /wl/* all
#                                  302 to the homepage + nav link removed
#   scripts/mint_page.sh status
#
# Edits vercel.json "redirects" and patches the bundled index.html nav.
# Changes are LOCAL — review with `git diff`, then commit + push (Vercel
# auto-deploys main via the GitHub integration).
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-status}"

redirects() { # add|remove|check the mint kill-switch rules in vercel.json
  node -e '
    const fs = require("fs");
    const f = "vercel.json";
    const mode = process.argv[1];
    const j = JSON.parse(fs.readFileSync(f, "utf8"));
    const MINT = ["/mint", "/mint.html", "/mint-config.js", "/wl/:path*"];
    const isMint = (r) => MINT.includes(r.source);
    const cur = j.redirects || [];
    const has = cur.some(isMint);
    if (mode === "check") { console.log(has ? "redirects: HIDDEN (302 → home)" : "redirects: OPEN (mint reachable)"); process.exit(0); }
    let next = cur.filter((r) => !isMint(r));
    if (mode === "add") next = next.concat(MINT.map((s) => ({ source: s, destination: "/", permanent: false })));
    if (next.length) j.redirects = next; else delete j.redirects;
    fs.writeFileSync(f, JSON.stringify(j, null, 2) + "\n");
    JSON.parse(fs.readFileSync(f, "utf8")); // sanity
    console.log("vercel.json redirects " + (mode === "add" ? "armed (mint hidden)" : "cleared (mint open)"));
  ' "$1"
}

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
  on)  redirects remove; nav_link add
       echo "mint page: ON. now: git add vercel.json website/index.html && git commit && git push" ;;
  off) redirects add; nav_link remove
       echo "mint page: OFF. now: git add vercel.json website/index.html && git commit && git push" ;;
  status) redirects check; nav_link check ;;
  *) echo "usage: $0 on|off|status"; exit 1 ;;
esac
