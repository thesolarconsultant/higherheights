# -*- coding: utf-8 -*-
"""Watermarks: keep the majority of the mark on screen at every breakpoint.

Measured before:
             desktop  tablet  mobile
  studio       35%      42%     43%
  contact      57%      55%     50%

The cause is percentage offsets on the vertical axis. `bottom:-14%` resolves
against the SECTION's height, and the studio section is 2252px tall, so the
mark was pushed 315px below its own container. The horizontal offsets had the
same problem in miniature.

Fixed offsets in px behave predictably: the bleed is a constant edge, not a
function of how tall the section happens to be. Scaled down at narrow widths
so a smaller mark does not lose proportionally more.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

OLD_DESK_STUDIO = ".hh-wm--studio{ right:-6%; bottom:-14%; width:min(42%,460px); opacity:.055; }"
OLD_DESK_CONTACT = ".hh-wm--contact{ left:-7%; top:-10%; width:min(38%,420px); opacity:.07; }"

NEW_DESK = (
    ".hh-wm--studio{ right:-26px; bottom:-32px; width:min(42%,460px); opacity:.055; }\n"
    ".hh-wm--contact{ left:-26px; top:-30px; width:min(38%,420px); opacity:.07; }"
)

assert OLD_DESK_STUDIO in s, "MISS studio"
assert OLD_DESK_CONTACT in s, "MISS contact"
s = s.replace(OLD_DESK_STUDIO + "\n" + OLD_DESK_CONTACT, NEW_DESK, 1)
print("  ok  desktop/tablet offsets -> px (was % of section height)")

OLD_MOB = (
    "  .hh-wm--studio{ right:-16%; bottom:-6%; width:min(62%,300px); opacity:.05; }\n"
    "  .hh-wm--contact{ left:-18%; top:-4%; width:min(58%,280px); opacity:.06; }"
)
NEW_MOB = (
    "  .hh-wm--studio{ right:-14px; bottom:-18px; width:min(58%,280px); opacity:.05; }\n"
    "  .hh-wm--contact{ left:-14px; top:-16px; width:min(54%,260px); opacity:.06; }"
)
assert OLD_MOB in s, "MISS mobile block"
s = s.replace(OLD_MOB, NEW_MOB, 1)
print("  ok  mobile offsets scaled to the smaller mark")

# A section that is shorter than the mark would still clip it; cap the mark
# against its own section so it can never exceed what there is room for.
EXTRA = """
/* The mark never grows past the room its section actually has */
.hh-wm{ max-height:76%; max-width:min(46%,480px); }
.hh-wm img{ object-fit:contain; max-height:100%; }
"""
s = s.replace(".hh-wm img{ display:block; width:100%; height:auto; }",
              ".hh-wm img{ display:block; width:100%; height:auto; }" + EXTRA, 1)
print("  ok  mark capped against its own section box")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
