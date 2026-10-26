# -*- coding: utf-8 -*-
"""Wire the icon set + share image into site-v4 and add the meta that was missing."""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site-v4")
ICONS = os.path.join(ROOT, "brand", "icons")
IMG = os.path.join(SITE, "assets", "img")

for f in ("icon-16.png", "icon-32.png", "icon-48.png", "icon-180.png"):
    shutil.copyfile(os.path.join(ICONS, f), os.path.join(IMG, f))
shutil.copyfile(os.path.join(ROOT, "brand", "og-image.png"), os.path.join(IMG, "og-image.jpg"))
# name it .jpg? no — keep png, just copy properly
os.remove(os.path.join(IMG, "og-image.jpg"))
shutil.copyfile(os.path.join(ROOT, "brand", "og-image.png"), os.path.join(IMG, "og-image.png"))

p = os.path.join(SITE, "index.html")
html = open(p, encoding="utf-8").read()

old_icon = '<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml" />'
new_icon = ('<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml" />\n'
            '<link rel="icon" href="assets/img/icon-32.png" sizes="32x32" type="image/png" />\n'
            '<link rel="icon" href="assets/img/icon-16.png" sizes="16x16" type="image/png" />\n'
            '<link rel="apple-touch-icon" href="assets/img/icon-180.png" />')
assert html.count(old_icon) == 1
html = html.replace(old_icon, new_icon)

old_og = '<meta property="og:image" content="assets/img/poster-hero.jpg" />'
new_og = ('<meta property="og:image" content="assets/img/og-image.png" />\n'
          '<meta property="og:image:width" content="1200" />\n'
          '<meta property="og:image:height" content="630" />\n'
          '<meta name="twitter:card" content="summary_large_image" />')
assert html.count(old_og) == 1
html = html.replace(old_og, new_og)

# the logo is the wordmark now, so the page title should carry the descriptor
html = html.replace('<title>Higher Heights — Film, Aerial &amp; Photography</title>',
                    '<title>Higher Heights Films — Film, Aerial &amp; Photography</title>')

open(p, "w", encoding="utf-8").write(html)
print("wired icons + og into", p)
