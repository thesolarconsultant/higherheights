# -*- coding: utf-8 -*-
"""Loading screen: the official wordmark under the monogram.

The loader showed the HH mark over a mono-type "Higher Heights" caption.
That caption was set in Geist Mono -- it was never the logo. The real
lockup (wordmark-cream.svg, the HIGHER HEIGHTS / FILMS artwork used in the
nav and footer) now sits under the mark instead.

Inlined rather than linked so it cannot be delayed by a second request on
the one screen whose whole job is to appear immediately.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")

word = open(os.path.join(SITE, "assets", "img", "wordmark-cream.svg"),
            encoding="utf-8").read()
word = re.sub(r"<\?xml[^>]*\?>", "", word).strip()
word = re.sub(r"<!--.*?-->", "", word, flags=re.S).strip()

CSS = """
.hhload__logo{
  width:clamp(190px,26vw,330px); height:auto;
  opacity:0; transform:translateY(8px);
  animation:hhload-logo .95s var(--ease,cubic-bezier(.16,1,.3,1)) .34s forwards;
}
.hhload__logo svg{ display:block; width:100%; height:auto; }
@keyframes hhload-logo{ to{ opacity:1; transform:none; } }
@media(prefers-reduced-motion:reduce){
  .hhload__logo{ opacity:1; transform:none; animation:none; }
}
"""

n = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    if 'class="hhload__logo"' in s:
        print(f"   {os.path.basename(f)}: already has it"); continue

    # swap the mono caption for the real lockup
    m = re.search(r'<div class="hhload__word">.*?</div>', s, re.S)
    if not m:
        print(f"   {os.path.basename(f)}: no caption found"); continue
    s = s[:m.start()] + f'<div class="hhload__logo">{word}</div>' + s[m.end():]

    if ".hhload__logo{" not in s:
        s = s.replace("</style>", CSS + "</style>", 1)

    open(f, "w", encoding="utf-8").write(s)
    n += 1
    print(f"   {os.path.basename(f)}")

print(f"\nwordmark on the loader for {n} pages")
