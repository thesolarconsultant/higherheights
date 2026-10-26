# -*- coding: utf-8 -*-
"""Pass D — sticky horizontal scroll + a logo marquee.

Product stills: the section pins and the stills travel sideways as you scroll
down. Mechanic adapted from Goodwork Library 'storypinned', driven on the X
axis instead of swapping chapters.

Client logos: a continuous marquee in two rows running opposite ways, held
still under the pointer. Colour-on-hover is kept.

Both degrade: under reduced-motion or below 760px the pin releases and the
existing drag carousel takes over, so nothing is lost.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why, count=1):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:150])
    s = s.replace(old, new, count)
    print("  ok ", why)


CSS = """
/* ══ Sticky horizontal scroll ═════════════════════════════════════
   Mechanic adapted from Goodwork Library v1.3.0 'storypinned', run on the
   X axis: the section pins and the stills travel sideways. ══ */
.pin{ position:relative; }
.pin__stage{ position:sticky; top:0; height:100svh; min-height:520px;
  overflow:hidden; display:flex; flex-direction:column; justify-content:center; }
.pin:not(.pin--off) .strip{ overflow:visible; scroll-snap-type:none;
  cursor:default; padding-bottom:0; }
.pin:not(.pin--off) .carousel__foot{ display:none; }
.pin__row{ will-change:transform; padding-inline:var(--pad); }
.pin__row figure{ width:clamp(210px,23vw,340px); }
.pin__meter{ position:absolute; left:var(--pad); right:var(--pad);
  bottom:clamp(2.2rem,5vh,3.6rem); height:1px; background:var(--line-soft); }
.pin__meter i{ position:absolute; left:0; top:-1px; height:3px; width:100%;
  background:var(--gold); transform-origin:left center; transform:scaleX(0); }
.pin__hint{ position:absolute; left:var(--pad); bottom:clamp(3.6rem,7.5vh,5.4rem);
  font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.18em; text-transform:uppercase; color:var(--muted-2); }
.pin--off .pin__stage{ position:static; height:auto; min-height:0; overflow:visible; }
.pin--off .pin__meter,.pin--off .pin__hint{ display:none; }

/* ══ Logo marquee ═════════════════════════════════════════════════ */
.marq{ position:relative; overflow:hidden;
  -webkit-mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);
          mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent); }
.marq__row{ display:flex; width:max-content; align-items:center;
  gap:clamp(2.4rem,5vw,4.6rem); animation:marq 52s linear infinite; }
.marq__row + .marq__row{ animation-duration:66s; animation-direction:reverse;
  margin-top:clamp(1.8rem,3.2vw,2.8rem); }
.marq:hover .marq__row{ animation-play-state:paused; }
@keyframes marq{ from{transform:translateX(0)} to{transform:translateX(-50%)} }
@media (prefers-reduced-motion:reduce){
  .marq__row{ animation:none }
  .marq{ overflow-x:auto; -webkit-mask:none; mask:none }
}
"""

JS = """
  /* ── sticky horizontal scroll ─────────────────────────── */
  document.querySelectorAll("[data-pin]").forEach(function (pin) {
    const row = pin.querySelector(".pin__row");
    const bar = pin.querySelector(".pin__meter i");
    if (!row) return;

    function travel() {
      return Math.max(0, row.scrollWidth - pin.clientWidth);
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
      // narrow screen or motion unwelcome: release the pin, drag carousel returns
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
    size();
  });

  /* ── marquee: duplicate each row so the loop is seamless ── */
  document.querySelectorAll(".marq__row").forEach(function (row) {
    row.innerHTML += row.innerHTML;
  });
"""

sub("/* ══ Client wall", CSS + "\n/* ══ Client wall", "pin + marquee CSS")

# ── close .wrap early, open .pin > .pin__stage around the carousel ────────
sub('      <div class="carousel" data-carousel>\n      <div class="strip" id="strip"',
    '      </div>\n\n'
    '    <div class="pin" data-pin>\n'
    '      <div class="pin__stage">\n'
    '      <div class="carousel" data-carousel>\n'
    '      <div class="strip pin__row" id="strip"',
    "open pin + stage")

sub('      <div class="carousel__foot">',
    '      <div class="pin__meter" aria-hidden="true"><i></i></div>\n'
    '      <span class="pin__hint">Scroll</span>\n'
    '      <div class="carousel__foot">',
    "meter + hint")

# ── close stage and pin, then re-open a wrap for the note ────────────────
sub("""      <p class="product__note mono mono--dim">
        Stills and product film from the Richard Mille RM 69 shoot.
      </p>
    </div>
  </section>""",
"""      </div>
    </div>

    <div class="wrap">
      <p class="product__note mono mono--dim">
        Stills and product film from the Richard Mille RM 69 shoot.
      </p>
    </div>
  </section>""",
    "close pin, rewrap the note")

# ── client wall grid becomes two marquee rows ────────────────────────────
import re
m = re.search(r'<div class="clients__grid reveal">(.*?)\n      </div>', s, re.S)
if not m:
    raise SystemExit("MISS: clients grid")
cards = re.findall(r'<div class="client" style=.*?</div>', m.group(1), re.S)
if len(cards) != 14:
    raise SystemExit(f"expected 14 logos, found {len(cards)}")
half = (len(cards) + 1) // 2


def row(items):
    return ('        <div class="marq__row">\n'
            + "\n".join("  " + c for c in items)
            + "\n        </div>")


marq = ('<div class="marq reveal">\n'
        + row(cards[:half]) + "\n"
        + row(cards[half:]) + "\n"
        + "      </div>")
s = s[:m.start()] + marq + s[m.end():]
print(f"  ok  marquee: {half} + {len(cards)-half} logos in two rows")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
