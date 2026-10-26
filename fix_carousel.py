# -*- coding: utf-8 -*-
"""Replace the product strip's drag handler with a proper scroll carousel.

The old one locked because:
  1. `pointerleave` fired while the pointer was CAPTURED, setting down=false
     mid-drag, so pointerup never cleaned up and `.is-dragging` stuck.
  2. With `.is-dragging` stuck off, `scroll-snap-type:x mandatory` re-engaged
     during the drag and yanked the strip back to a card edge.
  3. Nothing called preventDefault, so the browser started a text/image
     selection instead — the highlighted caption in the screenshot.

This is written as a generic `[data-carousel]` so any future carousel gets
the same behaviour.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:140])
    s = s.replace(old, new, 1)
    print("  ok ", why)


# ── 1. CSS: proximity snap (mandatory fights the drag), no text selection,
#         vertical page scroll preserved on touch, plus arrows and a track ──
sub(""".strip{
  display:flex; gap:clamp(.8rem,1.4vw,1.3rem);
  overflow-x:auto; scroll-snap-type:x mandatory;
  padding-bottom:1.2rem;
  scrollbar-width:thin; scrollbar-color:var(--line) transparent;
  cursor:grab;
}
.strip.is-dragging{ cursor:grabbing; scroll-snap-type:none; }""",
""".carousel{ position:relative; }
.strip{
  display:flex; gap:clamp(.8rem,1.4vw,1.3rem);
  overflow-x:auto; scroll-snap-type:x proximity;
  padding-bottom:1.2rem;
  scrollbar-width:none; cursor:grab;
  touch-action:pan-y;                 /* page still scrolls vertically */
  -webkit-user-select:none; user-select:none;
  overscroll-behavior-x:contain;
}
.strip::-webkit-scrollbar{ display:none; }
.carousel.is-dragging .strip{ cursor:grabbing; scroll-snap-type:none; }
.strip img{ -webkit-user-drag:none; user-drag:none; }

.carousel__foot{
  display:flex; align-items:center; gap:clamp(.9rem,2vw,1.6rem);
  margin-top:clamp(.9rem,1.8vw,1.4rem);
}
.carousel__arrow{
  flex:0 0 auto; width:34px; height:34px; display:grid; place-items:center;
  background:none; border:1px solid var(--line); color:var(--cream);
  cursor:pointer; transition:border-color .3s var(--ease), opacity .3s, color .3s;
}
.carousel__arrow svg{ width:13px; height:10px; fill:none; stroke:currentColor; stroke-width:1.2; }
.carousel__arrow:hover:not(:disabled){ border-color:var(--gold); color:var(--gold); }
.carousel__arrow:disabled{ opacity:.28; cursor:default; }
.carousel__arrow:focus-visible{ outline:1px solid var(--gold); outline-offset:3px; }
.carousel__prog{ flex:1 1 auto; height:1px; background:var(--line-soft); position:relative; }
.carousel__bar{
  position:absolute; left:0; top:-1px; height:3px; background:var(--gold);
  width:100%; transform-origin:left center; transform:scaleX(0);
  transition:transform .18s linear;
}
@media (prefers-reduced-motion:reduce){ .carousel__bar{ transition:none } }""",
    "carousel CSS")

# ── 2. wrap the strip and give it a foot ──
sub('      <div class="strip" id="strip" tabindex="0" role="group" aria-label="Richard Mille RM 69 stills gallery">',
    '      <div class="carousel" data-carousel>\n'
    '      <div class="strip" id="strip" tabindex="0" role="group" aria-label="Richard Mille RM 69 stills gallery">',
    "open .carousel wrapper")

ARROW_L = '<svg viewBox="0 0 13 10" aria-hidden="true"><path d="M13 5H1M5 1L1 5l4 4"/></svg>'
ARROW_R = '<svg viewBox="0 0 13 10" aria-hidden="true"><path d="M0 5h12M8 1l4 4-4 4"/></svg>'

# the strip closes just before the section's figcaption/closing wrap
OLD_CLOSE = """      </div>
"""
# anchor on the element that follows the strip
import re
m = re.search(r'(<div class="strip" id="strip".*?)(\n\s*</div>)(\s*\n\s*<p class="strip__note")',
              s, re.S)
if not m:
    # fall back: find the strip block and the first </div> after its last figure
    m = re.search(r'(<div class="strip" id="strip".*?</figure>\s*)(</div>)', s, re.S)
    if not m:
        raise SystemExit("MISS: could not find the strip's closing tag")
    s = s[:m.end(2)] + (
        '\n      <div class="carousel__foot">\n'
        f'        <button class="carousel__arrow" type="button" data-dir="-1" aria-label="Previous stills">{ARROW_L}</button>\n'
        '        <div class="carousel__prog"><span class="carousel__bar"></span></div>\n'
        f'        <button class="carousel__arrow" type="button" data-dir="1" aria-label="Next stills">{ARROW_R}</button>\n'
        '      </div>\n      </div>'
    ) + s[m.end(2):]
    print("  ok  carousel foot + close wrapper")
else:
    raise SystemExit("unexpected markup shape — inspect manually")

# ── 3. replace the drag handler wholesale ──
OLD_JS_START = '  /* ── draggable product strip ─────────────────────────── */'
i = s.find(OLD_JS_START)
if i < 0:
    raise SystemExit("MISS: drag handler block")
j = s.find("\n  }\n", s.find('strip.addEventListener("keydown"', i))
if j < 0:
    raise SystemExit("MISS: end of drag handler block")
j += len("\n  }\n")

NEW_JS = '''  /* ── scroll carousel ──────────────────────────────────
     Drag, inertia, snap, arrows and a progress bar.
     No pointerleave handler: with setPointerCapture it fires mid-drag,
     desyncs the dragging state and re-engages snap — that was the lock. */
  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    const track = root.querySelector(".strip");
    const bar   = root.querySelector(".carousel__bar");
    const arrows = root.querySelectorAll(".carousel__arrow");
    if (!track) return;

    let down = false, pid = null, startX = 0, startLeft = 0, moved = 0;
    let lastX = 0, lastT = 0, vx = 0, raf = 0;

    const maxScroll = () => Math.max(1, track.scrollWidth - track.clientWidth);

    function step() {
      const card = track.querySelector("figure");
      if (!card) return 260;
      const gap = parseFloat(getComputedStyle(track).gap) || 0;
      return card.getBoundingClientRect().width + gap;
    }

    function paint() {
      const p = Math.min(1, Math.max(0, track.scrollLeft / maxScroll()));
      if (bar) bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
      arrows.forEach(function (a) {
        const dir = +a.dataset.dir;
        a.disabled = dir < 0 ? track.scrollLeft < 2
                             : track.scrollLeft > maxScroll() - 2;
      });
    }
    track.addEventListener("scroll", paint, { passive: true });
    window.addEventListener("resize", paint);
    paint();

    function snap() {
      const w = step();
      track.scrollTo({ left: Math.round(track.scrollLeft / w) * w,
                       behavior: reduced ? "auto" : "smooth" });
    }

    function glide() {
      vx *= 0.94;
      track.scrollLeft -= vx * 16;
      if (Math.abs(vx) > 0.02 && track.scrollLeft > 0 && track.scrollLeft < maxScroll()) {
        raf = requestAnimationFrame(glide);
      } else { snap(); }
    }

    track.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      cancelAnimationFrame(raf);
      down = true; pid = e.pointerId; moved = 0; vx = 0;
      startX = lastX = e.clientX; startLeft = track.scrollLeft;
      lastT = performance.now();
      root.classList.add("is-dragging");
      try { track.setPointerCapture(pid); } catch (err) {}
    });

    track.addEventListener("pointermove", function (e) {
      if (!down || e.pointerId !== pid) return;
      const dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      if (moved <= 4) return;
      e.preventDefault();                      // stop selection / image drag
      track.scrollLeft = startLeft - dx;
      const now = performance.now(), dt = now - lastT;
      if (dt > 0) { vx = (e.clientX - lastX) / dt; lastX = e.clientX; lastT = now; }
    });

    function release(e) {
      if (!down) return;
      down = false;
      try { if (pid !== null && track.hasPointerCapture(pid)) track.releasePointerCapture(pid); } catch (err) {}
      pid = null;
      root.classList.remove("is-dragging");
      if (!reduced && Math.abs(vx) > 0.05) glide(); else snap();
    }
    track.addEventListener("pointerup", release);
    track.addEventListener("pointercancel", release);

    // a drag that ends on a card must not open it
    track.addEventListener("click", function (e) {
      if (moved > 4) { e.preventDefault(); e.stopPropagation(); }
    }, true);

    arrows.forEach(function (a) {
      a.addEventListener("click", function () {
        track.scrollBy({ left: (+a.dataset.dir) * step(),
                         behavior: reduced ? "auto" : "smooth" });
      });
    });

    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); track.scrollBy({ left: step(), behavior: reduced ? "auto" : "smooth" }); }
      if (e.key === "ArrowLeft")  { e.preventDefault(); track.scrollBy({ left: -step(), behavior: reduced ? "auto" : "smooth" }); }
    });

    // trackpad horizontal only — never hijack the page's vertical scroll
    track.addEventListener("wheel", function (e) {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
        e.preventDefault(); track.scrollLeft += e.deltaX;
      }
    }, { passive: false });
  });
'''

s = s[:i] + NEW_JS + s[j:]
print("  ok  drag handler -> scroll carousel")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
