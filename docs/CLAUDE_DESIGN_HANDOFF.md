# UwU GF — Claude Design handoff 🎨

Everything you need to rebuild / retouch the site in **Claude Design** (claude.ai).
Section 1 is a copy-paste prompt. Sections 2–5 are the exact design system, content,
assets, and interactions so you can tweak precisely.

---

## 1. 📋 Copy-paste this into Claude Design

> Build a single-page, mobile-responsive landing site for a cute NFT project called
> **UwU GF** — 6,969 hand-drawn anime "uwu girlfriend" PFPs minting on **Ethereum**.
> Vibe: kawaii / pastel / chronically-online-degen but wholesome. Playful, lowercase copy.
>
> **Design system**
> - Palette: hot-pink `#ff5fa2`, soft-pink `#ffd6e8`, lavender `#b08bff`, soft-lavender
>   `#e7dcff`, plum text `#3a2348`, muted plum `#7a5d8c`, mint `#9be8d8`, gold `#ffd86b`.
> - Page background: layered soft radial-gradients (pink top-left, lavender top-right)
>   over a `#fff7fc → #fdf0fb → #f3ecff` vertical gradient.
> - Fonts: **Fredoka** (600–700) for headings/brand/buttons; **Quicksand** (400–600) for body.
> - Rounded everything: cards `radius 24px`, pills `999px`, inputs `14px`. Soft pink shadows
>   (`0 18px 40px -18px rgba(255,95,162,.45)`). Generous whitespace.
>
> **Sections, top to bottom**
> 1. **Sticky nav** — logo image left; center links About / Traits / FAQ; right: a pink
>    pill button "Apply for WL 🎀" and a disabled "Mint soon" ghost button. Hamburger on mobile.
> 2. **Hero** (2 columns, stacks on mobile) — left: pill tag "🌸 hand-drawn · 6969 supply ·
>    minting on Ethereum", big headline "your new **uwu girlfriend** lives on-chain 🥺" (with
>    "uwu girlfriend" in a pink→lavender gradient), a lead line, two buttons ("Apply for
>    whitelist 💕" pink, "Meet the GFs" lavender), and a 4-up stat row (6969 supply / 0.00069Ξ
>    whitelist / 0.001Ξ public / ETH chain). Right: a **3×3 grid of square NFT cards** — 6 real
>    GF images + 3 blurred "soon 🥺" cards.
> 3. **Marquee** — infinite horizontal scroll of words/emoji: uwu · 🎀 · hand-drawn · 💕 · 6969 ·
>    exit liquidity · 💎 · on ETH · 🦄 · wgmi · ✨.
> 4. **About** — eyebrow "what even is this", heading "a girlfriend for every mood you
>    doomscroll through", + 3 cards: 🎨 actually hand-drawn / 💎 rarity that matters / 🩷 fair &
>    cute on Ethereum.
> 5. **Wardrobe** — eyebrow "the wardrobe", heading "9 layers of cuteness 🎀", a line about
>    100+ traits, then a **horizontal auto-scrolling carousel of fuzzy-hoodie garment images**
>    (clothes only, no faces), then rarity pills: common / rare / super rare / ✦ legendary.
> 6. **Mint countdown** — centered, "she's almost ready 🥺", a 4-unit DAYS/HRS/MIN/SEC counter.
> 7. **Whitelist** — a big rounded card: eyebrow "be her bestie", heading "apply for whitelist
>    🥺👉👈", a line "WL gets you in at 0.00069Ξ instead of 0.001Ξ", and a form (X handle*, wallet
>    address*, referred-by, "why do you deserve a uwu gf?" textarea, Submit button + disclaimer).
>    A cute mascot GF image peeks from the top-right corner (desktop only).
> 8. **FAQ** — eyebrow "delulu questions", heading "FAQ", 5 expand/collapse accordion items.
> 9. **Footer** — a full-width banner image, the logo, three social icons (X, OpenSea, Discord-
>    NONE — just X + OpenSea), and a small disclaimer that it's art, not financial advice.
>
> **Motion (respect `prefers-reduced-motion`)**: floating hearts/sparkles drifting up in the
> hero; NFT cards gently bob; the logo/brand does a subtle wiggle; a pulsing glow on the main
> pink CTA; two marquees scrolling opposite directions; the wardrobe carousel auto-scrolls and
> pauses on hover.
>
> Keep it a single self-contained HTML file with inline CSS + vanilla JS. Use placeholder pastel
> image boxes where I'll drop in the real art. Cute, polished, lots of hearts and sparkles. ♡

---

## 2. Design tokens (exact)

| token | value |
|---|---|
| `--pink` | `#ff5fa2` |
| `--pink-soft` | `#ffd6e8` |
| `--lav` | `#b08bff` |
| `--lav-soft` | `#e7dcff` |
| `--plum` (text) | `#3a2348` |
| `--plum-soft` | `#7a5d8c` |
| `--mint` | `#9be8d8` |
| `--gold` | `#ffd86b` |
| card shadow | `0 18px 40px -18px rgba(255,95,162,.45)` |
| headings font | Fredoka 600/700 · body Quicksand 400/600 |
| radii | cards 24px · pills 999px · inputs 14px |
| max content width | 1120px |
| mobile breakpoints | 900px (layout) · 560px (fine-tune) |

## 3. Real copy (so you don't have to retype)
- Headline: **your new uwu girlfriend lives on-chain 🥺**
- Lead: *6969 hand-drawn uwu gfs. she's cute, she's degen, she's kinda your exit liquidity (jk… unless?). whitelist is open bestie.*
- Stats: 6969 supply · 0.00069Ξ whitelist · 0.001Ξ public · ETH chain
- About cards, FAQ Q&As, whitelist form fields, footer disclaimer — all in `website/index.html`.

## 4. Assets (in `website/assets/`)
| file | use |
|---|---|
| `uwugf-logo-t.png` | transparent logo — nav + footer |
| `uwugf-banner.png` | 3:1 banner — footer + social share (og:image) |
| `uwugf-mascot.png` | mascot — whitelist corner |
| `hero-1..6.jpg` + `peek-1,2.jpg` | the 6 hero NFT cards (peek-1/2 are the finished "main characters") |
| `hero-7,8,9.jpg` | the 3 blurred "soon" cards |
| `fit-purple/pink/periwinkle.jpg` | wardrobe carousel garments |

## 5. Interactions to preserve
- **Hero grid**: 6 real imgs + 3 `.soon` cards (blurred img + "soon 🥺" overlay via `::after` + `backdrop-filter`).
- **Wardrobe carousel**: flex track, `translateX(-50%)` keyframe loop, pause on hover.
- **Two marquees**: opposite directions (`animation-direction:reverse` on the second).
- **Countdown**: JS ticking to a target date (`CONFIG.mintDate`).
- **Whitelist form**: posts to `CONFIG.wlEndpoint` if set, else saves to localStorage (needs a real backend before launch — Formspree/Tally).
- **Floating hearts**: JS injects ~16 emoji spans with random `floatUp` timing.

> The current build lives in `website/index.html` (one file). Open it in Claude Design, or paste
> the prompt above to regenerate a clean editable version, then drop the `assets/` images back in.
