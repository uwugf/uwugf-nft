# UwU GF: Ten Layers and One Very Opinionated Stylist

*Draft. Numbers marked `{{ }}` are filled from the final generated set.*
*Structure follows the Blokyz "Prehistoric: An Era of Cavemen" format: lore first,
captioned character groups, then the rarity table.*

---

She is 6,969 hand-drawn girlfriends. Not generated art with a hand-drawn filter
over it, and not a model's idea of "cute anime girl" — an actual human drew every
hoodie, every stray eyelash, every badly-behaved stuffie.

What follows is how she is put together, who decides what she wears, and which of
her are one of one.

---

## The Ten Layers

Every gf is assembled from ten layers, stacked in a fixed order so the art always
reads correctly: the hood falls over the hair, the sunglasses sit on the face and
not on the fringe, the stuffie stays in frame.

| # | Layer | Traits | Always present? |
|---|---|---|---|
| 1 | Background | 15 | yes |
| 2 | Skin | 8 | yes |
| 3 | Make-up | 6 | often bare |
| 4 | Mouth | 14 | yes |
| 5 | Eyes | 24 | yes |
| 6 | Hair | 18 | yes |
| 7 | Choker | 4 | sometimes |
| 8 | Sunglasses | 4 | rarely |
| 9 | Hoodie | 17 | yes |
| 10 | Stuffie | 5 | sometimes |

Four of those layers are allowed to be empty, and that emptiness is deliberate.
A bare face is not a missing trait, it is a look. Sunglasses in particular are
tuned to be uncommon — most gfs would rather you saw her eyes.

*[IMAGE: five gfs side by side showing the same base with different hoodies]*
*Caption: One skin, five moods.*

---

## The Tiers

Traits are weighted, not uniform. A legendary trait is drawn roughly **33× less
often** than a common one.

| Tier | Relative weight |
|---|---|
| Common | 100 |
| Rare | 30 |
| Super rare | 10 |
| Legendary | 3 |

The legendaries hide in the places you actually look: a handful of eyes, one
skin, one mouth, two hoodies. Rarity you can spot across a room, not rarity
buried in a metadata field nobody opens.

*[IMAGE: legendary eyes close-up grid]*
*Caption: Diamonds, Ghost, Alien, Sniper — the eyes that stop the scroll.*

---

## The Resident Stylist

Most PFP collections roll every layer independently and ship whatever falls out.
That is how you end up with a mint full of gfs wearing a lime hoodie against a
lime background, technically rare and genuinely unwearable.

UwU GF has a stylist. She is code, she has opinions, and she has veto power.

Before any gf is minted, her combination is scored on colour relationships —
hoodie against background, hair against both, make-up and skin in support. The
score runs 0 to 1. Anything below **0.85 is thrown out and re-rolled.** No
exceptions, no "it's fine, it's rare".

*[IMAGE: vibe-pass-1..4.jpg]*
*Caption: Approved. The stylist let these leave the house.*

*[IMAGE: vibe-fail-1..4.jpg]*
*Caption: Denied. All four scored around 0.42 — technically valid, aesthetically a crime.*

The important part: **the stylist never changes the odds.** She rejects a
*combination*, then rolls again from the same weighted deck. Every trait stays
exactly as mintable as its tier says. Your legendary is not rarer or commoner
because of her, it just arrives dressed properly.

### House rules

Two rules are absolute, because breaking either one ruins the drawing:

1. **Sunglasses only go on plain eyes.** If a gf rolled Diamonds, Ghost, Alien,
   Sniper, Lucky, Dead, Dazed, SideEye or X eyes, the shades are refused. Nobody
   spends a legendary trait and then covers it up.
2. **The hood sits above everything except the face.** Hair tucks under, chokers
   sit below, and the stuffie always stays in her arms.

---

## The One of Ones

Six gfs are not assembled from layers at all. They were drawn start to finish as
single pieces, and they share none of their traits with the other 6,963.

| # | Name | |
|---|---|---|
| 1 | **Harry Potter** | the scar, the scarf, the disappointed eyebrows |
| 2 | **McDonald's** | headset on, shift never ending |
| 3 | **OpenSea** | sailing, allegedly |
| 4 | **Whale** | you know exactly what she means |
| 5 | **Farm Girl** | cow hoodie, barn, zero notes |
| 6 | **Ghost** | not a costume, we think |

Their token IDs are **scattered at random through the supply** — not 1 through 6,
not the last six. There is no position in the mint that gets you closer to one.
In the metadata they carry a single attribute, `1 of 1`, which puts them at the
top of the rarity ranking on their own.

*[IMAGE: the six 1/1s as a 3×2 grid]*
*Caption: Six drawn one at a time. Scattered anywhere in the 6,969.*

---

## The Set, In Numbers

{{ RARITY_TABLE — final trait counts and set percentages, generated from the
completed collection: layer, trait, tier, count, % of set, 1-in-N }}

---

## Provenance

The full image set is hashed before anything is revealed, and that hash is
committed on-chain in a single call that can never be made twice. It proves the
art-to-token assignment was fixed in advance — nobody, including us, could look
at who minted what and then reshuffle the rares.

Hash: `{{ PROVENANCE_HASH }}`

---

*She will not text you back but she will be in your wallet forever.*
