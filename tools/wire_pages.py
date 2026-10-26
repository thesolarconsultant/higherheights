# -*- coding: utf-8 -*-
"""Link the service pages in, and give Google a sitemap.

An unlinked page is an orphan: Google may never find it, and if it does it
treats it as unimportant. The footer is the right home for service links --
it appears on every page, so each service page gains inbound links from
every other page.

Also rewrites the homepage title and description. It currently leads on
"brand films" (390/mo UK) and omits "video production" (33,100) and
"corporate video" (6,600) entirely.
"""
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")
BASE = "https://higher-heights.vercel.app"

PAGES = [
    ("corporate-video-production.html", "Corporate video",       "weekly", "0.9"),
    ("videographer-london.html",        "Videographer, London",  "weekly", "0.9"),
    ("event-videography.html",          "Event videography",     "weekly", "0.8"),
    ("aerial-drone-filming.html",       "Aerial &amp; drone",    "weekly", "0.8"),
]

FOOT_COL = """          <div class="foot__col">
            <h4>Services</h4>
{links}
          </div>
"""

def wire(path, is_home):
    s = open(path, encoding="utf-8").read()
    before = len(s)
    pre = "" if is_home else ""          # all links are root-relative

    # ── footer: add a Services column once ──
    if 'id="foot-services"' not in s:
        links = "\n".join(
            f'            <a href="{pre}/{slug}">{label}</a>' for slug, label, _, _ in PAGES)
        col = FOOT_COL.format(links=links).replace(
            '<h4>Services</h4>', '<h4 id="foot-services">Services</h4>')
        # insert before the LAST foot__col so it sits between Work and Studio
        idx = s.rfind('<div class="foot__col">')
        if idx != -1:
            s = s[:idx] + col.strip() + "\n          " + s[idx:]

    # ── nav: a Services link that points at the corporate page ──
    s = s.replace('<a href="#services">Services</a>',
                  '<a href="/corporate-video-production.html">Services</a>', 1)
    s = s.replace('<a href="/#services">Services</a>',
                  '<a href="/corporate-video-production.html">Services</a>', 1)

    open(path, "w", encoding="utf-8").write(s)
    return before, len(s)

print("── wiring footer + nav ──")
for f in ["index.html"] + [p[0] for p in PAGES]:
    p = os.path.join(SITE, f)
    if not os.path.exists(p):
        print(f"   MISSING {f}"); continue
    a, b = wire(p, f == "index.html")
    print(f"   {f:36s} {a:,} -> {b:,}")

# ── homepage title/description: lead on what people search ──
p = os.path.join(SITE, "index.html")
s = open(p, encoding="utf-8").read()
NEW_T = ("Video Production UK | Corporate Video &amp; Videographer "
         "— Higher Heights Films")
NEW_D = ("UK video production company. Corporate video, brand films, product, "
         "events and aerial — directed, shot and edited by one person. Based in "
         "the UK, filming worldwide.")
s = re.sub(r"<title>.*?</title>", f"<title>{NEW_T}</title>", s, count=1, flags=re.S)
s = re.sub(r'<meta name="description" content="[^"]*"',
           f'<meta name="description" content="{NEW_D}"', s, count=1)
open(p, "w", encoding="utf-8").write(s)
print(f"\n── homepage meta ──\n   title: {NEW_T[:64]}")

# ── sitemap + robots ──
today = datetime.date.today().isoformat()
urls = [("", "daily", "1.0")] + [(s_, c, pr) for s_, _, c, pr in PAGES]
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for slug, chg, pri in urls:
    xml += ["  <url>", f"    <loc>{BASE}/{slug}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <changefreq>{chg}</changefreq>",
            f"    <priority>{pri}</priority>", "  </url>"]
xml.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))

open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(
    f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print(f"   sitemap.xml  {len(urls)} urls\n   robots.txt")
