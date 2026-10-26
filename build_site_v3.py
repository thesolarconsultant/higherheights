# -*- coding: utf-8 -*-
"""site-v3: the two supplied logos, recoloured, applied to the v2 page."""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site-v2")
DST = os.path.join(ROOT, "site-v3")
LOGOS = os.path.join(ROOT, "brand", "logos")

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

ASSETS = {
    "wm-caps-gold.svg": "assets/img/logo-caps-gold.svg",
    "wm-caps-cream.svg": "assets/img/logo-caps-cream.svg",
    "wm-caps-navy.svg": "assets/img/logo-caps-navy.svg",
    "wm-full-cream.svg": "assets/img/logo-full-cream.svg",
    "wm-full-navy.svg": "assets/img/logo-full-navy.svg",
    "seal-gold.svg": "assets/img/seal-gold.svg",
    "seal-mark-gold.svg": "assets/img/hh-mark-gold.svg",
    "seal-mark-navy.svg": "assets/img/hh-mark-navy.svg",
}
for src, dst in ASSETS.items():
    shutil.copyfile(os.path.join(LOGOS, src), os.path.join(DST, dst))

# square favicon / app icon: navy field + gold HH
hh = open(os.path.join(LOGOS, "seal-mark-gold.svg"), encoding="utf-8").read()
inner = hh.split("</svg>")[0].split(">", 1)[1]
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">\n'
       '<rect width="64" height="64" fill="#0B1A26"/>\n'
       '<g transform="translate(12.5 11) scale(0.0655)">\n' + inner + '</g>\n</svg>\n')
open(os.path.join(DST, "assets/img/favicon.svg"), "w", encoding="utf-8").write(fav)

p = os.path.join(DST, "index.html")
html = open(p, encoding="utf-8").read()
checks = []


def sub(old, new, count=1, label=""):
    global html
    n = html.count(old)
    assert n == count, f"{label}: expected {count} got {n}"
    html = html.replace(old, new)
    checks.append(label)


NAV_OLD = ('<a class="brand" href="#top" aria-label="Higher Heights — home">\n'
           '      <img class="brand__mark" src="assets/img/mark-gold.svg" alt="" width="242" height="100" />\n'
           '      <span class="brand__text">Higher Heights</span>\n'
           '    </a>')
NAV_NEW = ('<a class="brand" href="#top" aria-label="Higher Heights — home">\n'
           '      <img class="brand__logo" src="assets/img/logo-caps-gold.svg" alt="Higher Heights" '
           'width="1881" height="160" />\n'
           '    </a>')
sub(NAV_OLD, NAV_NEW, label="nav lockup")

sub('.brand__mark{ width:clamp(26px,2.4vw,34px); height:auto; transition:transform .6s var(--ease); }',
    '.brand__logo{ height:clamp(15px,1.5vw,21px); width:auto; opacity:.96; transition:opacity .5s var(--ease); }\n'
    '.brand:hover .brand__logo{ opacity:1; }\n'
    '.brand__mark{ width:clamp(26px,2.4vw,34px); height:auto; transition:transform .6s var(--ease); }',
    label="brand logo css")

FOOT_OLD = ('<img class="footer__logo" src="assets/img/wordmark-light.svg" '
            'alt="Higher Heights — Film, Aerial, Photography" width="500" height="108" loading="lazy" />')
FOOT_NEW = ('<div class="footer__brand">\n'
            '            <img class="footer__logo" src="assets/img/logo-full-cream.svg" '
            'alt="Higher Heights — Films" width="1881" height="257" loading="lazy" />\n'
            '            <img class="footer__seal" src="assets/img/seal-gold.svg" alt="" '
            'width="1090" height="1048" loading="lazy" />\n'
            '          </div>')
sub(FOOT_OLD, FOOT_NEW, label="footer lockup + seal")

sub('.footer__logo{ width:clamp(210px,24vw,320px); height:auto; opacity:.92; }',
    '.footer__brand{ display:flex; align-items:center; gap:clamp(18px,2.4vw,34px); }\n'
    '.footer__logo{ width:clamp(210px,23vw,330px); height:auto; opacity:.94; }\n'
    '.footer__seal{ width:clamp(54px,5.4vw,80px); height:auto; opacity:.9; flex:none; }',
    label="footer css")

open(p, "w", encoding="utf-8").write(html)
print("wrote", p)
for c in checks:
    print("  ✓", c)
