# -*- coding: utf-8 -*-
"""Regenerate the site's logo/icon assets in the official palette."""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(ROOT, "brand")
SITE = os.path.join(ROOT, "site-v6")
IMG = os.path.join(SITE, "assets", "img")
OUT = os.path.join(B, "palette")
os.makedirs(OUT, exist_ok=True)

MIDNIGHT, IVORY, SAGE, ORANGE = "#050936", "#FAF1D0", "#E5E0AF", "#E78223"


def recolour(src, dst, colour):
    s = open(src, encoding="utf-8").read()
    s2 = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{colour}"', s)
    open(dst, "w", encoding="utf-8").write(s2)
    return len(s2)


jobs = [
    # site asset name        source                              colour
    ("logo-caps-ivory.svg", os.path.join(B, "logos", "wm-caps-gold.svg"), IVORY),
    ("logo-full-ivory.svg", os.path.join(B, "logos2", "wordmark-cream.svg"), IVORY),
    ("logo-full-midnight.svg", os.path.join(B, "logos2", "wordmark-navy.svg"), MIDNIGHT),
    ("hh-ivory.svg", os.path.join(B, "logos2", "hh-flat-gold.svg"), IVORY),
    ("hh-midnight.svg", os.path.join(B, "logos2", "hh-flat-gold.svg"), MIDNIGHT),
    ("hh-sage.svg", os.path.join(B, "logos2", "hh-flat-gold.svg"), SAGE),
    ("hh-orange.svg", os.path.join(B, "logos2", "hh-flat-gold.svg"), ORANGE),
]
for name, src, colour in jobs:
    size = recolour(src, os.path.join(IMG, name), colour)
    shutil.copyfile(os.path.join(IMG, name), os.path.join(OUT, name))
    print(f"{name:26s} {colour}  {size} bytes")

# favicon tile: midnight field, ivory HH
hh = open(os.path.join(IMG, "hh-ivory.svg"), encoding="utf-8").read()
inner = hh.split("</svg>")[0].split(">", 1)[1]
W, H = 713, 854
scale = (64 * 0.66) / H
tx, ty = (64 - W * scale) / 2, (64 - H * scale) / 2
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">\n'
       '<rect width="64" height="64" fill="#050936"/>\n'
       f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">\n{inner}</g>\n</svg>\n')
open(os.path.join(IMG, "favicon.svg"), "w", encoding="utf-8").write(fav)
shutil.copyfile(os.path.join(IMG, "favicon.svg"), os.path.join(OUT, "favicon.svg"))
print("favicon.svg               midnight + ivory")
