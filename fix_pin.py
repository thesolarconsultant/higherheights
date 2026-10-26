# -*- coding: utf-8 -*-
"""Pass D's JavaScript was never inserted.

pass_d.py built the CSS and the markup and defined the behaviour in a `JS`
variable — then only ever substituted the CSS. The pin had styling and
structure but nothing driving it, which is why travel stayed 0, the meter
never filled, and the marquee rows were never duplicated for a seamless loop.

Also fixes the measurement the pin would have used: scrollWidth only exceeds
clientWidth on a scroll container, and the pin sets the row to overflow:visible.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

if "data-pin" not in s:
    raise SystemExit("no pin markup found")
if "function travel" in s:
    raise SystemExit("pin JS already present - nothing to do")

JS = """
  /* -- sticky horizontal scroll -----------------------------------
     Mechanic adapted from Goodwork Library v1.3.0 'storypinned',
     driven on the X axis. -- */
  document.querySelectorAll("[data-pin]").forEach(function (pin) {
    const row = pin.querySelector(".pin__row");
    const bar = pin.querySelector(".pin__meter i");
    if (!row) return;

    function travel() {
      // offsetWidth, not scrollWidth: the row is overflow:visible inside the
      // pin, so scrollWidth collapses to the padding box and reports 0.
      const content = Math.max(row.offsetWidth, row.scrollWidth);
      return Math.max(0, content - pin.clientWidth);
    }

    function draw() {
      if (pin.classList.contains("pin--off")) return;
      const span = pin.offsetHeight - window.innerHeight;
      const p = span > 0
        ? Math.min(1, Math.max(0, -pin.getBoundingClientRect().top / span)) : 0;
      row.style.transform = "translate3d(" + (-p * travel()) + "px,0,0)";
      if (bar) bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    }

    function size() {
      // narrow screen or motion unwelcome: release the pin and let the
      // existing drag carousel take over
      if (reduced || window.innerWidth < 760) {
        pin.classList.add("pin--off");
        pin.style.height = "";
        row.style.transform = "";
        return;
      }
      pin.classList.remove("pin--off");
      pin.style.height = (window.innerHeight + travel()) + "px";
      draw();
    }

    window.addEventListener("scroll", draw, { passive: true });
    window.addEventListener("resize", size);
    window.addEventListener("load", size);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(size);
    size();
  });

  /* -- marquee: duplicate each row so the loop is seamless -- */
  document.querySelectorAll(".marq__row").forEach(function (row) {
    if (row.dataset.doubled) return;
    row.innerHTML += row.innerHTML;
    row.dataset.doubled = "1";
  });
"""

import re
m = re.search(r"^.*live London clock in the hero strip.*$", s, re.M)
if not m:
    raise SystemExit("MISS: clock anchor")
s = s[:m.start()] + JS + "\n" + s[m.start():]
print("  ok  pin + marquee JS injected")

open(p, "w", encoding="utf-8").write(s)
print(f"written: {start} -> {len(s)} bytes")
