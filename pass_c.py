# -*- coding: utf-8 -*-
"""Pass C — the client wall.

Fourteen real client logos, knocked to one ink and optically balanced so a
wide wordmark and a round seal carry the same weight. Mono at rest; hover
restores the real brand colour — so they are not 'just colour' sitting there.

Deliberately NOT the library's 'clientwall'/'proofclients': both drift two
rows of invented marks in opposite directions. For fourteen real logos a
still balanced grid reads as a client list; a conveyor belt reads as filler.

One element per logo: a CSS mask gives the shape, background gives the colour.
Any brand colour too dark to survive the navy is lifted, and the four
achromatic marks fall back to cream rather than disappearing.
"""
import os, json, shutil, colorsys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site-brand")
IMG = os.path.join(SITE, "assets", "img", "clients")
os.makedirs(IMG, exist_ok=True)

NAVY_L = 0.075   # relative luminance of #0B1A26
CREAM = "#F4EFE6"

rep = json.load(open(os.path.join(ROOT, "brand", "clients", "sized.json")))
for r in rep:
    shutil.copy(os.path.join(ROOT, "brand", "clients", r["slug"] + "-white.png"),
                os.path.join(IMG, r["slug"] + ".png"))
print(f"  +  {len(rep)} logos -> assets/img/clients/")


def lum(hexs):
    c = [int(hexs[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def lift(hexs):
    """Raise lightness until the mark clears the navy ground."""
    r, g, b = [int(hexs[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    h, l, sat = colorsys.rgb_to_hls(r, g, b)
    out = hexs
    for _ in range(16):
        out = "#%02X%02X%02X" % tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, sat))
        if (lum(out) + .05) / (NAVY_L + .05) >= 3.0:
            break
        l = min(0.95, l + 0.055)
    return out


for r in rep:
    r["tint"] = CREAM if not r.get("chromatic") else lift(r["brand"])
    ratio = (lum(r["tint"]) + .05) / (NAVY_L + .05)
    note = "" if r.get("chromatic") else "  (achromatic -> cream)"
    print(f"  {r['slug']:12s} {r['brand']} -> {r['tint']}  {ratio:4.1f}:1{note}")

p = os.path.join(SITE, "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:140])
    s = s.replace(old, new, 1)
    print("  ok ", why)


CSS = """
/* ══ Client wall ══════════════════════════════════════════════════
   Not the library's drifting rails: fourteen real marks, still and
   optically balanced. One ink at rest, the real brand colour on hover. ══ */
.clients{ padding:clamp(3.4rem,7vw,6rem) 0; border-top:1px solid var(--line-soft); }
.clients__head{ display:flex; justify-content:space-between; align-items:baseline;
  gap:2rem; flex-wrap:wrap; margin-bottom:clamp(2rem,4vw,3.2rem); }
.clients__grid{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(144px,1fr));
  gap:clamp(1.7rem,3.4vw,3rem) clamp(1.4rem,3vw,2.6rem); align-items:center; justify-items:center;
}
.client{ display:flex; align-items:center; justify-content:center; min-height:54px; }
.client__mark{
  display:block; background:var(--cream); opacity:.42;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat;
  -webkit-mask-position:center; mask-position:center;
  -webkit-mask-size:contain; mask-size:contain;
  transition:background .45s var(--ease), opacity .45s var(--ease);
}
.client:hover .client__mark{ background:var(--tint); opacity:1; }
@media (prefers-reduced-motion:reduce){ .client__mark{ transition:none } }
"""


def card(r):
    h = min(r["dh"], 44)
    w = round(h * r["aspect"])
    u = f'assets/img/clients/{r["slug"]}.png'
    return (f'          <div class="client" style="--tint:{r["tint"]}">\n'
            f'            <span class="client__mark" role="img" aria-label="{r["label"]}"\n'
            f'              style="width:{w}px;height:{h}px;'
            f'-webkit-mask-image:url({u});mask-image:url({u})"></span>\n'
            f'          </div>')


MARKUP = ('''
  <section class="clients" aria-labelledby="clients-head">
    <div class="wrap">
      <div class="clients__head">
        <div class="eyebrow reveal">
          <span class="eyebrow__line"></span><span class="mono">Trusted by</span></div>
        <span class="mono mono--dim" id="clients-head">Selected clients</span>
      </div>
      <div class="clients__grid reveal">
'''
          + "\n".join(card(r) for r in rep)
          + '''
      </div>
    </div>
  </section>
''')

sub("/* ══ Enquiry", CSS + "\n/* ══ Enquiry", "client wall CSS")
sub('  <section class="contact" id="contact"', MARKUP + '\n  <section class="contact" id="contact"',
    "client wall markup")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
