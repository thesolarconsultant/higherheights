# -*- coding: utf-8 -*-
"""Spencer Matthews second from the top, and the enquiry address.

The work grid pairs two independent things:
  f1..f8        grid-column span -- POSITIONAL (f1 and f6 span 8, the rest 4)
  film--w / --v aspect ratio      -- CONTENT (16/9 wide vs 5/6 vertical)

So the two wide films have to sit on f1 and f6 or the layout breaks. Dropping
whoop into slot 2 and pushing everything down would have handed Highland Road
(16/9) a span-4 slot and Clean Co (5/6) a span-8 one. Swapping Highland and
Clean Co keeps a wide film on f6 and costs nothing -- they were adjacent.

  was : roller  nobl  wtc  rm69  cleanco  highland  whoop  aduna
  now : roller  WHOOP nobl wtc   rm69     highland  cleanco aduna
          w                                  w
"""
import os, re

SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site-brand")
PAGE = os.path.join(SITE, "index.html")

ORDER = ["roller", "whoop", "nobl", "wtc", "rm69", "highland", "cleanco", "aduna"]
WIDE_SLOTS = {1, 6}          # f1 and f6 span 8 columns

s = open(PAGE, encoding="utf-8").read()

# ── lift each film block, with the comment line above it ──
pat = re.compile(
    r'[ \t]*<!--[^>]*-->\s*\n'                       # the "<!-- 02 -->" line
    r'([ \t]*<button class="film film--([wv]) f\d+ reveal" data-film="([a-z0-9]+)".*?</button>)',
    re.S)

blocks = {}
for m in pat.finditer(s):
    blocks[m.group(3)] = {"html": m.group(1), "shape": m.group(2), "full": m.group(0)}

missing = [k for k in ORDER if k not in blocks]
if missing or len(blocks) != 8:
    raise SystemExit(f"expected 8 films, found {len(blocks)}; missing {missing}")

# ── sanity: the wide films must end up on the wide slots ──
for i, name in enumerate(ORDER, 1):
    shape = blocks[name]["shape"]
    if (i in WIDE_SLOTS) != (shape == "w"):
        raise SystemExit(
            f"slot f{i} and '{name}' disagree: slot wide={i in WIDE_SLOTS}, film--{shape}. "
            "Reordering would break the grid.")

# ── rebuild, renumbering f1..f8 by position and naming the comments ──
first = min(m.start() for m in pat.finditer(s))
last  = max(m.end()   for m in pat.finditer(s))
indent = re.match(r"[ \t]*", blocks["roller"]["html"]).group(0)

out = []
for i, name in enumerate(ORDER, 1):
    html = blocks[name]["html"]
    html = re.sub(r'(class="film film--[wv]) f\d+', rf'\1 f{i}', html, count=1)
    out.append(f"{indent}<!-- {name} -->\n{html}")

s = s[:first] + "\n\n".join(out) + s[last:]
open(PAGE, "w", encoding="utf-8").write(s)

print("  order now:")
for i, n in enumerate(ORDER, 1):
    w = " (wide)" if i in WIDE_SLOTS else ""
    mark = "  <-- Spencer Matthews" if n == "whoop" else ""
    print(f"    f{i}  {n}{w}{mark}")

# ── the enquiry address ──
print()
import glob
total = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))) + \
         [os.path.join(SITE, "api", "enquiry.js")]:
    if not os.path.exists(f):
        continue
    t = open(f, encoding="utf-8").read()
    c = t.lower().count("hello@higherheights.uk")
    if not c:
        continue
    t = re.sub(r"hello@higherheights\.uk", "info@higherheights.uk", t, flags=re.I)
    open(f, "w", encoding="utf-8").write(t)
    total += c
    print(f"  {os.path.basename(f):34s} {c} -> info@")
print(f"\n  {total} references now info@higherheights.uk")
