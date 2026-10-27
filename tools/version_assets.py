# -*- coding: utf-8 -*-
"""Version the brand assets so a browser cannot serve a stale copy.

The mark has been replaced three times under the same filenames
(hh-navy.svg, hh-cream.svg, hh-mono.svg). Browsers and the CDN cache SVGs
hard, so the new artwork was live while the old one was still being served
from cache -- indistinguishable, from the outside, from "it didn't work".

Filenames now carry a content hash. Change the artwork, the name changes,
and every cache is bypassed automatically.
"""
import os, re, glob, hashlib, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "site-brand", "assets", "img")
HTML = sorted(glob.glob(os.path.join(ROOT, "site-brand", "*.html")))

ASSETS = ["hh-navy.svg", "hh-cream.svg", "hh-gold.svg", "hh-mono.svg",
          "hh-circle-navy.svg", "hh-circle-cream.svg"]

renames = {}
for a in ASSETS:
    p = os.path.join(IMG, a)
    if not os.path.exists(p):
        print(f"  skip {a} (absent)"); continue
    body = open(p, "rb").read()
    h = hashlib.sha1(body).hexdigest()[:8]
    stem, ext = os.path.splitext(a)
    stem = re.sub(r"\.[0-9a-f]{8}$", "", stem)        # drop any previous hash
    new = f"{stem}.{h}{ext}"
    if new != a:
        shutil.copy(p, os.path.join(IMG, new))
        renames[a] = new
    print(f"  {a:24s} -> {new}")

# point every reference at the hashed name
total = 0
for f in HTML:
    s = open(f, encoding="utf-8").read()
    before = s
    for old, new in renames.items():
        s = s.replace(f"assets/img/{old}", f"assets/img/{new}")
    if s != before:
        open(f, "w", encoding="utf-8").write(s)
        total += 1

# the loader inlines the SVG, so it is immune to caching and needs nothing

# clean up the unhashed originals so nothing can reference them by accident
for old in renames:
    p = os.path.join(IMG, old)
    if os.path.exists(p):
        os.remove(p)

print(f"\n  {total} pages repointed, {len(renames)} assets versioned")
