# -*- coding: utf-8 -*-
"""Put the full wordmark in the nav.

The nav carried the HH monogram plus 'Higher Heights' set in Geist caps — a
lockup assembled from two parts, one of which was live text imitating the
brand. Replaced with the supplied wordmark itself, so the nav shows the actual
HIGHER HEIGHTS / FILMS artwork.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:150])
    s = s.replace(old, new, 1)
    print("  ok ", why)


# ── markup: one image instead of a mark + text lockup ────────────────────
sub("""      <img class="brand__mark" src="assets/img/hh-gold.svg" alt="" width="713" height="854" />
      <span class="brand__text">Higher Heights</span>""",
"""      <img class="brand__wm" src="assets/img/wordmark-cream.svg"
           alt="Higher Heights Films" width="1600" height="357" />""",
    "nav lockup -> supplied wordmark")

# ── CSS ───────────────────────────────────────────────────────────────────
sub(".brand{ display:flex; align-items:center; gap:.7rem; flex-shrink:0; }",
    ".brand{ display:flex; align-items:center; flex-shrink:0; }\n"
    ".brand__wm{ width:clamp(132px,13.5vw,186px); height:auto; display:block;\n"
    "  transition:opacity .5s var(--ease); }\n"
    ".brand:hover .brand__wm{ opacity:.78; }\n"
    "@media(max-width:700px){ .brand__wm{ width:116px } }",
    "wordmark sizing")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
