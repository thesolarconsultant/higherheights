# -*- coding: utf-8 -*-
"""Build service pages that share the site's exact chrome.

Rather than hand-copy markup (which drifts), this lifts the real <head>,
nav and footer out of index.html and reuses them, so every page inherits
the same CSS, nav behaviour, inverting-nav script and footer.

Pages are chosen on UK search volume, not on what the studio likes calling
its work:

  corporate video production   3,600   + corporate videographer 6,600
                                       + corporate video uk     3,300
  event videographer           4,600
  videographer london          4,400
  aerial / drone filming       (genuine differentiator, lower volume)

For contrast, "brand video production" is 390 and "brand film" is
negligible -- which is what the site currently leads on.
"""
import os, re, json

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE  = os.path.join(ROOT, "site-brand")
src   = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
lines = src.split("\n")

def block(a, b):                       # 1-indexed, inclusive
    return "\n".join(lines[a-1:b])

def between(open_tag, close_tag, after=0):
    """Locate a block by its markup, not by line number.

    This used to slice fixed line ranges out of index.html. Every edit to the
    homepage shifted those offsets, and the nav silently started being cut
    mid-element -- producing pages with an unclosed <nav> that rendered at
    zero height. Markers survive edits; line numbers do not.
    """
    a = src.index(open_tag, after)
    b = src.index(close_tag, a) + len(close_tag)
    return src[a:b], b


_head_end = src.index("</head>")
HEAD_OPEN = src[:_head_end]                                   # doctype .. before </head>
_nav, _after_nav = between('<header class="nav"', "</header>")
_drawer, _ = between('<div class="nav__drawer"', "</div>", _after_nav)
NAV = _nav + "\n" + _drawer                                   # header + the drawer its JS wires
FOOTER, _after_foot = between('<footer class="foot"', "</footer>")
SCRIPTS = src[src.index("<script>", _after_foot):]            # all script blocks + </body></html>

# strip the page-specific meta out of the shared head; each page sets its own
def absolutise_nav(markup):
    """Sub-pages: in-page anchors must point back at the homepage."""
    import re as _re
    return _re.sub(r'href="#([a-z]+)"', r'href="/#"', markup)


def head_for(title, desc, slug, extra_ld=None):
    h = HEAD_OPEN
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*"',
               f'<meta name="description" content="{desc}"', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*"',
               f'<meta property="og:title" content="{title}"', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*"',
               f'<meta property="og:description" content="{desc}"', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*"',
               f'<link rel="canonical" href="https://higher-heights.vercel.app/{slug}"', h, count=1)
    if extra_ld:
        h += "\n<script type=\"application/ld+json\">\n" + json.dumps(extra_ld, indent=1) + "\n</script>"
    return h

def service_ld(name, desc, slug):
    return {
      "@context": "https://schema.org", "@type": "Service",
      "serviceType": name, "description": desc,
      "provider": {"@type": "LocalBusiness", "name": "Higher Heights Films",
                   "areaServed": "United Kingdom",
                   "url": "https://higher-heights.vercel.app/"},
      "areaServed": {"@type": "Country", "name": "United Kingdom"},
      "url": f"https://higher-heights.vercel.app/{slug}",
    }

def page(slug, title, desc, body, ld=None):
    html = (head_for(title, desc, slug, ld) + "\n</head>\n<body>\n"
            + absolutise_nav(NAV) + "\n<main id=\"top\">\n" + body + "\n" + FOOTER
            + "\n</main>\n" + trim_scripts(SCRIPTS)[0])
    out = os.path.join(SITE, slug)
    open(out, "w", encoding="utf-8").write(html)
    return len(html)



# Homepage-only script sections. A service page has none of their markup, so
# the first one to throw would kill every section after it -- including the
# inverting nav and reveal-on-scroll. Cut rather than guarded: subtraction
# cannot break index.html, and these pages genuinely do not need them.
HOMEPAGE_ONLY = [
    # "film data" stays: it defines the $ helper the nav code uses
    "hover-to-play film tiles", "screening modal",
    "aerial parallax", "live London clock", "scroll carousel",
    "hero video: pause when off-screen",
]


def trim_scripts(js):
    import re as _re
    marks = [(m.start(), m.group(0)) for m in _re.finditer(r"  /\* ── .*?\*/", js)]
    if not marks:
        marks = [(m.start(), m.group(0)) for m in _re.finditer(r"  /\* [─-]{2,} .*?\*/", js)]
    cuts = []
    for i, (pos, text) in enumerate(marks):
        if any(k.lower() in text.lower() for k in HOMEPAGE_ONLY):
            end = marks[i + 1][0] if i + 1 < len(marks) else None
            if end:
                cuts.append((pos, end))
    for a, b in reversed(cuts):
        js = js[:a] + js[b:]
    return js, len(cuts)

__all__ = ["page", "service_ld", "SITE"]

if __name__ == "__main__":
    print(f"head   {len(HEAD_OPEN):,}")
    print(f"nav    {len(NAV):,}")
    print(f"footer {len(FOOTER):,}")
    print(f"script {len(SCRIPTS):,}")
    print("\nsanity:")
    print("  nav has brand wordmark:", "wordmark-cream.svg" in NAV)
    print("  footer closes:", NAV.strip().endswith("</header>"), FOOTER.strip().endswith("</footer>"))
    print("  scripts close body:", SCRIPTS.strip().endswith("</body>") or "</html>" in SCRIPTS)
