# -*- coding: utf-8 -*-
"""Bring the hero's top strip to life.

It was two static labels. Now:
  left  — the disciplines, with a slow light passing through them
  right — a LIVE London clock and a real availability state, and it is a link
          to contact rather than a label that does nothing.

A working studio showing its own local time is a real detail that changes.
Restrained on purpose: brief rule 'no gimmicks, no trend styling'.
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


# ── CSS ───────────────────────────────────────────────────────────────────
sub(""".hero__top{ display:flex; justify-content:space-between; align-items:flex-start; gap:2rem; }
.hero__top .mono{ color:var(--gold); }""",
""".hero__top{ display:flex; justify-content:space-between; align-items:center; gap:2rem; }
.hero__top .mono{ color:var(--gold); }

/* the disciplines: a light passes along them, slowly */
.hero__disc{ display:inline-flex; align-items:center; gap:.62em; }
.hero__disc i{ font-style:normal; opacity:.55; animation:disc-pass 9s linear infinite; }
.hero__disc i:nth-of-type(2){ animation-delay:.5s; }
.hero__disc i:nth-of-type(3){ animation-delay:1s; }
.hero__disc b{ font-weight:400; opacity:.3; }
@keyframes disc-pass{ 0%,22%{opacity:.55} 7%{opacity:1} }

/* a live state, and somewhere to click */
.hero__status{
  display:inline-flex; align-items:center; gap:.75em;
  text-decoration:none; color:var(--gold);
  transition:color .4s var(--ease);
}
.hero__status:hover{ color:var(--cream); }
.hero__status:focus-visible{ outline:1px solid var(--gold); outline-offset:4px; }
.hero__clock{ font-variant-numeric:tabular-nums; opacity:.62; }
.hero__sep{ opacity:.3; }
.hero__avail{ display:inline-flex; align-items:center; gap:.6em; }
.hero__avail i{
  position:relative; width:5px; height:5px; flex:none;
  background:var(--gold); border-radius:50%;
}
.hero__avail i::after{
  content:""; position:absolute; inset:0; border-radius:inherit;
  background:inherit; animation:avail-breathe 3.4s var(--ease) infinite;
}
@keyframes avail-breathe{ 0%{transform:scale(1);opacity:.65} 70%,100%{transform:scale(3.2);opacity:0} }
@media(max-width:700px){ .hero__clock,.hero__sep{ display:none } }
@media (prefers-reduced-motion:reduce){
  .hero__disc i{ animation:none; opacity:.85 }
  .hero__avail i::after{ animation:none; display:none }
}""",
    "hero strip CSS")

# ── markup ────────────────────────────────────────────────────────────────
sub("""        <span class="mono">Film · Aerial · Photography</span>
        <span class="mono mono--dim">Available for commission</span>""",
"""        <span class="mono hero__disc" aria-label="Film, aerial and photography">
          <i>Film</i><b aria-hidden="true">·</b><i>Aerial</i><b aria-hidden="true">·</b><i>Photography</i>
        </span>
        <a class="mono hero__status" href="#contact">
          <span class="hero__clock" id="ukClock" aria-label="Current time in London">--:--</span>
          <span class="hero__sep" aria-hidden="true">·</span>
          <span class="hero__avail"><i aria-hidden="true"></i>Available for commission</span>
        </a>""",
    "hero strip markup")

# ── the clock ─────────────────────────────────────────────────────────────
sub("  /* ── scroll carousel ──────────────────────────────────",
"""  /* ── live London clock in the hero strip ─────────────── */
  (function () {
    const el = document.getElementById("ukClock");
    if (!el) return;
    function tick() {
      try {
        el.textContent = new Intl.DateTimeFormat("en-GB", {
          hour: "2-digit", minute: "2-digit", hour12: false,
          timeZone: "Europe/London",
        }).format(new Date()) + " London";
      } catch (err) {
        el.remove();                      // no Intl support: drop it silently
        return;
      }
      setTimeout(tick, 15000);
    }
    tick();
  })();

  /* ── scroll carousel ──────────────────────────────────""",
    "live clock")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
