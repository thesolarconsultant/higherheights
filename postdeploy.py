# -*- coding: utf-8 -*-
"""Post-deploy: absolute canonical/OG URLs, robots.txt, sitemap.xml."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site-v5")
BASE = "https://higher-heights.vercel.app"

p = os.path.join(SITE, "index.html")
html = open(p, encoding="utf-8").read()
done = []


def sub(old, new, label):
    global html
    assert html.count(old) == 1, f"{label}: {html.count(old)}"
    html = html.replace(old, new)
    done.append(label)


sub('<meta property="og:type" content="website" />',
    f'<meta property="og:type" content="website" />\n'
    f'<link rel="canonical" href="{BASE}/" />\n'
    f'<meta property="og:url" content="{BASE}/" />',
    "canonical + og:url")

sub('<meta property="og:image" content="assets/img/og-image.png" />',
    f'<meta property="og:image" content="{BASE}/assets/img/og-image.png" />\n'
    f'<meta property="og:image:alt" content="Higher Heights Films — film, aerial and photography" />',
    "og:image absolute")

sub('<meta name="twitter:card" content="summary_large_image" />',
    f'<meta name="twitter:card" content="summary_large_image" />\n'
    f'<meta name="twitter:image" content="{BASE}/assets/img/og-image.png" />',
    "twitter image")

open(p, "w", encoding="utf-8").write(html)

robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(robots)

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{BASE}/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(sitemap)

print("patched", p)
for d in done:
    print("  ✓", d)
print("  ✓ robots.txt, sitemap.xml")
