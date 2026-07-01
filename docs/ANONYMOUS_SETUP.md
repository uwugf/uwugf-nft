# UwU GF — anonymous ops setup 🕵️‍♀️

A do-it-yourself guide to a clean, pseudonymous project identity — nothing tied to
your personal `foxtroteth` accounts. (Pseudonymity is normal in crypto. Still: pay
your taxes, don't defraud buyers, follow the law — anonymity ≠ impunity.)

> ⚠️ I can't create accounts or enter passwords for you (hard safety rule). You do the
> signups; once you're logged in, I can drive the deploy in your Chrome + wire everything up.

**The golden rule:** ONE fresh identity, created in order (email first — everything
chains off it), NEVER mixed with your personal email / handle / wallets / photos.
Use a **separate browser profile** (Chrome → profiles → Add) for all of it.

---

## 🚀 Quick path — just to share the site today (10 min)
1. **Proton Mail** → https://proton.me → create free account (e.g. `uwugf.team@proton.me`). No phone needed for basic signup.
2. **Netlify** → https://app.netlify.com → "Sign up" → use the Proton email.
3. Tell me you're logged in + **attach `uwugf-site.zip` here** → I'll drop it via your Chrome → you get a permanent `uwugf.netlify.app` link. Done. 🎉

Everything below is the full stack for the actual mint.

---

## 1. 📧 Anonymous email  (the root of everything)
- **Proton Mail** (proton.me) — free, privacy-first, minimal signup. Recommended.
- Alt: Tutanota. Avoid a personal Gmail (ties to phone/identity).
- Use this email for **every** project account below. Pick a project name, not your name.

> ⚠️ **Gotcha: "Proton account restricted from registering on third-party services."**
> New free Proton accounts are rate-limited from signing up elsewhere (anti-spam), which
> blocks verification emails from Netlify etc. Fixes, best-anonymity first:
> - **Add a recovery *email*** (Proton → Settings → Recovery). Any email you control works —
>   it stays **private** (Netlify and the public never see it), so it barely dents anonymity.
>   This lifts the block immediately. *(Skip the phone option — that's more identifying.)*
> - **Apple "Hide My Email"** (if on Mac/iCloud): generates a random alias that forwards to you —
>   Netlify only ever sees the alias. Clean.
> - **Or just use a dedicated Gmail** for the project. Yes Google knows it's you — but it's still
>   **anonymous to your buyers and the public**, which is the anonymity that actually matters for
>   an NFT launch. Most pseudonymous founders do exactly this.

> 🧠 **Two kinds of "anonymous":** *anonymous-to-the-public/buyers* (what matters — achieved by a
> dedicated email + handle + wallet not tied to your name) vs *anonymous-to-the-providers*
> (Google/Netlify know your IP — only matters if you distrust the companies themselves, needs
> Proton + VPN). For shipping this project, the first is what counts.

## 2. 🔑 Password manager  (keep it separate)
- **Bitwarden** (free) — make a NEW vault/account with the Proton email, separate from personal.
- Generate a **unique strong password per service**. Turn on **2FA** everywhere (authenticator app like Aegis/Proton Authenticator — avoid SMS 2FA, it's phone-linked).

## 3. 🐦 Socials
- **X/Twitter**: sign up with the Proton email + a fresh handle (`@uwugf` etc.). No personal photos/links. (No Discord — per your call.)

## 4. 🌐 Website hosting  (pick one — all free)
- **Netlify** (easiest): sign up w/ Proton email → drag the site zip, or connect a repo. I can drive the drop for you.
- **Vercel**: sign up w/ Proton email or the anon GitHub below → best for the mint dApp later.
- **GitHub** (optional but useful): make an anon account w/ Proton email → host code + one-click deploy to Vercel/Netlify, or use GitHub Pages.

## 5. 🌍 Domain  (e.g. uwugf.xyz)
- **Most anonymous:** **Njalla** (njal.la) — privacy registrar that registers *on your behalf*, accepts crypto. They're the owner-of-record, you control it.
- **Easy + private:** **Cloudflare Registrar** or **Namecheap** — both include free WHOIS privacy (your info hidden from public lookups; the registrar still knows you if you pay by card).
- **Fully on-chain:** an **ENS `.eth`** name — no personal info at all, but needs a web gateway to resolve as a normal site.
- Point the domain at Netlify/Vercel (they give you the DNS records).

## 6. 📦 IPFS  (for the 6969 images + metadata)
- **Pinata** (pinata.cloud) — free tier, sign up w/ Proton email → get an **API key**. Give me the key (or set it as an env var) and I'll run the upload scripts to pin images + metadata and return the CIDs.
- Alts: **nft.storage**, **web3.storage**, **Filebase**. Any works — just sign up anon.

## 7. 👛 Wallets  (keep three roles separate)
- **Deployer wallet**: a brand-new **Rabby** or **MetaMask** wallet (fresh seed phrase, never used before, never linked to your personal wallets). Deploys the contract + is the initial owner.
- **Treasury / payout wallet**: a **Safe multisig** (safe.global) — mint funds withdraw here, NOT the deployer. Set `loveJar` to this.
- **Royalty receiver**: can be the Safe too.
- Funding reality check: on-chain is **pseudonymous, not invisible** — every transfer is traceable. Fund the deployer from a source not tied to your name if you care. **Do NOT** use sanctioned mixers. Keep the seed phrase offline; a **hardware wallet** (Ledger) for the treasury is strongly recommended.
- **Never** put a seed phrase or private key into any website, and never commit `.env` (the deployer key) to git.

## 8. 🛡️ OpSec checklist
- [ ] Separate Chrome profile (or separate browser) for all project accounts
- [ ] Unique email + handle + passwords, none reused from personal
- [ ] 2FA (authenticator app) on email, hosting, X, Pinata, exchanges
- [ ] Optional VPN during signups (hides your IP from the services)
- [ ] Fresh wallet seed stored offline; hardware wallet for treasury
- [ ] Never post identifying details (location, voice, personal handles, timezone tells)
- [ ] `.env` in `.gitignore` (already done); never share private keys with anyone — including me

---

## What I can do once you're set up
- **Website**: you attach the zip / log into Netlify in Chrome → I deploy + wire the domain.
- **IPFS**: give me a Pinata API key → I pin images + metadata, return CIDs, rewrite metadata.
- **Contract**: you fund the fresh deployer + drop its key in `contract/.env` → I run the Sepolia dry-run, then mainnet deploy + verify (you approve the final broadcast).
- I will **never** ask for or handle your seed phrase, and I can't create accounts or sign in for you.
