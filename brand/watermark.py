# -*- coding: utf-8 -*-
"""Watermark variants of the HH mark: solid, hairline outline, and a cut edition line."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "logos2", "hh-flat-navy.svg")
OUT = os.path.join(ROOT, "watermark")
os.makedirs(OUT, exist_ok=True)

raw = open(SRC, encoding="utf-8").read()
vb = re.search(r'viewBox="([^"]+)"', raw).group(1)
paths = re.findall(r"<path[^>]*\sd=\"([^\"]+)\"", raw)
if not paths:
    raise SystemExit("no path data found")
d = max(paths, key=len)
print(f"viewBox {vb}, {len(paths)} path(s), longest {len(d)} chars")


def wrap(body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{extra} '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">\n'
            f"{body}\n</svg>\n")


# 1. solid — fill inherits from CSS so one file serves every scheme
open(os.path.join(OUT, "hh-solid.svg"), "w", encoding="utf-8").write(
    wrap(f'  <path d="{d}" fill="currentColor"/>')
)

# 2. hairline outline — reads as an engraving rather than a stain
for name, w in (("hh-outline.svg", 2.0), ("hh-outline-fine.svg", 1.1)):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(
        wrap(f'  <path d="{d}" fill="none" stroke="currentColor" stroke-width="{w}" '
             f'stroke-linejoin="round"/>')
    )

# 3. outline over a whisper of fill — the one that survives on busy ground
open(os.path.join(OUT, "hh-duo.svg"), "w", encoding="utf-8").write(
    wrap(f'  <path d="{d}" fill="currentColor" fill-opacity=".30"/>\n'
         f'  <path d="{d}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>')
)

for f in sorted(os.listdir(OUT)):
    print(" ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
