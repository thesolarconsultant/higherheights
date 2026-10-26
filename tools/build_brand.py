# -*- coding: utf-8 -*-
"""Build the brand into the ORIGINAL site: real marks, watermarks, no numerals.
   Layout, palette and copy are left exactly as they are."""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "higher-heights", "site")
DST = os.path.join(ROOT, "site-brand")
BRAND = os.path.join(ROOT, "brand")

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
IMG = os.path.join(DST, "assets", "img")

# ── ship the supplied marks ───────────────────────────────────────────────
pairs = [
    ("logos2/hh-flat-cream.svg", "hh-cream.svg"),
    ("logos2/hh-flat-gold.svg",  "hh-gold.svg"),
    ("logos2/hh-flat-navy.svg",  "hh-navy.svg"),
    ("logos2/wordmark-cream.svg", "wordmark-cream.svg"),
    ("logos2/wordmark-gold.svg",  "wordmark-gold.svg"),
    ("logos/wm-caps-gold.svg",    "caps-gold.svg"),
    ("logos/wm-caps-cream.svg",   "caps-cream.svg"),
]
for s, d in pairs:
    p = os.path.join(BRAND, s)
    if os.path.exists(p):
        shutil.copy(p, os.path.join(IMG, d))
        print("  +", d)
    else:
        print("  !! missing", s)

p = os.path.join(DST, "index.html")
s = open(p, encoding="utf-8").read()
start_len = len(s)


def sub(old, new, why, count=1):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:130])
    s = s.replace(old, new, count)
    print("  ok ", why)


# ── 1. the numerals go ────────────────────────────────────────────────────
n_before = len(re.findall(r'<span class="eyebrow__num">\(\d\d\)</span>', s))
s = re.sub(r'\s*<span class="eyebrow__num">\(\d\d\)</span>\s*', "\n        ", s)
print(f"  ok  removed {n_before} eyebrow numerals")

# the rule that styled them can go too, so nothing reserves the space
s = re.sub(r"\.eyebrow__num\{[^}]*\}", "", s)

# ── 2. real marks where the placeholders were ─────────────────────────────
sub('<link rel="icon" href="assets/img/mark-gold.png" />',
    '<link rel="icon" href="assets/img/hh-gold.svg" type="image/svg+xml" />\n'
    '<link rel="apple-touch-icon" href="assets/img/icon-180.png" />',
    "favicon -> HH mark")

sub('<img class="brand__mark" src="assets/img/mark-gold.png" alt="" width="588" height="380" />',
    '<img class="brand__mark" src="assets/img/hh-gold.svg" alt="" width="713" height="854" />',
    "hero brand mark -> HH monogram")

sub('<img class="footer__logo" src="assets/img/logo-light.png" '
    'alt="Higher Heights — Film, Aerial, Photography" width="1600" height="357" loading="lazy" />',
    '<img class="footer__logo" src="assets/img/wordmark-cream.svg" '
    'alt="Higher Heights — Film, Aerial, Photography" width="1600" height="357" loading="lazy" />',
    "footer logo -> supplied wordmark")

# ── 3. watermark styling ──────────────────────────────────────────────────
sub(".band-cream{ background:var(--cream); color:var(--ink); position:relative; }",
    """.band-cream{ background:var(--cream); color:var(--ink); position:relative; }
.hh-wm{ position:absolute; z-index:0; pointer-events:none; user-select:none; }
.hh-wm img{ display:block; width:100%; height:auto; }
.hh-wm--studio{ right:-6%; bottom:-14%; width:min(42%,460px); opacity:.055; }
.hh-wm--contact{ left:-7%; top:-10%; width:min(38%,420px); opacity:.07; }
.studio .wrap, .contact .wrap{ position:relative; z-index:1; }
@media(max-width:860px){
  .hh-wm--studio{ right:-16%; bottom:-6%; width:min(62%,300px); opacity:.05; }
  .hh-wm--contact{ left:-18%; top:-4%; width:min(58%,280px); opacity:.06; }
}""",
    "watermark CSS")

sub(".studio{ padding:var(--sect) 0; background:var(--cream); color:var(--ink); }",
    ".studio{ padding:var(--sect) 0; background:var(--cream); color:var(--ink); "
    "position:relative; overflow:hidden; }",
    "studio becomes a stage")

# ── 4. watermark markup ───────────────────────────────────────────────────
sub('<section class="studio" id="studio" aria-labelledby="studio-head">\n    <div class="wrap">',
    '<section class="studio" id="studio" aria-labelledby="studio-head">\n'
    '    <div class="hh-wm hh-wm--studio" aria-hidden="true"><img src="assets/img/hh-navy.svg" alt=""></div>\n'
    '    <div class="wrap">',
    "studio watermark (navy on cream)")

sub('<section class="contact" id="contact" aria-labelledby="contact-head">\n    <div class="wrap">',
    '<section class="contact" id="contact" aria-labelledby="contact-head">\n'
    '    <div class="hh-wm hh-wm--contact" aria-hidden="true"><img src="assets/img/hh-cream.svg" alt=""></div>\n'
    '    <div class="wrap">',
    "contact watermark (cream on navy)")

open(p, "w", encoding="utf-8").write(s)
print(f"\nsite-brand written: {start_len} -> {len(s)} bytes")
print("numerals left:", re.findall(r"\(0\d\)", s) or "none")
