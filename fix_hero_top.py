# -*- coding: utf-8 -*-
"""The scrim pullback cost the top strip its legibility.

Letting the footage breathe removed the darkness the nav and the discipline
strip were relying on, so they now sit on bright sky. Rather than put the
heavy scrim back and lose the colour again, add a shallow top gradient that
only covers the band the type occupies, plus a shadow on the type itself.
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


# a shallow top wash — only as deep as the type, so the sky survives
sub("""    linear-gradient(to top, rgba(11,26,38,.94) 0%, rgba(11,26,38,.72) 14%, rgba(11,26,38,.26) 38%, rgba(11,26,38,.04) 60%, rgba(11,26,38,.30) 100%),
    radial-gradient(95% 70% at 12% 102%, rgba(11,26,38,.80) 0%, transparent 62%);""",
"""    linear-gradient(to top, rgba(11,26,38,.94) 0%, rgba(11,26,38,.72) 14%, rgba(11,26,38,.26) 38%, rgba(11,26,38,.04) 60%, transparent 78%),
    linear-gradient(to bottom, rgba(11,26,38,.78) 0%, rgba(11,26,38,.42) 9%, transparent 19%),
    radial-gradient(95% 70% at 12% 102%, rgba(11,26,38,.80) 0%, transparent 62%);""",
    "shallow top wash for the nav band")

# and let the type defend itself, so the wash can stay light
sub(".hero__top{ display:flex; justify-content:space-between; align-items:center; gap:2rem; }",
    ".hero__top{ display:flex; justify-content:space-between; align-items:center; gap:2rem; }\n"
    ".hero__top .mono, .hero__status{ text-shadow:0 1px 16px rgba(11,26,38,.95), 0 0 3px rgba(11,26,38,.8); }",
    "shadow on the strip type")

sub(".nav__links a{", ".nav a, .nav__links a{ text-shadow:0 1px 14px rgba(11,26,38,.9); }\n.nav__links a{",
    "shadow on the nav")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
