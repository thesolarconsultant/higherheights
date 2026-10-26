# -*- coding: utf-8 -*-
"""Consolidate the design system.

Measured on the live build:
  line-height      11 distinct values  ->  5
  letter-spacing   10 distinct values  ->  5
  transition       12 distinct values  ->  3
  easing            2 near-identical   ->  1
  ad-hoc font-size  5 off-token        ->  tokens

Every value maps to its nearest canonical neighbour, so nothing moves more
than a hair visually — but the system stops arguing with itself.

Also: scroll-margin so anchored content clears the fixed nav, and the one
rounded pill group squared off to match the rest of the page.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def count(pat):
    return len(re.findall(pat, s))


# ── 1. LINE HEIGHT: 11 -> 5 (1 tight / 1.08 display / 1.5 lede / 1.6 body / 1.7 loose)
LH = {"1.02": "1", "1.12": "1.08", "1.62": "1.6", "1.72": "1.7", "1.8": "1.7", "1.9": "1.7"}
n = 0
for a, b in LH.items():
    pat = r"line-height:\s*" + re.escape(a) + r"(?![0-9])"
    n += count(pat)
    s = re.sub(pat, "line-height:" + b, s)
print(f"  ok  line-height: {n} declarations folded -> 1 / 1.08 / 1.5 / 1.6 / 1.7")

# ── 2. TRACKING: 10 -> 5 (-.045 hero / -.02 display / .12 / .14 / .22)
LS = {".1em": ".12em", ".13em": ".14em", ".16em": ".14em",
      ".18em": ".22em", ".24em": ".22em", ".2em": ".22em",
      "-.025em": "-.02em", "-.005em": "-.02em"}
n = 0
for a, b in LS.items():
    pat = r"letter-spacing:\s*" + re.escape(a) + r"(?![0-9a-z])"
    n += count(pat)
    s = re.sub(pat, "letter-spacing:" + b, s)
print(f"  ok  letter-spacing: {n} declarations folded -> -.045 / -.02 / .12 / .14 / .22")

# ── 3. MOTION: 12 durations -> 3 (.3 fast / .6 base / .9 slow)
# never touch 0s or the 100s marquee
DUR = {".35s": ".3s", ".4s": ".3s", ".25s": ".3s",
       ".45s": ".6s", ".5s": ".6s", ".55s": ".6s", ".7s": ".6s", ".65s": ".6s",
       ".75s": ".9s", ".8s": ".9s", ".85s": ".9s", ".95s": ".9s",
       "1.05s": ".9s", "1.15s": ".9s", "1.4s": ".9s"}
n = 0
for a, b in DUR.items():
    pat = r"(?<![0-9.])" + re.escape(a) + r"(?![0-9])"
    n += count(pat)
    s = re.sub(pat, b, s)
print(f"  ok  transition: {n} durations folded -> .3s / .6s / .9s")

# ── 4. EASING: two near-identical expo curves -> one
before = count(r"cubic-bezier\(\.22,1,\.36,1\)")
s = s.replace("cubic-bezier(.22,1,.36,1)", "cubic-bezier(.16,1,.3,1)")
print(f"  ok  easing: {before} uses of the second expo curve folded into --ease")

# ── 5. AD-HOC FONT SIZES -> tokens
FS = {"font-size:.68rem": "font-size:var(--fs-micro)",
      "font-size:.7rem": "font-size:var(--fs-micro)",
      "font-size:.72rem": "font-size:var(--fs-micro)",
      "font-size:.92rem": "font-size:var(--fs-body)"}
n = 0
for a, b in FS.items():
    n += s.count(a)
    s = s.replace(a, b)
print(f"  ok  font-size: {n} ad-hoc values routed through tokens")

# ── 6. The one rounded pill group, squared to match everything else
n = s.count("border-radius:999px")
s = s.replace("border-radius:999px", "border-radius:0")
print(f"  ok  rounded pills squared ({n})")

# ── 7. Anchored content must clear the fixed nav
if "scroll-margin-top" not in s:
    anchor = "/* ══ Navigation: centred logo"
    if anchor not in s:
        anchor = ".nav{"
    s = s.replace(anchor,
        "/* Anchored sections must clear the fixed nav */\n"
        "section[id], [id^=work], [id^=studio], [id^=contact], [id^=aerial], [id^=product]{\n"
        "  scroll-margin-top:clamp(84px,9vw,112px);\n}\n\n" + anchor, 1)
    print("  ok  scroll-margin added for anchored sections")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
