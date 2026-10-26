# -*- coding: utf-8 -*-
"""site-v5: flat HH as the icon (favicon ladder, og), seal badge removed, wordmark unchanged."""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_history/site-v4")
DST = os.path.join(ROOT, "site-v5")
L2 = os.path.join(ROOT, "brand", "logos2")

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
IMG = os.path.join(DST, "assets", "img")

assets = {
    "hh-flat-gold.svg": "hh-gold.svg",
    "hh-flat-cream.svg": "hh-cream.svg",
    "hh-flat-navy.svg": "hh-navy.svg",
    "hh-3d-512.png": "hh-3d.png",
}
for src, dst in assets.items():
    shutil.copyfile(os.path.join(L2, src), os.path.join(IMG, dst))

# square app icon: navy field + gold flat HH
hh = open(os.path.join(L2, "hh-flat-gold.svg"), encoding="utf-8").read()
inner, w, h = hh.split("</svg>")[0].split(">", 1)[1], 713, 854
scale = (64 * 0.66) / h
tx, ty = (64 - w * scale) / 2, (64 - h * scale) / 2
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">\n'
       '<rect width="64" height="64" fill="#0B1A26"/>\n'
       f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.4f})">\n{inner}</g>\n</svg>\n')
open(os.path.join(IMG, "favicon.svg"), "w", encoding="utf-8").write(fav)

p = os.path.join(DST, "index.html")
html = open(p, encoding="utf-8").read()
done = []


def sub(old, new, label):
    global html
    assert html.count(old) == 1, f"{label}: {html.count(old)}"
    html = html.replace(old, new)
    done.append(label)


# the seal badge is a "gimmick" by the brand brief — the HH now lives in the icon, not the footer
sub('<img class="footer__seal" src="assets/img/seal-gold.svg" alt="" width="1090" height="1048" loading="lazy" />\n',
    '', "footer seal removed")

sub('<div>© <span id="year">2026</span> Higher Heights</div>',
    '<div>© <span id="year">2026</span> Higher Heights Films</div>', "copyright sub-brand")

# favicon points at the new tile
sub('<link rel="icon" href="assets/img/icon-32.png" sizes="32x32" type="image/png" />',
    '<link rel="icon" href="assets/img/icon-32.png" sizes="32x32" type="image/png" />\n'
    '<link rel="mask-icon" href="assets/img/favicon.svg" color="#0B1A26" />', "mask-icon")

open(p, "w", encoding="utf-8").write(html)
print("wrote", p)
for d in done:
    print("  ✓", d)
