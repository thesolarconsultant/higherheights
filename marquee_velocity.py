# -*- coding: utf-8 -*-
"""Scroll-reactive marquee.

Two rows run opposite ways on a constant drift. Page scroll feeds velocity
into that drift, so the rail surges when you move and settles when you stop —
the logos behave like film passing a gate rather than a CSS loop.

Replaces the original site's CSS-animation marquee and its duplication script.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

# retire the old duplication + CSS keyframes
m = re.search(r'\s*/\* .{0,4} marquee: duplicate for a seamless loop.*?\n  if \(track\) track\.innerHTML \+= track\.innerHTML;\n', s, re.S)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    print("  ok  old duplication script removed")
s = re.sub(r"@keyframes marquee\{(?:[^{}]|\{[^}]*\})*\}", "", s)

JS = '''
  /* -- client marquee: two rows, opposite, scroll-reactive ------------
     Constant drift plus page-scroll velocity, so the rail surges as you
     move and settles when you stop. Honours reduced-motion. -- */
  (function () {
    const rows = [].slice.call(document.querySelectorAll(".marquee__track"));
    if (!rows.length) return;

    rows.forEach(function (row) {
      if (!row.dataset.doubled) {            // seamless loop needs a second copy
        row.innerHTML += row.innerHTML;
        row.dataset.doubled = "1";
      }
      row.dataset.offset = "0";
    });

    if (reduced) return;                      // static rows, no drift

    const DRIFT = 0.35;                       // px per frame at rest
    let lastY = window.scrollY, vel = 0, raf = 0, visible = true;

    const io = ("IntersectionObserver" in window)
      ? new IntersectionObserver(function (e) { visible = e[0].isIntersecting; },
                                 { threshold: 0 })
      : null;
    if (io) io.observe(rows[0].closest(".marquee") || rows[0]);

    function frame() {
      const y = window.scrollY;
      vel += (y - lastY) * 0.9;
      lastY = y;
      vel *= 0.90;                            // friction
      if (Math.abs(vel) < 0.01) vel = 0;

      if (visible) {
        rows.forEach(function (row) {
          const dir = +(row.dataset.dir || -1);
          const span = row.scrollWidth / 2;   // one copy's width
          if (!span) return;
          let off = parseFloat(row.dataset.offset) + (DRIFT + Math.abs(vel) * 0.14) * dir;
          if (off <= -span) off += span;      // wrap, both directions
          if (off >= 0 && dir > 0) off -= span;
          row.dataset.offset = off;
          row.style.transform = "translate3d(" + off.toFixed(2) + "px,0,0)";
        });
      }
      raf = requestAnimationFrame(frame);
    }

    // seed row 2 so it starts mid-span and runs the other way
    rows.forEach(function (row) {
      if (+(row.dataset.dir || -1) > 0) row.dataset.offset = -(row.scrollWidth / 2);
    });
    raf = requestAnimationFrame(frame);
    window.addEventListener("resize", function () {
      rows.forEach(function (r) { r.dataset.offset = "0"; });
    });
  })();
'''

anchor = re.search(r"^.*sticky horizontal scroll.*$", s, re.M)
if not anchor:
    raise SystemExit("MISS: anchor")
s = s[:anchor.start()] + JS + "\n" + s[anchor.start():]
print("  ok  scroll-reactive marquee wired")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
