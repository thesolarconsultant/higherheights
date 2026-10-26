# -*- coding: utf-8 -*-
"""Two jobs.

1. The hero video was 19.5 MB — 95% of the page weight. Now serves a 5.4 MB
   1080p on desktop and a 1.5 MB 720p on narrow screens, and skips the video
   entirely on a metered or slow connection so the poster carries it.

2. Positioning widens from luxury-only to all work. The superyacht/classic-car
   framing was narrowing the studio to three worlds; the copy now leads on the
   craft and covers the range, while keeping people at the centre — which is
   the actual differentiator, and survives either positioning.
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


# ── 1. responsive video ───────────────────────────────────────────────────
sub('        <source src="assets/vid/commercial.mp4" type="video/mp4" />',
    '        <!-- source chosen at runtime: 720p on narrow screens, skipped on\n'
    '             a metered or slow connection so the poster carries it -->\n'
    '        <source data-src-wide="assets/vid/commercial-1080.mp4"\n'
    '                data-src-narrow="assets/vid/commercial-720.mp4" type="video/mp4" />',
    "hero video -> responsive sources")

sub("  /* \u2500\u2500 live London clock", """  /* -- hero video: pick a weight that suits the device -- */
  (function () {
    const v = document.getElementById("heroVideo");
    if (!v) return;
    const src = v.querySelector("source[data-src-wide]");
    if (!src) return;
    const c = navigator.connection || {};
    const thrifty = c.saveData === true ||
                    /^(slow-2g|2g|3g)$/.test(c.effectiveType || "");
    if (thrifty) { v.removeAttribute("autoplay"); v.load(); return; }  // poster only
    src.src = window.matchMedia("(max-width: 860px)").matches
      ? src.dataset.srcNarrow : src.dataset.srcWide;
    v.load();
    v.play().catch(function () {});
  })();

  /* \u2500\u2500 live London clock""",
    "runtime source selection")

# ── 2. positioning: all work ──────────────────────────────────────────────
TITLE = "Higher Heights Films — Film, Aerial &amp; Photography"
DESC = ("Higher Heights Films is a UK film, aerial and photography studio. Commercial films, "
        "brand stories, automotive, product, events and stills — story-led, filmed worldwide.")

s = re.sub(r"(<title>)[^<]*(</title>)", lambda m: m.group(1) + TITLE + m.group(2), s)
n = 0
for pat in [r'(<meta name="description" content=")[^"]*(")',
            r'(<meta property="og:description" content=")[^"]*(")',
            r'(<meta name="twitter:description" content=")[^"]*(")',
            r'(<meta property="og:title" content=")[^"]*(")',
            r'(<meta name="twitter:title" content=")[^"]*(")']:
    rep = TITLE if "title" in pat else DESC
    s, k = re.subn(pat, lambda m: m.group(1) + rep + m.group(2), s)
    n += k
print(f"  ok  title + {n} meta tags widened")

sub("""            Superyachts, classic cars and the machines people give
            their lives to — filmed through the people who keep them alive.""",
"""            Commercial film, brand stories, aerial and stills — for cars, boats,
            products and the people behind them. UK based, filming worldwide.""",
    "hero subline widened")

sub("""            <p class="foot__tag">Story-led films about extraordinary machines on land and sea,
            and the people who keep them alive.</p>""",
"""            <p class="foot__tag">Film, aerial and photography for brands, machines
            and the people behind them. Story first, every time.</p>""",
    "footer tagline widened")

sub("""<p class="band__lede reveal">A launch, a delivery, a restoration coming off the bench.""",
    """<p class="band__lede reveal">A launch, a campaign, a build, an event.""",
    "contact lede widened")

# the enquiry's first question narrowed the studio to three worlds
sub("""              <label class="enq__opt"><input type="radio" name="subject" value="Yacht or boat" required><span>A yacht or boat</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Classic car"><span>A classic car</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Supercar"><span>A supercar</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Something else"><span>Something else</span></label>""",
"""              <label class="enq__opt"><input type="radio" name="subject" value="A brand or product" required><span>A brand or product</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="A car, boat or machine"><span>A car, boat or machine</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="A place or property"><span>A place or property</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="An event"><span>An event</span></label>
              <label class="enq__opt"><input type="radio" name="subject" value="Something else"><span>Something else</span></label>""",
    "enquiry subjects widened")

# and the budget bands shouldn't assume a heritage film
sub('[10000, "A single film, shot in a day, cut for the site and for social.",',
    '[10000, "A single film, shot in a day, cut for the site and for social.",', "bands kept")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
