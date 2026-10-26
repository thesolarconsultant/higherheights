# -*- coding: utf-8 -*-
"""Lay a projector print over the hero footage.

Mechanic from Goodwork Library v1.3.0 'filmgrain': the drifting fractal-noise
grain, the 1px gate scratch and the flicker veil. The component's own light
leak (hot orange/pink on screen blend) and its pill-and-Poppins wrapper are
discarded — the leak would wreck the navy and the wrapper is house style.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

GRAIN_URI = (
    "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc"
    "yNDAnIGhlaWdodD0nMjQwJz48ZmlsdGVyIGlkPSduJz48ZmVUdXJidWxlbmNlIHR5cGU9J2ZyYWN0YWxOb2lzZScg"
    "YmFzZUZyZXF1ZW5jeT0nLjknIG51bU9jdGF2ZXM9JzMnIHN0aXRjaFRpbGVzPSdzdGl0Y2gnLz48ZmVDb2xvck1hd"
    "HJpeCB0eXBlPSdtYXRyaXgnIHZhbHVlcz0nMi4xIDAgMCAwIC0uNTUgMi4xIDAgMCAwIC0uNTUgMi4xIDAgMCAwIC"
    "0uNTUgMCAwIDAgMCAxJy8+PC9maWx0ZXI+PHJlY3Qgd2lkdGg9JzEwMCUnIGhlaWdodD0nMTAwJScgZmlsdGVyPSd"
    "1cmwoI24pJy8+PC9zdmc+"
)

CSS = """
/* ── Print: grain, gate scratch and flicker over the hero footage.
      Mechanic adapted from Goodwork Library v1.3.0 'filmgrain'.
      Its light leak and wrapper are deliberately not used. ── */
.print{ position:absolute; inset:0; z-index:-1; pointer-events:none; overflow:hidden; }
.print__grain{
  position:absolute; inset:-60%;
  background-image:url("%GRAIN%");
  background-size:240px 240px;
  mix-blend-mode:overlay; opacity:.26;
  animation:print-grain 1.1s steps(6) infinite;
}
.print__flick{
  position:absolute; inset:0; background:#fff;
  mix-blend-mode:overlay; opacity:0;
  animation:print-flick 6.2s ease-in-out infinite;
}
.print__scratch{
  position:absolute; top:0; bottom:0; width:1px; left:var(--x);
  background:linear-gradient(180deg,transparent,rgba(255,255,255,.55) 18%,rgba(255,255,255,.35) 72%,transparent);
  opacity:0; animation:print-scratch 5s steps(1) var(--d) infinite;
}
@keyframes print-grain{
  0%{transform:translate(0,0)}      10%{transform:translate(-4%,-7%)}
  20%{transform:translate(-10%,5%)} 30%{transform:translate(6%,-11%)}
  40%{transform:translate(-3%,13%)} 50%{transform:translate(-12%,-4%)}
  60%{transform:translate(10%,0)}   70%{transform:translate(0,11%)}
  80%{transform:translate(-8%,7%)}  90%{transform:translate(8%,-6%)}
  100%{transform:translate(0,0)}
}
@keyframes print-flick{
  0%{opacity:0} 6%{opacity:.055} 9%{opacity:0} 31%{opacity:.028}
  33%{opacity:.066} 35%{opacity:0} 60%{opacity:.044} 62%{opacity:0}
  84%{opacity:.06} 86%{opacity:.022} 88%{opacity:0}
}
@keyframes print-scratch{ 0%,100%{opacity:0} 40%{opacity:.6} 41.6%{opacity:0} }
@media (prefers-reduced-motion:reduce){
  .print__grain,.print__flick,.print__scratch{ animation:none!important }
  .print__flick,.print__scratch{ display:none }
  .print__grain{ opacity:.2 }
}
""".replace("%GRAIN%", GRAIN_URI)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:130])
    s = s.replace(old, new, 1)
    print("  ok ", why)


sub(".hero__media{ position:absolute; inset:0; z-index:-2; }",
    ".hero__media{ position:absolute; inset:0; z-index:-2; }\n" + CSS,
    "print CSS")

# sits above the scrim so the grain reads on the graded image, below the type
sub('<div class="hero__scrim" aria-hidden="true"></div>',
    '<div class="hero__scrim" aria-hidden="true"></div>\n'
    '    <div class="print" aria-hidden="true">\n'
    '      <div class="print__grain"></div>\n'
    '      <div class="print__flick"></div>\n'
    '      <div class="print__scratch" style="--x:23%;--d:0s"></div>\n'
    '      <div class="print__scratch" style="--x:61%;--d:2.4s"></div>\n'
    '      <div class="print__scratch" style="--x:84%;--d:3.7s"></div>\n'
    '    </div>',
    "print markup")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
