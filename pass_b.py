# -*- coding: utf-8 -*-
"""Pass B — the enquiry.

'quizfocus' gives the shape: one question per screen, large type, Enter to
carry on, a progress rail.
'formbudget' gives the substance: a budget slider whose band explains in
plain English what that money actually buys.

They are merged into ONE flow. Two separate enquiry forms on a single page
would compete; the budget becomes a step inside the questionnaire.

Bands are written to Morgan's real ladder (brief §14), not the library's
trades pricing.
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


CSS = """
/* ══ Enquiry ══════════════════════════════════════════════════════
   Shape from Goodwork Library v1.3.0 'quizfocus', budget band logic from
   'formbudget'. Styling is not theirs: no pills, no gradients, no glass,
   no rounded corners. ══ */
.enq{ border-top:1px solid var(--line); margin-top:clamp(3rem,6vw,5rem); padding-top:clamp(2.2rem,4vw,3.4rem); }
.enq__rail{ display:flex; gap:6px; margin-bottom:clamp(1.8rem,3.4vw,2.6rem); }
.enq__rail i{ flex:1; height:1px; background:var(--line-soft); transition:background .5s var(--ease); }
.enq__rail i.is-done{ background:var(--gold); }
.enq__screen{ display:none; }
.enq__screen.is-on{ display:block; animation:enq-in .55s var(--ease) both; }
@keyframes enq-in{ from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:none} }
.enq__q{ font-family:"Instrument Serif",Georgia,serif; font-weight:400;
  font-size:clamp(1.6rem,3.2vw,2.8rem); line-height:1.08; letter-spacing:-.02em;
  color:var(--cream); margin:0 0 clamp(1.2rem,2.4vw,1.9rem); max-width:22ch; }
.enq__hint{ display:block; font-family:"Geist Mono",ui-monospace,monospace;
  font-size:var(--fs-micro); letter-spacing:.16em; text-transform:uppercase;
  color:var(--muted-2); margin-bottom:.9rem; }

.enq__opts{ display:flex; flex-wrap:wrap; gap:.6rem; }
.enq__opt{ position:relative; }
.enq__opt input{ position:absolute; opacity:0; width:0; height:0; }
.enq__opt span{ display:block; padding:.85rem 1.3rem; border:1px solid var(--line);
  color:var(--cream); font-size:var(--fs-body); cursor:pointer;
  transition:border-color .35s var(--ease), background .35s var(--ease), color .35s var(--ease); }
.enq__opt span:hover{ border-color:var(--gold); }
.enq__opt input:checked + span{ background:var(--cream); border-color:var(--cream); color:var(--navy); }
.enq__opt input:focus-visible + span{ outline:1px solid var(--gold); outline-offset:3px; }

.enq__field{ width:100%; max-width:30rem; background:none; border:0;
  border-bottom:1px solid var(--line); color:var(--cream);
  font-family:inherit; font-size:clamp(1.05rem,1.8vw,1.4rem); padding:.6rem 0;
  transition:border-color .35s var(--ease); }
.enq__field::placeholder{ color:var(--muted-2); }
.enq__field:focus{ outline:none; border-color:var(--gold); }

/* budget — the 'formbudget' idea, rebuilt */
.enq__money{ font-family:"Instrument Serif",Georgia,serif;
  font-size:clamp(2rem,4.4vw,3.4rem); line-height:1; color:var(--gold); }
.enq__range{ -webkit-appearance:none; appearance:none; width:100%; max-width:34rem;
  height:1px; background:var(--line); margin:clamp(1.4rem,2.6vw,2rem) 0 1rem; cursor:pointer; }
.enq__range::-webkit-slider-thumb{ -webkit-appearance:none; width:15px; height:15px;
  background:var(--gold); cursor:grab; border:0; }
.enq__range::-moz-range-thumb{ width:15px; height:15px; background:var(--gold);
  border:0; cursor:grab; }
.enq__range:focus-visible{ outline:1px solid var(--gold); outline-offset:8px; }
.enq__band{ max-width:44ch; color:var(--muted); font-size:var(--fs-body); line-height:1.6; margin:0 0 1rem; }
.enq__buys{ list-style:none; margin:0; padding:0; display:grid; gap:.5rem; max-width:44ch; }
.enq__buys li{ display:flex; gap:.7rem; font-size:var(--fs-body); color:var(--cream); }
.enq__buys li::before{ content:""; width:12px; height:1px; background:var(--gold);
  flex:none; margin-top:.72em; }

.enq__nav{ display:flex; align-items:center; gap:1rem; margin-top:clamp(1.8rem,3.4vw,2.6rem); }
.enq__back{ background:none; border:0; color:var(--muted-2); cursor:pointer;
  font-family:"Geist Mono",ui-monospace,monospace; font-size:var(--fs-micro);
  letter-spacing:.16em; text-transform:uppercase; transition:color .3s; }
.enq__back:hover{ color:var(--cream); }
.enq__back[hidden]{ display:none; }
.enq__done{ max-width:46ch; }
.enq__done p{ color:var(--muted); margin:.9rem 0 0; line-height:1.6; }
@media(max-width:700px){ .enq__opts{ flex-direction:column } .enq__opt span{ text-align:left } }
@media (prefers-reduced-motion:reduce){ .enq__screen.is-on{ animation:none } }
"""

MARKUP = """
      <div class="enq reveal" id="enquiry">
        <div class="enq__rail" aria-hidden="true"><i class="is-done"></i><i></i><i></i><i></i></div>
        <form id="enqForm" novalidate>

          <section class="enq__screen is-on" data-step="0">
            <span class="enq__hint">The machine</span>
            <h3 class="enq__q">What are we filming?</h3>
            <div class="enq__opts">
              <label class="enq__opt"><input type="radio" name="subject" value="Yacht or boat" required><span>A yacht or boat</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Classic car"><span>A classic car</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Supercar"><span>A supercar</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Something else"><span>Something else</span></label>
            </div>
          </section>

          <section class="enq__screen" data-step="1">
            <span class="enq__hint">The moment</span>
            <h3 class="enq__q">When does it happen?</h3>
            <div class="enq__opts">
              <label class="enq__opt"><input type="radio" name="timing" value="Within a month"><span>Within a month</span></label>
              <label class="enq__opt"><input type="radio" name="timing" value="One to three months"><span>One to three months</span></label>
              <label class="enq__opt"><input type="radio" name="timing" value="Later this year"><span>Later this year</span></label>
              <label class="enq__opt"><input type="radio" name="timing" value="Still deciding"><span>Still deciding</span></label>
            </div>
          </section>

          <section class="enq__screen" data-step="2">
            <span class="enq__hint">The budget</span>
            <h3 class="enq__q">Roughly what are you working with?</h3>
            <div class="enq__money" id="enqMoney">£10,000</div>
            <input class="enq__range" type="range" name="budget" min="5000" max="50000" step="2500" value="10000"
                   aria-label="Approximate budget" />
            <p class="enq__band" id="enqBand"></p>
            <ul class="enq__buys" id="enqBuys"></ul>
          </section>

          <section class="enq__screen" data-step="3">
            <span class="enq__hint">The reply</span>
            <h3 class="enq__q">Where do I send it?</h3>
            <input class="enq__field" type="email" name="email" placeholder="you@company.com"
                   autocomplete="email" required />
          </section>

          <section class="enq__screen enq__done" data-step="4">
            <h3 class="enq__q">Thank you.</h3>
            <p id="enqSummary"></p>
            <p>This opens your email so you can send it — and read it back before you do.
            The reply comes from me, not an autoresponder.</p>
          </section>

          <div class="enq__nav">
            <button class="cbtn cbtn--main" type="button" id="enqNext">
              Continue <svg viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4"/></svg>
            </button>
            <button class="enq__back" type="button" id="enqBack" hidden>Back</button>
          </div>
        </form>
      </div>
"""

JS = """
  /* ── Enquiry: 'quizfocus' shape + 'formbudget' bands ─────────── */
  (function () {
    const form = document.getElementById("enqForm");
    if (!form) return;
    const screens = [].slice.call(form.querySelectorAll(".enq__screen"));
    const rail = document.querySelectorAll(".enq__rail i");
    const next = document.getElementById("enqNext");
    const back = document.getElementById("enqBack");
    const nav  = form.querySelector(".enq__nav");
    const rng  = form.elements.budget;
    let at = 0;

    // what each band actually buys — Morgan's ladder, brief §14
    const BANDS = [
      [10000, "A single film, shot in a day, cut for the site and for social.",
        ["One shoot day", "A two to three minute film", "Three social cutdowns"]],
      [20000, "Where most heritage and launch films land.",
        ["Two shoot days", "Story built around the people, not just the machine", "Stills shot alongside"]],
      [35000, "A fuller production: travel, a crew, and more than one chapter.",
        ["Multiple days and locations", "A small crew, not a one-man band", "A film plus a set of cutdowns"]],
      [1e9, "A season, or a series.",
        ["Several shoots across the year", "A presenter-led episodic format", "A library you keep drawing on"]],
    ];

    function gbp(v) { return "£" + (+v).toLocaleString("en-GB") + (+v >= 50000 ? "+" : ""); }

    function syncBudget() {
      const v = +rng.value;
      const b = BANDS.filter(function (x) { return v < x[0]; })[0] || BANDS[BANDS.length - 1];
      document.getElementById("enqMoney").textContent = gbp(v);
      document.getElementById("enqBand").textContent = b[1];
      document.getElementById("enqBuys").innerHTML =
        b[2].map(function (t) { return "<li>" + t + "</li>"; }).join("");
    }
    rng.addEventListener("input", syncBudget);
    syncBudget();

    function valid(i) {
      if (i === 0) return !!form.querySelector('[name="subject"]:checked');
      if (i === 1) return !!form.querySelector('[name="timing"]:checked');
      if (i === 3) return /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(form.elements.email.value.trim());
      return true;
    }

    function show(i) {
      at = i;
      screens.forEach(function (s, n) { s.classList.toggle("is-on", n === i); });
      rail.forEach(function (el, n) { el.classList.toggle("is-done", n <= i); });
      back.hidden = i === 0 || i === screens.length - 1;
      nav.hidden = i === screens.length - 1;
      next.firstChild.textContent = i === 3 ? "Send it " : "Continue ";
      const f = screens[i].querySelector("input:not([type=radio]), input[type=radio]");
      if (f && i !== 2) { try { f.focus({ preventScroll: true }); } catch (e) {} }
    }

    function finish() {
      const d = new FormData(form);
      const line = [d.get("subject"), d.get("timing"), gbp(d.get("budget"))]
        .filter(Boolean).join(" · ");
      document.getElementById("enqSummary").textContent = line;
      // PLACEHOLDER: swap for a real endpoint once the domain exists
      const body = encodeURIComponent(
        "Filming: " + d.get("subject") + "\\nTiming: " + d.get("timing") +
        "\\nBudget: " + gbp(d.get("budget")) + "\\nReply to: " + d.get("email"));
      window.location.href =
        "mailto:hello@higherheights.studio?subject=" +
        encodeURIComponent("Enquiry — " + d.get("subject")) + "&body=" + body;
      show(4);
    }

    next.addEventListener("click", function () {
      if (!valid(at)) {
        const bad = screens[at].querySelector(".enq__opts, .enq__field");
        if (bad) { bad.animate(
          [{ transform: "translateX(0)" }, { transform: "translateX(-5px)" },
           { transform: "translateX(5px)" }, { transform: "translateX(0)" }],
          { duration: 260 }); }
        return;
      }
      if (at === 3) { finish(); return; }
      show(at + 1);
    });
    back.addEventListener("click", function () { if (at > 0) show(at - 1); });

    // choosing an option carries you on, and Enter works everywhere
    form.addEventListener("change", function (e) {
      if (e.target.type === "radio" && at < 2) setTimeout(function () { next.click(); }, 240);
    });
    form.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); next.click(); }
    });
  })();
"""

sub("/* ══ Enquiry", "/* ══ Enquiry")  if False else None

# CSS goes after the contact styles
sub(".contact__open{ font-family:\"Geist Mono\",ui-monospace,monospace; font-size:var(--fs-micro);\n  letter-spacing:.14em; text-transform:uppercase; color:var(--muted-2); }",
    ".contact__open{ font-family:\"Geist Mono\",ui-monospace,monospace; font-size:var(--fs-micro);\n"
    "  letter-spacing:.14em; text-transform:uppercase; color:var(--muted-2); }\n" + CSS,
    "enquiry CSS")

# markup goes after the contact grid, before the footer
sub("      <footer class=\"footer\">", MARKUP + "\n      <footer class=\"footer\">",
    "enquiry markup")

# JS before the carousel block
sub("  /* ── live London clock in the hero strip ─────────────── */",
    JS + "\n  /* ── live London clock in the hero strip ─────────────── */",
    "enquiry JS")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
