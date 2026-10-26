# -*- coding: utf-8 -*-
"""Rebuild the contact block on the bones of Goodwork Library 'footercta'.

Taken:   the layout (eyebrow / title / lede / actions / side panel / base)
         and the reveal-on-scroll entrance.
Dropped: the blue-pink gradient, Poppins 800, pill buttons, frosted glass,
         26px corners, chat bubbles, the ping dot and the coral accent —
         every one of them is on Morgan's ban list.

The chat becomes a piece of correspondence, because 'a personal reply from
Morgan, not a form' (brief §17) is the thing actually worth showing.
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
sub(".contact{ padding:var(--sect) 0 0; position:relative; overflow:hidden; }",
""".contact{ padding:var(--sect) 0 0; position:relative; overflow:hidden; }

/* Layout from Goodwork Library v1.3.0 'footercta'. Its styling is not used:
   no gradients, no pills, no glass, no rounded corners. */
.contact__lede{
  max-width:46ch; margin:clamp(1.1rem,2vw,1.6rem) 0 0;
  font-size:var(--fs-lead); line-height:1.6; color:var(--muted);
}
.contact__actions{ display:flex; flex-wrap:wrap; align-items:center; gap:clamp(.7rem,1.4vw,1rem); margin-top:clamp(1.6rem,3vw,2.3rem); }
.cbtn{
  display:inline-flex; align-items:center; gap:.7rem; height:52px; padding:0 1.6rem;
  border:1px solid var(--line); color:var(--cream); text-decoration:none;
  font-size:var(--fs-body); letter-spacing:.01em;
  transition:border-color .4s var(--ease), color .4s var(--ease), background .4s var(--ease);
}
.cbtn svg{ width:14px; height:10px; fill:none; stroke:currentColor; stroke-width:1.2; }
.cbtn:hover{ border-color:var(--gold); color:var(--gold); }
.cbtn--main{ background:var(--cream); color:var(--navy); border-color:var(--cream); }
.cbtn--main:hover{ background:var(--gold); border-color:var(--gold); color:var(--navy); }
.cbtn:focus-visible{ outline:1px solid var(--gold); outline-offset:3px; }
.contact__open{ font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted-2); }

/* the exchange — correspondence, not chat bubbles */
.letter{ border-top:1px solid var(--line); padding-top:clamp(1.2rem,2.2vw,1.7rem); margin-bottom:clamp(1.8rem,3.4vw,2.6rem); }
.letter__q{
  font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.12em; text-transform:uppercase; color:var(--muted-2);
  line-height:1.8; max-width:34ch;
}
.letter__a{
  margin:clamp(.9rem,1.6vw,1.2rem) 0 0;
  font-family:"Instrument Serif",Georgia,serif; font-weight:400;
  font-size:clamp(1.05rem,1.5vw,1.35rem); line-height:1.42; color:var(--cream);
  max-width:38ch; text-wrap:pretty;
}
.letter__by{ display:flex; align-items:center; gap:.6rem; margin-top:clamp(.8rem,1.4vw,1.1rem); }
.letter__by i{ width:18px; height:1px; background:var(--gold); flex:none; }
.letter__by span{ font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
@media(max-width:860px){ .letter__q,.letter__a{ max-width:none } }""",
    "contact CTA styles")

# ── markup: lede + actions ────────────────────────────────────────────────
sub("""          <h2 id="contact-head" class="reveal">Have something<br />worth <em>filming?</em></h2>
          <!-- PLACEHOLDER: confirm the studio contact address before going live -->
          <a class="contact__mail reveal" href="mailto:hello@higherheights.studio">
            hello@higherheights.studio
            <svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4"/></svg>
          </a>""",
"""          <h2 id="contact-head" class="reveal">Have something<br />worth <em>filming?</em></h2>
          <p class="contact__lede reveal">Tell me what you have and when it happens — a launch, a delivery,
          a restoration coming off the bench. The first reply is mine, not a form.</p>

          <div class="contact__actions reveal">
            <!-- PLACEHOLDER: confirm the studio contact address before going live -->
            <a class="cbtn cbtn--main" href="mailto:hello@higherheights.studio">
              Start a project
              <svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4"/></svg>
            </a>
            <a class="cbtn" href="#work">See the work</a>
            <span class="contact__open">Booking 2026</span>
          </div>

          <!-- PLACEHOLDER: confirm the studio contact address before going live -->
          <a class="contact__mail reveal" href="mailto:hello@higherheights.studio">
            hello@higherheights.studio
            <svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4"/></svg>
          </a>""",
    "lede + actions")

# ── markup: the exchange, above the details ───────────────────────────────
sub("""        <div class="contact__side reveal">
          <dl>""",
"""        <div class="contact__side reveal">
          <div class="letter">
            <p class="letter__q">&ldquo;We have a 1973 restoration coming off the bench in March.
            Is there a film in it?&rdquo;</p>
            <p class="letter__a">Almost always &mdash; though rarely the one people expect. Who has been
            turning the spanners for the last two years? Start there and the car tells its own story.</p>
            <div class="letter__by"><i aria-hidden="true"></i><span>Morgan &middot; Founder</span></div>
          </div>
          <dl>""",
    "the exchange")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
