# -*- coding: utf-8 -*-
"""Touch: let the stills strip scroll, and stop pinning on touch devices.

Two faults, both mine.

1. `.strip{ touch-action: pan-y }` -- added so dragging the strip would not
   hijack vertical page scrolling. pan-y tells the browser to handle ONLY
   vertical gestures on that element, so horizontal swipe was disabled
   outright. On a phone or iPad the strip could not be moved at all.
   `pan-x pan-y` allows both: the browser scrolls the strip sideways and the
   page vertically, natively.

2. The pin released below 760px, but iPad portrait is 768px -- so a touch
   device got the desktop sticky-scroll treatment, where a scroll-driven
   horizontal transform fights native momentum scrolling. The release now
   keys off a coarse pointer as well as width, so every touch device gets
   the swipe carousel and only mice get the pin.

Also: the JS pointer-drag is skipped for touch input. It exists to give mice
a grab-and-throw; on touch it competes with the browser's own scrolling.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

# ── 1. allow horizontal touch scrolling on the strip ──
OLD = "touch-action:pan-y;                 /* page still scrolls vertically */"
NEW = ("touch-action:pan-x pan-y;           /* swipe the strip, scroll the page */\n"
       "  -webkit-overflow-scrolling:touch;   /* momentum on iOS */\n"
       "  overscroll-behavior-x:contain;      /* no back-swipe navigation */")
assert OLD in s, "MISS touch-action"
s = s.replace(OLD, NEW, 1)
print("  ok  strip: touch-action pan-y -> pan-x pan-y (+ iOS momentum)")

# ── 2. release the pin on any touch device, not just narrow ones ──
OLD = "if (reduced || window.innerWidth < 760) {"
NEW = ("var coarse = window.matchMedia('(pointer: coarse)').matches;\n"
       "      if (reduced || coarse || window.innerWidth < 760) {")
assert OLD in s, "MISS pin guard"
s = s.replace(OLD, NEW, 1)
print("  ok  pin: released on coarse pointer (covers iPad at 768px)")

# ── 3. the mouse drag must not fight native touch scrolling ──
#     find the pointerdown handler on the carousel and bail for touch
CAND = [
  'strip.addEventListener("pointerdown", function (e) {',
  'el.addEventListener("pointerdown", function (e) {',
  '.addEventListener("pointerdown", function (e) {',
]
done = False
for c in CAND:
    if c in s:
        s = s.replace(c, c + '\n      if (e.pointerType === "touch") return;  /* let the browser scroll it */', 1)
        print(f"  ok  drag: skipped for touch input")
        done = True
        break
if not done:
    print("  --  no pointerdown handler found to guard")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
