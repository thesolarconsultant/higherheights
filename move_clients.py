# -*- coding: utf-8 -*-
"""Move the logos into the original 'Selected clients' band, and drop the
duplicate section I had added lower down.

That band is CREAM, so the whole tint calculation inverts: the marks sit navy
at rest, and the hover colour must be dark enough to read on cream rather than
lifted to clear navy. Colours that are too light get darkened instead.
"""
import os, re, json, colorsys

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
rep = json.load(open(os.path.join(ROOT, "brand", "clients", "sized.json")))
s = open(p, encoding="utf-8").read()
start = len(s)

CREAM_L = 0.869          # relative luminance of #F4EFE6
INK = "#0B1A26"


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def ratio_on_cream(h):
    return (CREAM_L + .05) / (lum(h) + .05)


def darken(h):
    """Push a colour down until it reads on cream."""
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hh, l, sat = colorsys.rgb_to_hls(r, g, b)
    out = h
    for _ in range(18):
        out = "#%02X%02X%02X" % tuple(round(x * 255) for x in colorsys.hls_to_rgb(hh, l, sat))
        if ratio_on_cream(out) >= 3.0:
            break
        l = max(0.05, l - 0.05)
    return out


for r in rep:
    # on cream: achromatic marks just go ink; coloured ones darken to clear it
    r["tint_cream"] = INK if not r.get("chromatic") else darken(r["brand"])
json.dump(rep, open(os.path.join(ROOT, "brand", "clients", "sized.json"), "w"), indent=2)


def card(r):
    h = min(r["dh"], 38)
    w = round(h * r["aspect"])
    if w > 150:
        w = 150
        h = round(w / r["aspect"])
    u = f'assets/img/clients/{r["slug"]}.png'
    return ('            <div class="client" style="--tint:%s">\n'
            '              <span class="client__mark" role="img" aria-label="%s"\n'
            '                style="width:%dpx;height:%dpx;'
            '-webkit-mask-image:url(%s);mask-image:url(%s)"></span>\n'
            '            </div>' % (r["tint_cream"], r["label"], w, h, u, u))


# ── 1. the original text track becomes a logo track ──────────────────────
m = re.search(r'(<div class="marquee__track" id="marqueeTrack">)(.*?)(</div>)', s, re.S)
if not m:
    raise SystemExit("MISS: original marquee track")
s = s[:m.start(2)] + "\n" + "\n".join(card(r) for r in rep) + "\n          " + s[m.end(2):]
print(f"  ok  original track -> {len(rep)} logos")

# ── 2. style the marks for a cream ground ────────────────────────────────
sub_old = """.marquee__track span{"""
if sub_old not in s:
    raise SystemExit("MISS: marquee span style")
s = s.replace(sub_old,
""".marquee__track .client{ display:flex; align-items:center; justify-content:center;
  flex:0 0 auto; padding:0 clamp(1.5rem,3.2vw,2.9rem); min-height:46px; }
.marquee__track .client__mark{
  display:block; background:var(--ink); opacity:.46;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat;
  -webkit-mask-position:center; mask-position:center;
  -webkit-mask-size:contain; mask-size:contain;
  transition:background .45s var(--ease), opacity .45s var(--ease);
}
.marquee__track .client:hover .client__mark{ background:var(--tint); opacity:1; }
@media (prefers-reduced-motion:reduce){ .marquee__track .client__mark{ transition:none } }
.marquee__track span{""", 1)
print("  ok  cream-ground mark styling")

# ── 3. the duplicate section lower down goes ─────────────────────────────
m = re.search(r'\n  <section class="clients" aria-labelledby="clients-head">.*?\n  </section>\n', s, re.S)
if not m:
    raise SystemExit("MISS: duplicate clients section")
s = s[:m.start()] + "\n" + s[m.end():]
print("  ok  duplicate section removed")

# the JS doubles .marq__row; the original track needs the same treatment
s = s.replace('document.querySelectorAll(".marq__row").forEach(function (row) {',
              'document.querySelectorAll(".marq__row, #marqueeTrack").forEach(function (row) {', 1)
print("  ok  seamless-loop duplication now covers the original track")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
