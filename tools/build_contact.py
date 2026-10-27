# -*- coding: utf-8 -*-
"""The standalone /contact page.

The body is the homepage's own contact section, lifted by markup so it cannot
drift from it: same enquiry form, same script block, same watermark. Two
changes on the way through:

  * the heading becomes the page's <h1> (split-letter treatment and the
    <em> styling are kept; the CSS carries h1 twins of its h2 rules);
  * its anchors are made absolute (the footer lives inside this section).

/api/enquiry sends non-JS clients to /contact?sent=1; the enquiry script in
index.html turns that into the thank-you state.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagekit import page, section, absolutise_nav

KEEP = ("enquiry",)

slug = "contact.html"

body = section('<section class="contact" id="contact"')

# h2 -> h1
h2 = re.search(r'<h2 id="contact-head" data-gw="letters">(.*?)</h2>', body, re.S)
assert h2, "contact heading not found in index.html"
body = body.replace(h2.group(0),
                    f'<h1 id="contact-head" data-gw="letters">{h2.group(1)}</h1>')

# The homepage nests the footer inside this section's .wrap, which is what gives it
# its side padding, so it stays there. Its anchors get the same treatment page()
# gives the nav (#work -> /#work); "#enquiry" is on this page, so it stays.
body = absolutise_nav(body, KEEP)

# guards: the things this page is specified to have, and to not have
assert body.count("<h1") == 1 and "<h2" not in body.split("<h1")[0], "heading"
assert "<em>filming?</em>" in body and 'data-gw="letters"' in body
assert 'class="hh-wm hh-wm--contact"' in body, "watermark"
assert '<span class="mono">Contact</span>' in body, "eyebrow"
assert not re.search(r'<span class="mono">\s*0?\d\b', body), "numbered label"
assert body.count("<footer") == 1 and body.count("</footer>") == 1, "footer"
assert 'href="#contact"' not in body
assert body.count('id="enqForm"') == 1

n = page(slug,
  "Contact — Higher Heights Films",
  "Tell Higher Heights Films what you want filming and when it happens. "
  "The first reply comes from Morgan, usually within a day.",
  body,
  keep=KEEP, loader=True, footer=False)        # the form is on this page: "Start a project" stays in-page
print(f"  {slug:36s} {n:,}")
