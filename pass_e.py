# -*- coding: utf-8 -*-
"""Pass E — contact rebuilt, and a real footer.

The contact block was a headline, a paragraph and two buttons sitting in a lot
of empty navy. Now it is a band: the ask on the left, the enquiry on the
right, so the section does something instead of announcing something.

The footer takes the shape of the 'footercta' component — band over a base
carrying brand, navigation and legal — with none of its styling.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:150])
    s = s.replace(old, new, 1)
    print("  ok ", why)


CSS = """
/* ══ Contact band ═════════════════════════════════════════════════
   Layout from Goodwork Library v1.3.0 'footercta'; none of its styling.
   The ask sits beside the enquiry so the section works, not just talks. ══ */
.band{ display:grid; grid-template-columns:1.02fr .98fr; gap:clamp(2rem,5vw,5rem);
  align-items:start; border-top:1px solid var(--line); padding-top:clamp(2.4rem,5vw,4rem); }
.band__ask h2{ margin:0; }
.band__lede{ max-width:40ch; margin:clamp(1.1rem,2vw,1.6rem) 0 0;
  font-size:var(--fs-lead); line-height:1.6; color:var(--muted); }
.band__mail{ display:inline-flex; align-items:center; gap:.7rem;
  margin-top:clamp(1.6rem,3vw,2.4rem); padding-bottom:.5rem;
  border-bottom:1px solid var(--line); color:var(--cream);
  text-decoration:none; font-size:var(--fs-body);
  transition:border-color .4s var(--ease), color .4s var(--ease); }
.band__mail svg{ width:14px; height:10px; fill:none; stroke:currentColor; stroke-width:1.2; }
.band__mail:hover{ color:var(--gold); border-color:var(--gold); }
.band__facts{ display:grid; gap:0; margin:clamp(2rem,4vw,3rem) 0 0; }
.band__facts > div{ display:flex; justify-content:space-between; gap:1.5rem;
  padding:.85rem 0; border-top:1px solid var(--line-soft);
  font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.14em; text-transform:uppercase; }
.band__facts dt{ color:var(--muted-2); }
.band__facts dd{ margin:0; color:var(--cream); }
@media(max-width:900px){ .band{ grid-template-columns:1fr } }

/* ══ Footer ═══════════════════════════════════════════════════════
   Shape from 'footercta': a base carrying brand, nav and legal. ══ */
.foot{ margin-top:clamp(4rem,8vw,7rem); border-top:1px solid var(--line);
  padding:clamp(2.4rem,5vw,3.6rem) 0 clamp(2rem,4vw,3rem); }
.foot__top{ display:grid; grid-template-columns:1.3fr 1fr 1fr;
  gap:clamp(2rem,4vw,4rem); align-items:start; }
.foot__brand img{ width:clamp(200px,20vw,280px); height:auto; }
.foot__tag{ max-width:30ch; margin:clamp(1rem,2vw,1.5rem) 0 0;
  color:var(--muted); font-size:var(--fs-body); line-height:1.6; }
.foot__col h4{ margin:0 0 1.1rem; font-family:"Geist Mono",ui-monospace,monospace;
  font-size:var(--fs-micro); font-weight:400; letter-spacing:.18em;
  text-transform:uppercase; color:var(--muted-2); }
.foot__col a, .foot__col span{ display:block; padding:.34rem 0; color:var(--cream);
  text-decoration:none; font-size:var(--fs-body);
  transition:color .3s var(--ease); }
.foot__col a:hover{ color:var(--gold); }
.foot__base{ display:flex; flex-wrap:wrap; justify-content:space-between;
  gap:1rem 2rem; margin-top:clamp(2.4rem,5vw,4rem); padding-top:clamp(1.4rem,2.6vw,2rem);
  border-top:1px solid var(--line-soft);
  font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted-2); }
.foot__base a{ color:var(--muted-2); text-decoration:none; transition:color .3s; }
.foot__base a:hover{ color:var(--cream); }
@media(max-width:860px){ .foot__top{ grid-template-columns:1fr; gap:2.4rem } }
"""

sub("/* ══ Sticky horizontal scroll", CSS + "\n/* ══ Sticky horizontal scroll", "band + footer CSS")

# ── rebuild the contact inner: ask beside enquiry ────────────────────────
m = re.search(r'<div class="contact__inner">.*?\n      </div>\n', s, re.S)
if not m:
    raise SystemExit("MISS: contact__inner")

BAND = '''<div class="band">
        <div class="band__ask">
          <h2 id="contact-head" class="reveal">Have something<br />worth <em>filming?</em></h2>
          <p class="band__lede reveal">A launch, a delivery, a restoration coming off the bench.
          Tell me what it is and when it happens.</p>
          <!-- PLACEHOLDER: confirm the studio contact address before going live -->
          <a class="band__mail reveal" href="mailto:hello@higherheights.studio">
            hello@higherheights.studio
            <svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4"/></svg>
          </a>
          <dl class="band__facts reveal">
            <div><dt>Based</dt><dd>London</dd></div>
            <div><dt>Available</dt><dd>Worldwide</dd></div>
            <div><dt>Booking</dt><dd>2026 — open</dd></div>
            <div><dt>First reply</dt><dd>From Morgan, within a day</dd></div>
          </dl>
        </div>

        <div class="band__form">
'''
s = s[:m.start()] + BAND + s[m.end():]
print("  ok  contact band (ask | enquiry)")

# the enquiry moves inside the band's right column; drop its own top rule
sub('      <div class="enq reveal" id="enquiry">',
    '        <div class="enq reveal" id="enquiry">', "enquiry into the band")
sub('.enq{ border-top:1px solid var(--line); margin-top:clamp(3rem,6vw,5rem); padding-top:clamp(2.2rem,4vw,3.4rem); }',
    '.enq{ margin-top:0; }', "enquiry sits flush in the band")

# close the band's right column + the band itself, before the footer
sub('      <footer class="footer">',
    '        </div>\n      </div>\n\n      <footer class="footer">',
    "close band")

# ── replace the footer wholesale ─────────────────────────────────────────
m = re.search(r'<footer class="footer">.*?</footer>', s, re.S)
if not m:
    raise SystemExit("MISS: footer")

FOOTER = '''<footer class="foot">
        <div class="foot__top">
          <div class="foot__brand">
            <img src="assets/img/wordmark-cream.svg" width="1600" height="357"
                 alt="Higher Heights — Film, Aerial, Photography" loading="lazy" />
            <p class="foot__tag">Story-led films about extraordinary machines on land and sea,
            and the people who keep them alive.</p>
          </div>
          <nav class="foot__col" aria-label="Work">
            <h4>Work</h4>
            <a href="#work">Selected films</a>
            <a href="#aerial">Aerial</a>
            <a href="#product">Product &amp; stills</a>
            <a href="#studio">Studio</a>
          </nav>
          <div class="foot__col">
            <h4>Studio</h4>
            <a href="#enquiry">Start a project</a>
            <!-- PLACEHOLDER: confirm the studio contact address before going live -->
            <a href="mailto:hello@higherheights.studio">hello@higherheights.studio</a>
            <span>London · Worldwide</span>
            <span>Booking 2026</span>
          </div>
        </div>
        <div class="foot__base">
          <span>© <span id="year">2026</span> Higher Heights Films</span>
          <span>Film · Aerial · Photography</span>
          <span>Est. 2024</span>
        </div>
      </footer>'''

s = s[:m.start()] + FOOTER + s[m.end():]
print("  ok  footer rebuilt")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
