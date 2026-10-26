# -*- coding: utf-8 -*-
"""Service pages, chosen on UK search volume and backed by real work.

No invented credits, clients, results or testimonials -- every name used
here appears in the existing site or the Drive manifest.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import page, service_ld

CTA = """
  <section class="contact" id="enquire" aria-labelledby="cta-head">
    <div class="wrap">
      <div class="contact__inner">
        <div>
          <div class="eyebrow eyebrow--n reveal">
            <span class="eyebrow__line"></span><span class="mono">Start here</span>
          </div>
          <h2 class="contact__h" id="cta-head" data-gw="letters">{H}</h2>
          <p class="contact__lede">{L}</p>
          <div class="contact__actions">
            <a class="cbtn cbtn--main" href="/#enquire">Tell me what you need</a>
            <a class="cbtn" href="/#work">See the work</a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

def intro(eyebrow, h1, lede):
    return f"""
  <section class="svc" aria-labelledby="pg-head">
    <div class="wrap">
      <div class="eyebrow eyebrow--n reveal">
        <span class="eyebrow__line"></span><span class="mono">{eyebrow}</span>
      </div>
      <h1 class="svc__h" id="pg-head" data-gw="letters">{h1}</h1>
      <p class="hero__sub">{lede}</p>
    </div>
  </section>
"""

def listing(head, items):
    li = "\n".join(f'        <li class="reveal"><span class="svc__name">{i}</span></li>' for i in items)
    return f"""
  <section class="svc" aria-labelledby="l-{abs(hash(head))%9999}">
    <div class="wrap">
      <h2 class="svc__h" id="l-{abs(hash(head))%9999}" data-gw="letters">{head}</h2>
      <ol class="svc__grid">
{li}
      </ol>
    </div>
  </section>
"""

def prose(head, paras):
    # Cream ground: use the site's own statement classes. The dark-ground
    # .band__lede is coloured var(--muted) = rgba(233,229,219,.56) -- cream at
    # 56% -- which is invisible on cream.
    p = "\n".join(f'          <p>{x}</p>' for x in paras)
    return f"""
  <section class="band-cream" aria-labelledby="p-{abs(hash(head))%9999}">
    <div class="wrap statement">
      <div class="statement__grid">
        <p class="statement__lead" id="p-{abs(hash(head))%9999}">{head}</p>
        <div class="statement__body reveal">
{p}
        </div>
      </div>
    </div>
  </section>
"""

# ───────────────────────── CORPORATE ─────────────────────────
slug = "corporate-video-production.html"
body = (
  intro("Corporate video production",
        "Corporate video that people actually watch",
        "Films for companies that need to explain something, sell something or "
        "hire someone — made the way a brand film is made, not the way a corporate "
        "video usually is. UK based, filming across the country and abroad.")
  + listing("What companies commission most", [
      "Recruitment &amp; culture films",
      "Company and brand stories",
      "Product and service explainers",
      "Case studies &amp; testimonials",
      "Conference &amp; event coverage",
      "Social cutdowns from one shoot",
    ])
  + prose("How it tends to go", [
      "Most corporate video fails for the same reason: it is written to say "
      "everything, so it says nothing. The fix is not a bigger crew or a longer "
      "film — it is deciding, before anyone picks up a camera, what one thing the "
      "film is for and who it is talking to.",
      "A typical job is one or two shoot days, a small crew, and a cut that "
      "respects how long anyone will actually watch. You get the main film plus "
      "the cutdowns the campaign needs, from the same shoot, rather than paying "
      "twice.",
      "Recent work includes a recruitment film for Nexus, property films for "
      "Oakridge Property Group, brand work for Aduna and WHOOP, and ongoing "
      "product film for WatchTrader &amp; Co.",
    ])
  + listing("What you get", [
      "A director who shoots and edits",
      "One or two days, not a fortnight",
      "Main film plus social cutdowns",
      "Stills from the same shoot",
      "Aerial built in where it earns its place",
      "Usage that covers paid media",
    ])
  + CTA.format(H="Tell me what the film is for",
               L="A sentence about the problem is enough to start. "
                 "You will get a reply from Morgan, not a form response.")
)
n = page(slug,
  "Corporate Video Production UK | Corporate Videographer — Higher Heights Films",
  "UK corporate video production and corporate videographer services. Recruitment "
  "films, brand stories, product explainers, event coverage and social cutdowns. "
  "Based in the UK, filming worldwide.",
  body,
  service_ld("Corporate Video Production",
             "Corporate video production and corporate videographer services across the UK.",
             slug))
print(f"  {slug:44s} {n:,} bytes")

# ───────────────────────── EVENTS ─────────────────────────
slug = "event-videography.html"
body = (
  intro("Event videography",
        "Event films that are worth keeping",
        "Conference, launch, ceremony and sport coverage — cut while it still "
        "matters, not six weeks later. UK based, filming worldwide.")
  + listing("What gets filmed", [
      "Conferences &amp; summits",
      "Product launches",
      "Awards &amp; ceremonies",
      "Sport &amp; ringside",
      "Brand activations",
      "Same-week social edits",
    ])
  + prose("Why most event video disappoints", [
      "An event happens once, which means there is no second take and no reshoot. "
      "What separates usable coverage from a hard drive nobody opens is deciding "
      "in advance which five moments actually matter, and being in the right place "
      "for each of them.",
      "Coverage usually means one or two operators, a plan agreed before the day, "
      "and a fast turnaround on the social cut so it lands while people still care "
      "— with the longer film following after.",
      "Event and coverage work includes ringside filming for Matchroom Boxing.",
    ])
  + CTA.format(H="Tell me about the event",
               L="Date, venue and what it needs to achieve. That is enough to "
                 "come back to you with a plan and a number.")
)
n = page(slug,
  "Event Videography UK | Event Videographer — Higher Heights Films",
  "UK event videographer and event video production. Conferences, launches, "
  "awards, sport and brand activations, with fast social edits and a longer "
  "film to follow.",
  body,
  service_ld("Event Videography",
             "Event videography and event video production across the UK.", slug))
print(f"  {slug:44s} {n:,} bytes")
