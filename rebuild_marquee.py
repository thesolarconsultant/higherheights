# -*- coding: utf-8 -*-
"""Rebuild the client marquee from the merged set (19 logos)."""
import os, re, json, colorsys

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
rep = json.load(open(os.path.join(ROOT, "brand", "clients", "sized.json")))
s = open(p, encoding="utf-8").read()
start = len(s)

NAVY_L, CREAM = 0.075, "#F4EFE6"


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def lift(h):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hh, l, sat = colorsys.rgb_to_hls(r, g, b)
    out = h
    for _ in range(16):
        out = "#%02X%02X%02X" % tuple(round(x * 255) for x in colorsys.hls_to_rgb(hh, l, sat))
        if (lum(out) + .05) / (NAVY_L + .05) >= 3.0:
            break
        l = min(0.95, l + 0.055)
    return out


# tint was computed at build time but never persisted for the original set
for r in rep:
    if not r.get("tint"):
        r["tint"] = lift(r["brand"]) if r.get("chromatic") else CREAM
json.dump(rep, open(os.path.join(ROOT, "brand", "clients", "sized.json"), "w"), indent=2)


def card(r):
    h = min(r["dh"], 44)
    w = round(h * r["aspect"])
    # very wide wordmarks need a ceiling or they dominate the rail
    if w > 170:
        w = 170
        h = round(w / r["aspect"])
    u = f'assets/img/clients/{r["slug"]}.png'
    return ('          <div class="client" style="--tint:%s">\n'
            '            <span class="client__mark" role="img" aria-label="%s"\n'
            '              style="width:%dpx;height:%dpx;'
            '-webkit-mask-image:url(%s);mask-image:url(%s)"></span>\n'
            '          </div>' % (r["tint"], r["label"], w, h, u, u))


half = (len(rep) + 1) // 2
rows = [rep[:half], rep[half:]]
marq = ('<div class="marq reveal">\n'
        + "\n".join('        <div class="marq__row">\n'
                    + "\n".join("  " + card(r) for r in row)
                    + "\n        </div>" for row in rows)
        + "\n      </div>")

m = re.search(r'<div class="marq reveal">.*?\n      </div>', s, re.S)
if not m:
    raise SystemExit("MISS: marquee block")
s = s[:m.start()] + marq + s[m.end():]

open(p, "w", encoding="utf-8").write(s)
print(f"marquee rebuilt: {len(rep)} logos ({half} + {len(rep)-half})")
print(f"written: {start} -> {len(s)} bytes")
for r in rep:
    print(f"   {r['label']}")
