# -*- coding: utf-8 -*-
"""Fix the hero.

Four things were wrong:

1. The title was Geist Light 200 — a thin grotesk. The brand's own wordmark is
   a high-contrast serif, so the hero was contradicting the identity it sits
   under. Moved to Instrument Serif.
2. The scrim stacked three navy layers, the lowest at .99 opacity, over footage
   already pushed to saturate(.72) brightness(.78). Green landscape and a red
   car were arriving as blue-grey mud. Brief rule 8: 'photography and film
   should provide most of the visual colour'.
3. The subline led on 'Commercial films, brand stories' — both on the brief's
   anti-keyword list (§20) — and closed on 'clients who care how it looks',
   which is the kind of line every agency writes.
4. Masked lines plus a serif with descenders would clip the g in 'Higher'
   and 'Heights'; the masks need descender room.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:150])
    s = s.replace(old, new, 1)
    print("  ok ", why)


# ── 1. the type ───────────────────────────────────────────────────────────
sub("""h1.hero__title{
  font-size:var(--fs-hero);
  font-weight:200;
  line-height:.86;
  letter-spacing:-.045em;
  text-wrap:balance;
}""",
"""h1.hero__title{
  font-family:"Instrument Serif",Georgia,serif;
  font-size:clamp(3.4rem,9.4vw,10rem);
  font-weight:400;
  line-height:.92;
  letter-spacing:-.022em;
  text-wrap:balance;
}""",
    "title -> Instrument Serif")

# masks must not guillotine the descenders
sub("h1.hero__title .rise{ padding-bottom:.04em; }",
    "h1.hero__title .rise{ padding-bottom:.17em; margin-bottom:-.17em; }",
    "descender room in the masks")

# ── 2. let the footage carry the colour ──────────────────────────────────
sub("""  background:
    linear-gradient(to top, rgba(11,26,38,.99) 0%, rgba(11,26,38,.94) 16%, rgba(11,26,38,.62) 40%, rgba(11,26,38,.34) 62%, rgba(11,26,38,.58) 100%),
    radial-gradient(120% 85% at 18% 100%, rgba(11,26,38,.92) 0%, transparent 66%),
    linear-gradient(90deg, rgba(11,26,38,.5) 0%, transparent 55%);""",
"""  background:
    linear-gradient(to top, rgba(11,26,38,.94) 0%, rgba(11,26,38,.72) 14%, rgba(11,26,38,.26) 38%, rgba(11,26,38,.04) 60%, rgba(11,26,38,.30) 100%),
    radial-gradient(95% 70% at 12% 102%, rgba(11,26,38,.80) 0%, transparent 62%);""",
    "scrim pulled back")

sub("filter:saturate(.72) brightness(.78) contrast(1.1);",
    "filter:saturate(1) brightness(.94) contrast(1.02);",
    "grade: stop desaturating the footage")

# ── 3. the copy ───────────────────────────────────────────────────────────
sub("""            Commercial films, brand stories and aerial cinematography —
            made for clients who care how it looks.""",
"""            Superyachts, classic cars and the machines people give
            their lives to — filmed through the people who keep them alive.""",
    "subline rewritten to the brief")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
