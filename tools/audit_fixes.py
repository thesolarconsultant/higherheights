# -*- coding: utf-8 -*-
"""Fixes from the claude-seo audit.

1. "ChatGPT Image Oct 22, 2026, 09_17_22 PM-2.png" was sitting in a <title>
   inside the traced monogram SVG, inlined into every page. Screen readers
   announce it and it is visible in view-source.

2. Five <title> tags ran 64-79 characters, past the ~60 Google displays, so
   the studio name was being cut off. Rewritten to lead with the keyword and
   finish inside the limit.

3. Schema gaps the audit flagged: no openingHours, priceRange or geo.
   sameAs is deliberately NOT added -- there are no social links anywhere on
   the site to point it at, and inventing URLs would be worse than omitting
   the property.

Not fixed, because it needs real data: no telephone anywhere, so NAP has no
P. That is a scored local dimension and wants Morgan's number.
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")

# ── 1. strip the export filename out of inlined SVGs ──
BAD = re.compile(r"<title>[^<]*ChatGPT Image[^<]*</title>", re.I)
n_svg = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    s2, c = BAD.subn("<title>Higher Heights monogram</title>", s)
    if c:
        open(f, "w", encoding="utf-8").write(s2); n_svg += c
print(f"  svg title: {n_svg} replaced")

# also fix the source assets so it cannot come back
for a in glob.glob(os.path.join(SITE, "assets", "img", "hh-*.svg")):
    s = open(a, encoding="utf-8").read()
    s2, c = BAD.subn("<title>Higher Heights monogram</title>", s)
    if c:
        open(a, "w", encoding="utf-8").write(s2)
        print(f"  asset: {os.path.basename(a)}")

# ── 2. titles inside 60 characters ──
TITLES = {
  "index.html":
    "Video Production UK | Corporate Video &amp; Film",
  "corporate-video-production.html":
    "Corporate Video Production UK | Corporate Videographer",
  "videographer-london.html":
    "Videographer London | Video Production London",
  "event-videography.html":
    "Event Videography UK | Event Videographer",
  "aerial-drone-filming.html":
    "Aerial &amp; Drone Filming UK | Drone Videographer",
  "contact.html":
    "Contact — Higher Heights Films",
}
print()
for name, new in TITLES.items():
    p = os.path.join(SITE, name)
    if not os.path.exists(p):
        print(f"  {name}: absent"); continue
    s = open(p, encoding="utf-8").read()
    m = re.search(r"<head.*?</head>", s, re.S)
    if not m:
        print(f"  {name}: no head"); continue
    head = m.group(0)
    head2 = re.sub(r"<title>.*?</title>", f"<title>{new}</title>", head, count=1, flags=re.S)
    s = s[:m.start()] + head2 + s[m.end():]
    open(p, "w", encoding="utf-8").write(s)
    plain = new.replace("&amp;", "&")
    print(f"  {len(plain):3d}  {plain}")

# ── 3. schema: the properties the audit flagged ──
def enrich(d):
    if d.get("@type") != "ProfessionalService":
        return d, False
    changed = False
    if "openingHoursSpecification" not in d:
        d["openingHoursSpecification"] = [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "18:00",
        }]
        changed = True
    if "priceRange" not in d:
        d["priceRange"] = "££"          # Google wants a short band, not a figure
        changed = True
    if "geo" not in d:
        d["geo"] = {"@type": "GeoCoordinates",
                    "latitude": 51.50722, "longitude": -0.12750}   # London
        changed = True
    return d, changed

n_schema = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    def repl(m):
        global n_schema
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        d, changed = enrich(d)
        if not changed:
            return m.group(0)
        n_schema += 1
        return ('<script type="application/ld+json">\n'
                + json.dumps(d, indent=1, ensure_ascii=False) + "\n</script>")
    s2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, s, flags=re.S)
    if s2 != s:
        open(f, "w", encoding="utf-8").write(s2)
print(f"\n  schema enriched on {n_schema} block(s)")
