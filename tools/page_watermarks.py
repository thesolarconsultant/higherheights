# -*- coding: utf-8 -*-
"""Refined-monogram watermarks on the service pages.

The service pages inherited the .hh-wm CSS from the shared head but carried
no watermark markup, so they had none at all.

Sized larger than the homepage marks (460/420px): these pages have calmer
sections and more room, so the mark can carry more weight without competing
with footage. Alternating corners so it does not read as a repeating stamp.

Colour-locked files, not the currentColor master -- an <img> does not
inherit currentColor.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")

PAGES = ["corporate-video-production.html", "event-videography.html",
         "videographer-london.html", "aerial-drone-filming.html"]

# bigger than the homepage pair, and a touch more present
CSS = """
/* Service pages: the mark gets more room than it does on the homepage */
.hh-wm--pg{ width:min(52%,620px); opacity:.07; }
.hh-wm--pg.is-br{ right:-30px; bottom:-38px; }
.hh-wm--pg.is-tl{ left:-30px;  top:-34px; }
.hh-wm--pg.is-bl{ left:-30px;  bottom:-38px; }
@media(max-width:860px){
  .hh-wm--pg{ width:min(66%,320px); opacity:.06; }
  .hh-wm--pg.is-br{ right:-16px; bottom:-20px; }
  .hh-wm--pg.is-tl{ left:-16px;  top:-18px; }
  .hh-wm--pg.is-bl{ left:-16px;  bottom:-20px; }
}
"""

def mark(corner, cream):
    src = "hh-cream.svg" if cream else "hh-navy.svg"
    return (f'      <div class="hh-wm hh-wm--pg {corner}" aria-hidden="true">'
            f'<img src="assets/img/{src}" alt="" loading="lazy" decoding="async"></div>\n')

total = 0
for f in PAGES:
    p = os.path.join(SITE, f)
    if not os.path.exists(p):
        print(f"   MISSING {f}"); continue
    s = open(p, encoding="utf-8").read()

    if ".hh-wm--pg{" not in s:
        s = s.replace("</style>", CSS + "</style>", 1)

    if 'hh-wm--pg' in s and '<div class="hh-wm hh-wm--pg' in s:
        print(f"   {f}: already marked"); continue

    # every <section> is a positioned stage already (position:relative on sections)
    # drop a mark into the first dark section and the cream one, alternating corners
    # Place in the FIRST and LAST eligible sections, not the first two.
    # Adjacent sections put a bottom-right mark next to the next section's
    # top-left one, so they cluster and read as a pair rather than as two
    # separate moments on the page.
    cand = [m for m in re.finditer(r'<section class="([^"]*)"[^>]*>\s*\n(\s*)<div class="wrap', s)
            if "contact" not in m.group(1)]
    if len(cand) >= 2:
        chosen = [(cand[0], "is-br"), (cand[-1], "is-tl")]
    elif cand:
        chosen = [(cand[0], "is-br")]
    else:
        chosen = []

    n = 0
    out, pos = [], 0
    for m, corner in chosen:                      # already in document order
        cls = m.group(1)
        ins = m.end(0) - len('<div class="wrap')
        out.append(s[pos:ins])
        out.append(mark(corner, cream="band-cream" not in cls))
        out.append("      ")
        pos = ins
        n += 1
    out.append(s[pos:])
    s = "".join(out)

    # sections must be a positioned stage and clip the bleed
    if ".hh-wm--pg" in s and "section{position:relative" not in s:
        s = s.replace("</style>",
            "\nmain > section{ position:relative; isolation:isolate; overflow:hidden; }\n"
            "main > section > .wrap{ position:relative; z-index:1; }\n</style>", 1)

    open(p, "w", encoding="utf-8").write(s)
    total += n
    print(f"   {f:34s} {n} marks")

print(f"\n{total} watermarks placed")
