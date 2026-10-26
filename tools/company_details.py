# -*- coding: utf-8 -*-
"""Company details: legal compliance + local SEO.

A UK limited company must display its registered name, company number and
registered office on its website (Companies Act 2006 s.82 / the E-Commerce
Regulations 2002). None of the three were on the site.

The same details are a strong local-SEO signal, so they also go into
schema.org as a real Organization with a postal address rather than the
vague LocalBusiness stub that was there.

Verified against Companies House, 17461146:
  HIGHER HEIGHTS (LONDON) LIMITED
  Active, private limited company, incorporated 15 September 2026
  16 The Drive, Loughton, England, IG10 1HB
"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")
BASE = "https://higher-heights.vercel.app"

LEGAL_NAME = "Higher Heights (London) Limited"
CO_NO      = "17461146"
ADDR1      = "16 The Drive"
TOWN       = "Loughton"
POSTCODE   = "IG10 1HB"
INCORP     = "2026-09-15"

LEGAL_HTML = (
  f'<span class="foot__legal">{LEGAL_NAME} · Registered in England &amp; Wales '
  f'no.&nbsp;{CO_NO} · {ADDR1}, {TOWN}, {POSTCODE}</span>'
)

ORG = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Higher Heights Films",
  "legalName": LEGAL_NAME,
  "identifier": {"@type": "PropertyValue",
                 "name": "Company number", "value": CO_NO},
  "foundingDate": INCORP,
  "url": BASE + "/",
  "image": BASE + "/assets/img/icon-512.png",
  "logo": BASE + "/assets/img/hh-mono.svg",
  "description": ("UK video production company. Corporate video, brand films, "
                  "product, events and aerial — directed, shot and edited by "
                  "one person."),
  "address": {"@type": "PostalAddress",
              "streetAddress": ADDR1, "addressLocality": TOWN,
              "postalCode": POSTCODE, "addressRegion": "Essex",
              "addressCountry": "GB"},
  "areaServed": [{"@type": "City", "name": "London"},
                 {"@type": "Country", "name": "United Kingdom"}],
  "knowsAbout": ["Corporate video production", "Event videography",
                 "Aerial and drone filming", "Brand films",
                 "Product photography"],
}

# ── 1. footer legal line on every page ──
added = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    if "foot__legal" in s:
        continue
    m = re.search(r'<div class="foot__base">(.*?)</div>', s, re.S)
    if not m:
        print(f"   no foot__base in {os.path.basename(f)}")
        continue
    inner = m.group(1)
    s = s[:m.start(1)] + inner.rstrip() + "\n          " + LEGAL_HTML + "\n        " + s[m.end(1):]
    open(f, "w", encoding="utf-8").write(s)
    added += 1
    print(f"   legal line  {os.path.basename(f)}")

# ── 2. styling for it ──
CSS = """
.foot__legal{ display:block; margin-top:.75rem; max-width:var(--measure-wide);
  font-size:var(--fs-micro); line-height:1.7; color:var(--muted);
  letter-spacing:.12em; text-transform:none; }
"""
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    if ".foot__legal{" in s:
        continue
    s = s.replace("</style>", CSS + "</style>", 1)
    open(f, "w", encoding="utf-8").write(s)

# ── 3. the organisation schema on the homepage ──
idx = os.path.join(SITE, "index.html")
s = open(idx, encoding="utf-8").read()
if '"legalName"' not in s:
    blob = ('<script type="application/ld+json">\n'
            + json.dumps(ORG, indent=1, ensure_ascii=False) + "\n</script>\n")
    s = s.replace("</head>", blob + "</head>", 1)
    open(idx, "w", encoding="utf-8").write(s)
    print("\n   organisation schema -> index.html")

print(f"\n{added} pages given the legal line")
