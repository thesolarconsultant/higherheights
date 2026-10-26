# -*- coding: utf-8 -*-
"""The nav pill adapts to the section beneath it.

It is a dark green pill at 82% over whatever is behind. On the dark sections
that reads correctly. Over the two cream sections it sits as a murky patch
with blurred text showing through.

Now it detects the ground under the nav and inverts: cream pill, ink type,
on light sections. One class, swapped on scroll.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

CSS = """
/* Nav over a light section: invert rather than muddy it */
.nav--light .nav__inner{
  background:rgba(233,229,219,.94) !important;
  border-color:rgba(5,16,13,.14) !important;
}
.nav--light .nav__inner a,
.nav--light .nav__inner button,
.nav--light .nav__fold,
.nav--light .brand__wm,
.nav--light .nav__side a{ color:var(--ink); }
.nav--light .brand img,
.nav--light .nav__inner img{ filter:invert(1) brightness(.18); }
.nav--light .nav__plus,
.nav--light .nav__plus::before,
.nav--light .nav__plus::after{ background:var(--ink); border-color:var(--ink); }
"""

anchor = "/* Anchored sections must clear the fixed nav */"
if anchor not in s:
    anchor = ".nav{"
s = s.replace(anchor, CSS + "\n" + anchor, 1)
print("  ok  inverted-nav CSS")

JS = '''
  /* -- nav inverts over light sections ------------------------------- */
  (function () {
    const nav = document.querySelector("header.nav, .nav");
    if (!nav) return;
    const LIGHT = ".band-cream, .studio, .clients--light, [data-ground=light]";
    let ticking = false;

    function test() {
      ticking = false;
      const r = nav.getBoundingClientRect();
      const y = r.bottom - 6;
      // sample three points so a narrow pill cannot miss the section
      const xs = [window.innerWidth * 0.5, window.innerWidth * 0.18, window.innerWidth * 0.82];
      let light = false;
      for (const x of xs) {
        const stack = document.elementsFromPoint(x, y) || [];
        for (const el of stack) {
          if (el.closest && el.closest("header.nav, .nav")) continue;
          if (el.closest && el.closest(LIGHT)) { light = true; break; }
          // first real ground element wins
          const bg = getComputedStyle(el).backgroundColor;
          if (bg && !/rgba\\(0, 0, 0, 0\\)/.test(bg)) {
            const m = bg.match(/\\d+/g);
            if (m) {
              const lum = (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255;
              if (lum > 0.6) light = true;
            }
            break;
          }
        }
        if (light) break;
      }
      nav.classList.toggle("nav--light", light);
    }

    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(test); }
    }, { passive: true });
    window.addEventListener("resize", test);
    test();
  })();
'''

m = re.search(r"^.*client marquee: two rows.*$", s, re.M)
if not m:
    m = re.search(r"^.*sticky horizontal scroll.*$", s, re.M)
if not m:
    raise SystemExit("MISS: js anchor")
s = s[:m.start()] + JS + "\n" + s[m.start():]
print("  ok  inverted-nav script")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
