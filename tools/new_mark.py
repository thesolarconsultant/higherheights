# -*- coding: utf-8 -*-
"""New HH mark: watermark assets + positioning so nothing gets cut.

Two jobs.

1. The supplied files carry the original raster trace as an embedded base64
   PNG, so each one is 434KB for a 5-path vector. Stripped to ~4.5KB.
   Colour-locked copies are generated because an <img> does not inherit
   currentColor.

2. Watermarks were positioned with negative offsets, so a constant edge of
   the mark bled out of its section -- fine as a texture, but it clipped the
   serifs top and bottom. They now sit fully inside the section with a
   positive inset, so the whole mark is always on screen.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BR   = os.path.join(ROOT, "brand")
IMG  = os.path.join(ROOT, "site-brand", "assets", "img")

# ── assets ──
white = open(os.path.join(BR, "clean-hh-white.svg"), encoding="utf-8").read()
black = open(os.path.join(BR, "clean-hh-black.svg"), encoding="utf-8").read()
circle_w = open(os.path.join(BR, "clean-circle-white.svg"), encoding="utf-8").read()
circle_b = open(os.path.join(BR, "clean-circle-black.svg"), encoding="utf-8").read()

OUT = {
    "hh-cream.svg": (white, "#ffffff", "#F4EFE6"),   # on dark ground
    "hh-navy.svg":  (black, "#000000", "#0B1A26"),   # on cream ground
    "hh-gold.svg":  (black, "#000000", "#C9AE7C"),
    "hh-mono.svg":  (white, "#ffffff", "currentColor"),
    "hh-circle-cream.svg": (circle_w, "#ffffff", "#F4EFE6"),
    "hh-circle-navy.svg":  (circle_b, "#000000", "#0B1A26"),
}
for name, (src, frm, to) in OUT.items():
    s = src.replace(f'fill="{frm}"', f'fill="{to}"').replace(f"fill:{frm}", f"fill:{to}")
    open(os.path.join(IMG, name), "w", encoding="utf-8").write(s)
    print(f"  {name:24s} {len(s):6,} bytes  {to}")

# ── positioning: fully inside the section, nothing clipped ──
REPLACE = [
    # homepage, desktop
    (r"\.hh-wm--studio\{ right:-26px; bottom:-32px;",
     ".hh-wm--studio{ right:clamp(16px,3vw,54px); bottom:clamp(16px,3vw,48px);"),
    (r"\.hh-wm--contact\{ left:-26px; top:-30px;",
     ".hh-wm--contact{ left:clamp(16px,3vw,54px); top:clamp(16px,3vw,48px);"),
    # homepage, mobile
    (r"\.hh-wm--studio\{ right:-14px; bottom:-18px;",
     ".hh-wm--studio{ right:14px; bottom:16px;"),
    (r"\.hh-wm--contact\{ left:-14px; top:-16px;",
     ".hh-wm--contact{ left:14px; top:16px;"),
    # service pages
    (r"\.hh-wm--pg\.is-br\{ right:-30px; bottom:-38px; \}",
     ".hh-wm--pg.is-br{ right:clamp(16px,3vw,54px); bottom:clamp(16px,3vw,48px); }"),
    (r"\.hh-wm--pg\.is-tl\{ left:-30px;  top:-34px; \}",
     ".hh-wm--pg.is-tl{ left:clamp(16px,3vw,54px); top:clamp(16px,3vw,48px); }"),
    (r"\.hh-wm--pg\.is-bl\{ left:-30px;  bottom:-38px; \}",
     ".hh-wm--pg.is-bl{ left:clamp(16px,3vw,54px); bottom:clamp(16px,3vw,48px); }"),
    (r"\.hh-wm--pg\.is-br\{ right:-16px; bottom:-20px; \}",
     ".hh-wm--pg.is-br{ right:14px; bottom:16px; }"),
    (r"\.hh-wm--pg\.is-tl\{ left:-16px;  top:-18px; \}",
     ".hh-wm--pg.is-tl{ left:14px; top:16px; }"),
    (r"\.hh-wm--pg\.is-bl\{ left:-16px;  bottom:-20px; \}",
     ".hh-wm--pg.is-bl{ left:14px; bottom:16px; }"),
]

print()
for f in sorted(glob.glob(os.path.join(ROOT, "site-brand", "*.html"))):
    s = open(f, encoding="utf-8").read()
    hits = 0
    for pat, rep in REPLACE:
        s2, n = re.subn(pat, rep, s)
        if n:
            s = s2; hits += n
    # the mark must also fit inside the section, so cap it against the box
    s = s.replace(".hh-wm{ max-height:76%;", ".hh-wm{ max-height:62%;")
    if hits:
        open(f, "w", encoding="utf-8").write(s)
    print(f"  {os.path.basename(f):34s} {hits} offsets -> inset")
