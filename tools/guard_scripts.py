# -*- coding: utf-8 -*-
"""Make the shared script blocks safe on pages that lack homepage markup.

All page JS lives in one IIFE in index.html, split into commented sections.
Sections that drive homepage-only features (the film lightbox, hover-to-play
tiles, aerial parallax, the carousel, the hero video) dereference elements
that do not exist on a service page, so the first one to fail kills every
section after it -- including the inverting nav and reveal-on-scroll.

Each optional section now opens with a guard that returns early when its
markup is absent. Written as a labelled block so a bare `break` works
inside the shared IIFE without restructuring anything.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

# section marker  ->  selector that must exist for it to run
GUARDS = [
    ("/* ── hover-to-play film tiles ────────────────────────── */", ".film__frame, [data-film]"),
    ("/* ── screening modal ─────────────────────────────────── */", "#screen"),
    ("/* ── aerial parallax (transform only) ────────────────── */", ".aerial"),
    ("/* ── live London clock in the hero strip ─────────────── */", "#clock, .hero__clock"),
    ("/* ── hero video: pause when off-screen, resume on return ─ */", "#heroVideo"),
]

n = 0
for marker, sel in GUARDS:
    if marker not in s:
        print(f"  --  marker not found: {marker[:46]}")
        continue
    guard = (marker + "\n"
             f'  optional_{n}: {{ if (!document.querySelector("{sel}")) break optional_{n};\n')
    # close the labelled block at the next section marker, or before the IIFE end
    idx = s.index(marker)
    nxt = len(s)
    for m2, _ in GUARDS:
        j = s.find(m2, idx + len(marker))
        if j != -1:
            nxt = min(nxt, j)
    # also stop at any other top-level section comment
    m3 = re.search(r"\n  /\* ── ", s[idx + len(marker):])
    if m3:
        nxt = min(nxt, idx + len(marker) + m3.start() + 1)
    s = s[:idx] + guard + s[idx + len(marker):nxt] + "  }\n" + s[nxt:]
    n += 1
    print(f"  ok  guarded {marker.split('──')[1].strip()[:40]:42s} on  {sel}")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  ({n} sections guarded)")
