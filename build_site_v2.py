# -*- coding: utf-8 -*-
"""Build site-v2: new identity (mark + wordmark) and new type system on the existing page."""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "higher-heights", "site")
DST = os.path.join(ROOT, "site-v2")
BRAND = os.path.join(ROOT, "brand", "svg")

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

# ── assets ───────────────────────────────────────────────────────────────────
copies = {
    "a-wordmark-cream.svg": "assets/img/wordmark-light.svg",
    "a-wordmark-navy.svg": "assets/img/wordmark-dark.svg",
    "mark-tight-gold.svg": "assets/img/mark-gold.svg",
    "mark-tight-cream.svg": "assets/img/mark-cream.svg",
    "favicon.svg": "assets/img/favicon.svg",
}
for src, dst in copies.items():
    shutil.copyfile(os.path.join(BRAND, src), os.path.join(DST, dst))

p = os.path.join(DST, "index.html")
html = open(p, encoding="utf-8").read()
checks = []


def sub(old, new, count=1, label=""):
    global html
    n = html.count(old)
    assert n == count, f"{label or old[:50]!r}: expected {count} got {n}"
    html = html.replace(old, new)
    checks.append(label or old[:40])


# ── 1. fonts ────────────────────────────────────────────────────────────────
sub(
    'family=Geist:wght@200;300;400;500;600&family=Geist+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap',
    'family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Instrument+Serif:ital@0;1&display=swap',
    label="fonts link")

# ── 2. sans swap ────────────────────────────────────────────────────────────
sub('font-family:"Geist",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;',
    'font-family:"Instrument Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;',
    label="body sans")

# ── 3. mono → sans 500 ──────────────────────────────────────────────────────
n_mono = html.count('font-family:"Geist Mono",monospace;')
html = html.replace('font-family:"Geist Mono",monospace;',
                    'font-family:"Instrument Sans",sans-serif; font-weight:500;')
checks.append(f"mono→sans ({n_mono})")
assert html.count('"Geist Mono",ui-monospace,monospace') == 1
html = html.replace(
    '.mono{\n  font-family:"Geist Mono",ui-monospace,monospace;\n  font-size:var(--fs-micro);\n  font-weight:400;\n  letter-spacing:.19em;',
    '.mono{\n  font-family:"Instrument Sans",sans-serif;\n  font-size:var(--fs-micro);\n  font-weight:500;\n  letter-spacing:.17em;')
checks.append(".mono block")

# ── 4. display → serif ──────────────────────────────────────────────────────
SERIF = 'font-family:"Instrument Serif",Georgia,serif;'

sub("""h1.hero__title{
  font-size:var(--fs-hero);
  font-weight:200;
  line-height:.86;
  letter-spacing:-.045em;""",
    f"""h1.hero__title{{
  {SERIF}
  font-size:var(--fs-hero);
  font-weight:400;
  line-height:.90;
  letter-spacing:-.024em;""",
    label="hero h1")

sub(".sect-head h2{ font-size:var(--fs-h2); font-weight:200; line-height:1; letter-spacing:-.04em; margin-top:.7rem; }",
    f".sect-head h2{{ {SERIF} font-size:var(--fs-h2); font-weight:400; line-height:1.02; letter-spacing:-.022em; margin-top:.7rem; }}",
    label="sect-head h2")

sub(".aerial__copy h2{ font-size:var(--fs-h2); font-weight:200; line-height:1; letter-spacing:-.04em; }",
    f".aerial__copy h2{{ {SERIF} font-size:var(--fs-h2); font-weight:400; line-height:1.02; letter-spacing:-.022em; }}",
    label="aerial h2")

sub(".product__head h2{ font-size:var(--fs-h2); font-weight:200; letter-spacing:-.04em; line-height:1.02; margin-top:.7rem; }",
    f".product__head h2{{ {SERIF} font-size:var(--fs-h2); font-weight:400; letter-spacing:-.022em; line-height:1.04; margin-top:.7rem; }}",
    label="product h2")

sub(".studio__copy h2{ font-size:var(--fs-h2); font-weight:200; letter-spacing:-.04em; line-height:1.02; margin-bottom:1.4rem; }",
    f".studio__copy h2{{ {SERIF} font-size:var(--fs-h2); font-weight:400; letter-spacing:-.022em; line-height:1.04; margin-bottom:1.4rem; }}",
    label="studio h2")

sub("""  font-size:clamp(2.4rem,6.4vw,6.2rem); font-weight:200;
  line-height:.94; letter-spacing:-.045em; margin-top:1.2rem; text-wrap:balance;""",
    f"""  {SERIF}
  font-size:clamp(2.4rem,6.4vw,6.2rem); font-weight:400;
  line-height:.96; letter-spacing:-.026em; margin-top:1.2rem; text-wrap:balance;""",
    label="contact h2")

sub("    font-size:clamp(2rem,9vw,3.2rem); font-weight:300; letter-spacing:-.03em;",
    f"    {SERIF} font-size:clamp(2rem,9vw,3.2rem); font-weight:400; letter-spacing:-.02em;",
    label="drawer links")

# ── 5. wordmark / mark assets ───────────────────────────────────────────────
sub('<img class="brand__mark" src="assets/img/mark-gold.png" alt="" width="588" height="380" />',
    '<img class="brand__mark" src="assets/img/mark-gold.svg" alt="" width="242" height="100" />',
    label="nav mark")

sub('<img class="footer__logo" src="assets/img/logo-light.png" alt="Higher Heights — Film, Aerial, Photography" width="1600" height="357" loading="lazy" />',
    '<img class="footer__logo" src="assets/img/wordmark-light.svg" alt="Higher Heights — Film, Aerial, Photography" width="500" height="108" loading="lazy" />',
    label="footer wordmark")

sub('<link rel="icon" href="assets/img/mark-gold.png" />',
    '<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml" />',
    label="favicon")

# ── 6. signature tracking ───────────────────────────────────────────────────
sub("""  font-size:clamp(.72rem,.86vw,.82rem);
  font-weight:500; letter-spacing:.30em; text-transform:uppercase;""",
    """  font-size:clamp(.74rem,.88vw,.84rem);
  font-weight:500; letter-spacing:.26em; text-transform:uppercase;""",
    label="brand text")

# social preview image (was a relative path — broken on every platform)

open(p, "w", encoding="utf-8").write(html)
print("wrote", p)
print("applied:", len(checks))
for c in checks:
    print("  ✓", c)
