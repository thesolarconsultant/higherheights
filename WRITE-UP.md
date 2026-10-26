# Higher Heights Films — where the site is, and what's missing

**Live:** https://higher-heights.vercel.app
**Repo:** github.com/thesolarconsultant/higherheights — branch `design/site-brand-refresh`
**Last commit:** `6ad8e58`

---

## Part one — what's actually been done

### The site went from one page to five

| URL | Targets | UK searches/mo |
|---|---|---|
| `/` | video production UK, corporate video | — |
| `/corporate-video-production` | corporate videographer (6,600), corporate video (6,600), corporate video production (3,600) | **~13,500** |
| `/event-videography` | event videographer | **4,600** |
| `/videographer-london` | videographer london, video production london | **4,400** |
| `/aerial-drone-filming` | drone / aerial | lower volume, real differentiator |

All four share the homepage's real nav, mobile drawer, inverting-nav script and footer —
pulled from `index.html` at build time by `tools/pagekit.py`, not copied. They can't drift.

### The keyword research that drove it

| term | UK monthly |
|---|---|
| video production | 33,100 |
| video production services | 12,100 |
| video production company | 9,900 |
| corporate video | 6,600 |
| corporate videographer | 6,600 |
| videographer uk | 5,700 |
| event videographer | 4,600 |
| videographer london | 4,400 |
| **brand video production** | **390** |
| **brand film** | negligible |

The site was leading on the bottom two. The title said *"Film, Aerial & Photography"* —
no "video production" anywhere. That's now fixed.

### Design and brand work

- **Refined HH monogram** wired through everything — favicon, apple icon, both watermarks,
  share image. Your file was 351 KB (it carried the original raster trace as a hidden
  base64 PNG); it's now **994 bytes**.
- **16px problem solved** — a high-contrast serif loses its hairlines first, so each
  favicon size renders from a weight-compensated cut: stroke 16 at 16px, stroke 10 at
  32px, plain from 48px up.
- **Watermarks fixed** — they were cropped to 35–57% visible because the offsets were
  percentages, and a percentage on the vertical axis resolves against the *section's*
  height (`bottom:-14%` on a 2,249px section = 315px below its own container). Now
  **84–89% visible** on desktop, tablet and mobile.
- **Nav inverts over light sections** — it was a dark green pill at 82% sitting on cream,
  muddying the copy behind it. It now samples the ground beneath and swaps to cream.
- **Design system consolidated** — line-heights 11→5, tracking 10→5, transition durations
  12→3, two near-identical easing curves →1, twelve ad-hoc measures →4 tokens.
- **New hero loop** in, with a 1.44 MB mobile encode.

### Housekeeping

- **1.29 GB freed** — 1.19 GB of Puppeteer browser profiles, 90 MB of superseded builds,
  6.9 MB of orphaned video, 21 `.DS_Store` files.
- Site assets **67 files → 57**, and all 57 are referenced.
- 100 loose scripts sorted into `tools/` (9 live) and `tools/archive/` (91 one-offs).
- `sitemap.xml`, `robots.txt`, canonical URLs fixed to match the extensionless URLs
  Vercel actually serves.

---

## Part two — you're right, the pages are thin

Each service page currently has four blocks: intro, a list of what gets commissioned,
three paragraphs, a list of what you get, CTA. That's enough to exist. It isn't enough
to rank against agencies with 2,000-word service pages, and it isn't enough to convince
someone spending £10k.

**What's missing, and what should go in each one:**

### Every service page needs

1. **Real project examples with specifics** — not "recent work includes Oakridge" but
   what the job actually was: the brief, the constraint, what got made, how long it took.
2. **Process, step by step** — what happens between the first email and delivery. Buyers
   who've been burned before are scanning for this.
3. **What it costs** — a band, not a number. "Most corporate films here land between
   £X and £Y depending on days and locations." Pages with pricing convert better and
   filter out time-wasters.
4. **Turnaround** — how long from shoot to first cut to final.
5. **FAQs** — these win featured snippets and answer the objection before it's raised.
   "How long does a corporate video take?" "Do you write the script?" "Can we use it
   in paid ads?"
6. **What's included vs extra** — usage rights, revisions, cutdowns, stills, music
   licensing. Ambiguity here kills deals.

### Per page, specifically

**Corporate** — the biggest prize at ~13,500/mo. Needs: the Nexus recruitment film and
Oakridge property films written up properly as case studies; a section on recruitment
film specifically (it's a distinct buyer with a distinct problem); the internal-comms
angle; what happens with interviews and talking heads.

**Events** — needs turnaround times made explicit (this is the #1 buyer anxiety for
events), a section on multi-camera vs single operator, and the Matchroom ringside work
written up. Live-stream capability if it exists.

**London** — thinnest of the four. Needs genuinely local content: areas and venues worked
in, travel/call-out policy, parking and permit realities, same-day turnaround for London
clients. Generic copy with "London" dropped in won't rank.

**Aerial** — needs the CAA/insurance detail spelled out (it's a trust signal and a search
term — "CAA approved drone operator"), what can and can't be flown, how permissions work
near airports and over people, and the Spens Motors / property work shown.

---

## Part three — what I need from you to write it properly

I can write structure. I can't write the specifics without inventing them, and the
rebuild brief says explicitly: *do not invent credits, client results or testimonials.*
So I've left those gaps rather than filling them with plausible fiction.

**For each of the main jobs — Nexus, Oakridge, Matchroom, WatchTrader, RM69, NOBL,
WHOOP, Aduna, Spens Motors — I need three or four lines:**

- What did the client actually need?
- What was the constraint (budget, time, access, weather, one shot at it)?
- What got made — length, how many cutdowns, where it ran?
- Anything that went right or wrong worth telling?

**And on the business:**

- What does a typical job actually cost, in bands?
- How long from shoot to delivery?
- What's included as standard — usage, revisions, cutdowns, stills?
- Is the drone work CAA-certified? Insured to what level?
- London: happy to travel? Call-out minimum?

Give me that and the pages go from thin to genuinely useful — and from "exists" to
"ranks and converts."

---

## Part four — still outstanding

**The Chrome credential files are still in git history.** `.pptr/Default/Login Data`,
`Login Data For Account` and `Account Web Data` were removed from the working tree, but
they're still in commit `e264769` and earlier on a public repo. Either rewrite history
or rotate whatever that profile touched.

**`hello@higherheights.studio` bounces** — the domain doesn't exist. The enquiry form has
nowhere to land even if someone finds the page.

**No real domain.** A `.vercel.app` subdomain has no SEO authority. Every page I built is
now *eligible* to rank, which isn't the same as ranking. This is the single
highest-value thing left, and it fixes the email problem too.

**Nine breakpoints** — 520, 620, 640, 700, 760, 860, 900, 1024, 1100px. Too many to
reason about; needs a careful pass with eyes on each.

**Unused Drive material** — 16 RM69 stills, 13 Spens Motors shots, 26 files of Morgan
actually working, and the Oakridge and Nexus films. A `/work` index and a `/studio` page
would use most of it.
