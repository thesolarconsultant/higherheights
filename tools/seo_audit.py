#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local + technical SEO audit of higherheights.uk.

Follows the seo-local and seo-audit dimensions from the claude-seo skill set,
run directly against the live site rather than through the plugin scripts
(which expect a Claude Code plugin root that does not exist here).

Checks only what can be verified from the live pages -- no invented findings.
"""
import json, re, ssl, socket, urllib.request, urllib.error
from collections import OrderedDict

BASE = "https://www.higherheights.uk"
PAGES = ["/", "/corporate-video-production", "/videographer-london",
         "/event-videography", "/aerial-drone-filming"]

UA = {"User-Agent": "Mozilla/5.0 (compatible; SEOAudit/1.0)"}


def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), ""
    except Exception as e:
        return None, {}, f"ERR {e}"


def tag(html, pat, flags=re.I | re.S):
    m = re.search(pat, html, flags)
    return m.group(1).strip() if m else None


report = OrderedDict()

# ── fetch everything once ──
docs = {}
for p in PAGES:
    code, hdr, body = get(BASE + p)
    docs[p] = (code, hdr, body)

# ── 1. ON-PAGE / LOCAL SIGNALS ──
onpage = []
for p, (code, hdr, body) in docs.items():
    title = tag(body, r"<title>(.*?)</title>") or ""
    desc  = tag(body, r'<meta name="description" content="(.*?)"') or ""
    h1s   = re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.I | re.S)
    h1s   = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
    canon = tag(body, r'<link rel="canonical" href="(.*?)"') or ""
    onpage.append({
        "page": p, "status": code,
        "title": title, "title_len": len(title),
        "desc_len": len(desc),
        "h1_count": len(h1s), "h1": h1s[0][:60] if h1s else None,
        "canonical": canon.replace(BASE, "").replace("https://higherheights.uk", "") or "/",
        "has_london": "london" in body.lower(),
        "nap_phone": bool(re.search(r"tel:\+?[\d\s()-]{7,}", body, re.I)),
        "has_email": "hello@higherheights.uk" in body,
        "words": len(re.sub(r"<[^>]+>", " ", body).split()),
    })
report["on_page"] = onpage

# ── 2. SCHEMA ──
schema = []
code, hdr, home = docs["/"]
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', home, re.S):
    try:
        d = json.loads(m.group(1))
    except Exception as e:
        schema.append({"error": f"invalid JSON: {e}"}); continue
    schema.append({
        "type": d.get("@type"),
        "name": d.get("name"),
        "legalName": d.get("legalName"),
        "has_address": "address" in d,
        "address": d.get("address"),
        "areaServed": [a.get("name") for a in d.get("areaServed", [])] if isinstance(d.get("areaServed"), list) else d.get("areaServed"),
        "has_aggregateRating": "aggregateRating" in d,
        "has_geo": "geo" in d,
        "has_openingHours": "openingHoursSpecification" in d,
        "has_telephone": "telephone" in d,
        "has_priceRange": "priceRange" in d,
        "has_image": "image" in d,
        "has_sameAs": "sameAs" in d,
    })
report["schema"] = schema

# ── 3. TECHNICAL ──
rcode, rhdr, robots = get(BASE + "/robots.txt")
scode, shdr, sitemap = get(BASE + "/sitemap.xml")
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
_, home_hdr, _ = docs["/"]

report["technical"] = {
    "robots_status": rcode,
    "robots_has_sitemap": "sitemap:" in robots.lower(),
    "sitemap_status": scode,
    "sitemap_urls": len(locs),
    "sitemap_matches_live": sorted(l.replace("https://higherheights.uk", "").replace(BASE, "") or "/" for l in locs),
    "hsts": "strict-transport-security" in {k.lower() for k in home_hdr},
    "x_content_type": "x-content-type-options" in {k.lower() for k in home_hdr},
    "x_frame": "x-frame-options" in {k.lower() for k in home_hdr},
    "csp": "content-security-policy" in {k.lower() for k in home_hdr},
    "server": home_hdr.get("server") or home_hdr.get("Server"),
}

# apex vs www
acode, ahdr, _ = get("https://higherheights.uk/")
report["technical"]["apex_status"] = acode
report["technical"]["apex_redirects_to"] = ahdr.get("location") or ahdr.get("Location")

# ── 4. AI / GEO readiness ──
lcode, _, llms = get(BASE + "/llms.txt")
report["ai_readiness"] = {
    "llms_txt": lcode,
    "robots_blocks_ai": any(b in robots for b in ["GPTBot", "ClaudeBot", "PerplexityBot", "CCBot"]),
    "og_image": bool(tag(home, r'<meta property="og:image" content="(.*?)"')),
    "og_title": bool(tag(home, r'<meta property="og:title" content="(.*?)"')),
    "twitter_card": bool(tag(home, r'<meta name="twitter:card" content="(.*?)"')),
}

# ── 5. IMAGES ──
imgs = re.findall(r"<img[^>]*>", home, re.I)
report["images"] = {
    "total": len(imgs),
    "missing_alt": sum(1 for i in imgs if not re.search(r'\balt=', i, re.I)),
    "empty_alt": sum(1 for i in imgs if re.search(r'alt=""', i)),
    "lazy": sum(1 for i in imgs if "loading=" in i.lower()),
}

print(json.dumps(report, indent=1, ensure_ascii=False))
