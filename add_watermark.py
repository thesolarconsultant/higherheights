# -*- coding: utf-8 -*-
"""Add the oversized HH watermark to the Who panel (and a small one in the footer)."""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site-v9")
p = os.path.join(SITE, "index.html")
s = open(p, encoding="utf-8").read()

# ship the marks with the site
dst = os.path.join(SITE, "assets", "img")
for f in ("hh-outline.svg", "hh-outline-fine.svg", "hh-solid.svg", "hh-duo.svg"):
    shutil.copy(os.path.join(ROOT, "brand", "watermark", f), os.path.join(dst, f))


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n  " + old[:120])
    s = s.replace(old, new, 1)
    print("  ok  " + why)


# ── the panel becomes a positioning context, and the text sits above the mark ──
sub(".who__body{padding:clamp(3rem,7vw,7rem) clamp(1.6rem,4.5vw,5.5rem);display:flex;flex-direction:column;",
    ".who__body{position:relative;isolation:isolate;overflow:hidden;"
    "padding:clamp(3rem,7vw,7rem) clamp(1.6rem,4.5vw,5.5rem);display:flex;flex-direction:column;",
    "who__body is a stage")

# ── the watermark itself ──
sub("  .who__body .micro{color:rgba(8,8,10,.55)}",
    """  .who__wm{position:absolute;z-index:-1;right:-14%;bottom:-20%;width:min(78%,560px);
    color:var(--mid);opacity:.085;pointer-events:none;user-select:none}
  .who__wm svg,.who__wm img{display:block;width:100%;height:auto}
  .who__body>*{position:relative;z-index:1}
  .who__body .micro{color:rgba(8,8,10,.55)}""",
    "watermark style")

# ── markup: sits first so it reads as ground, not content ──
sub('  <div class="who__body">\n    <div class="micro">Who</div>',
    '  <div class="who__body">\n'
    '    <div class="who__wm" aria-hidden="true"><img src="assets/img/hh-outline.svg" alt=""></div>\n'
    '    <div class="micro">Who</div>',
    "watermark markup")

# ── mobile: pull it in so it never collides with the signature line ──
sub("    .who{grid-template-columns:1fr}",
    "    .who__wm{right:-20%;bottom:-8%;width:min(86%,360px);opacity:.07}\n"
    "    .who{grid-template-columns:1fr}",
    "watermark on mobile")

open(p, "w", encoding="utf-8").write(s)
print("\nwrote", p, len(s), "bytes")
