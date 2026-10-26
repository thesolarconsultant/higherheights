#!/usr/bin/env python3
"""Pull logo candidates straight from each client's own site."""
import os, re, sys, json
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sourced")
os.makedirs(OUT, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

SITES = {
    "nobl": "https://noblclo.com/",
    "oakridge-uk": "https://oakridgepropertygroup.co.uk/",
    "melissahemsley": "https://www.melissahemsley.com/",
    "matchroom": "https://www.matchroomboxing.com/",
    "watchtrader": "https://www.watchtrader.co.uk/",
}


def get(url, timeout=25):
    r = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(r, timeout=timeout) as f:
        return f.read(), f.headers.get("Content-Type", "")


def candidates(html, base):
    """Anything that smells like a logo, best guesses first."""
    out = []
    # explicit logo-ish assets
    for m in re.finditer(r'(?:src|href|content)=["\']([^"\']+\.(?:svg|png|webp|jpg))["\']', html, re.I):
        u = m.group(1)
        score = 0
        low = u.lower()
        if "logo" in low: score += 10
        if low.endswith(".svg"): score += 6
        if "brand" in low or "mark" in low: score += 3
        if "wordmark" in low: score += 4
        if any(b in low for b in ("sprite", "placeholder", "banner", "hero", "product", "payment", "flag")):
            score -= 8
        if score > 0:
            out.append((score, urljoin(base, u)))
    # og:image as a last resort
    og = re.search(r'property=["\']og:image["\']\s+content=["\']([^"\']+)', html, re.I)
    if og:
        out.append((1, urljoin(base, og.group(1))))
    seen, uniq = set(), []
    for sc, u in sorted(out, key=lambda x: -x[0]):
        if u not in seen:
            seen.add(u); uniq.append((sc, u))
    return uniq[:6]


report = {}
for slug, site in SITES.items():
    entry = {"site": site, "saved": [], "error": None}
    try:
        body, _ = get(site)
        html = body.decode("utf-8", "ignore")
        cands = candidates(html, site)
        entry["found"] = len(cands)
        for i, (score, u) in enumerate(cands[:3]):
            try:
                data, ctype = get(u)
                if len(data) < 350:
                    continue
                ext = ".svg" if "svg" in ctype or u.lower().endswith(".svg") else \
                      ".png" if "png" in ctype or u.lower().endswith(".png") else \
                      ".webp" if "webp" in ctype else ".jpg"
                name = f"{slug}-{i}{ext}"
                with open(os.path.join(OUT, name), "wb") as fh:
                    fh.write(data)
                entry["saved"].append({"file": name, "bytes": len(data),
                                       "score": score, "url": u[:95]})
            except Exception as e:
                entry.setdefault("fetch_errors", []).append(f"{u[:70]}: {e.__class__.__name__}")
    except Exception as e:
        entry["error"] = f"{e.__class__.__name__}: {e}"
    report[slug] = entry
    print(f"\n{slug:16s} {entry.get('error') or str(entry.get('found','?')) + ' candidates'}")
    for s in entry["saved"]:
        print(f"   {s['file']:22s} {s['bytes']:>8,}b  score {s['score']:2d}  {s['url']}")

json.dump(report, open(os.path.join(OUT, "sources.json"), "w"), indent=2)
