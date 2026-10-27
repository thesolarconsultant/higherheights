# -*- coding: utf-8 -*-
"""Repair the service pages' nav and footer links; point Contact at /contact.

The four service pages were not produced by the builders alone: they carry
the loader, the .hh-wm--pg watermarks and later tuning laid on top by
page_watermarks.py / loading_screen.py / loader_wordmark.py. Re-running
build_pages_a/b would drop those, so this edits only the links in the nav
(header, mega menu, drawer) and the footer, and nothing else.

What was wrong: pagekit's old absolutise_nav() wrote a literal 0x01 byte
instead of the \1 group reference, so every nav link read href="/#<SOH>" --
name lost, all of them landing at the top of the homepage -- and the footer
was never rewritten at all, leaving bare "#work" etc. with no target on
these pages.

What this does:
  * Contact (header, mega, drawer)  -> /contact
  * the other nav links             -> /#<name>, matched on the link's own text
                                       (the names were lost; the pages' nav has
                                       also been hand-tuned, e.g. Services, so
                                       position cannot be relied on)
  * footer "#work" "#enquiry" etc.  -> /#<name>

Idempotent: a page with nothing left to fix is reported and left alone.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import SITE

PAGES = ["corporate-video-production.html", "videographer-london.html",
         "event-videography.html", "aerial-drone-filming.html"]
SOH = '<a href="/#\x01"'
BAD = 'href="/#\x01"'
# visible text of a broken nav link -> the homepage anchor it was meant for
BY_TEXT = {"Work": "work", "Studio": "studio", "": "top",       # "" is the logo link
           "The studio": "about", "What we make": "services", "Selected work": "work",
           "Aerial": "aerial", "Product & stills": "product", "Meet Morgan": "studio"}
LINK = re.compile(r'(<a\b[^>]*?)href="/#\x01"([^>]*>)(.*?)</a>', re.S)
SWAPS = [
    ('<a href="/#\x01">Contact</a>',                '<a href="/contact">Contact</a>',               2),
    ('<a class="mega__a" href="/#\x01" data-i="6"', '<a class="mega__a" href="/contact" data-i="6"', 1),
]

for f in PAGES:
    p = os.path.join(SITE, f)
    s = open(p, encoding="utf-8", newline="").read()
    a = s.index('<header class="nav"')
    b = s.index("</div>", s.index('<div class="nav__drawer"', a)) + len("</div>")
    nav, rest = s[a:b], s[b:]
    did = []

    for old, new, n in SWAPS:
        if nav.count(old):
            assert nav.count(old) == n, (f, old, nav.count(old))
            nav = nav.replace(old, new); did.append("contact")

    def restore(m):
        text = re.sub(r"<[^>]+>", "", m.group(3)).replace("&amp;", "&").strip()
        text = re.sub(r"\s+", " ", text)
        text = text.split(" First reply")[0].split("First reply")[0]
        for key in sorted(BY_TEXT, key=len, reverse=True):      # mega items carry a caption after the title
            if key and text.startswith(key):
                return f'{m.group(1)}href="/#{BY_TEXT[key]}"{m.group(2)}{m.group(3)}</a>'
        if not text:
            return f'{m.group(1)}href="/#top"{m.group(2)}{m.group(3)}</a>'
        raise AssertionError((f, "no anchor known for nav link text", text))
    nav2 = LINK.sub(restore, nav)
    if nav2 != nav:
        did.append(f"{nav.count(BAD)} nav anchors"); nav = nav2

    fa = rest.index('<footer class="foot"'); fb = rest.index("</footer>", fa)
    foot = rest[fa:fb]
    foot2 = re.sub(r'href="#([a-z]+)"', r'href="/#\1"', foot)
    if foot2 != foot:
        did.append("footer anchors"); rest = rest[:fa] + foot2 + rest[fb:]

    s = s[:a] + nav + rest
    assert "\x01" not in s, f
    if did:
        open(p, "w", encoding="utf-8", newline="").write(s)
    print(f"  {f:34s} {', '.join(did) or 'already done'}")
