# -*- coding: utf-8 -*-
"""site-v6: migrate the palette to the official Higher Heights Films colour guidelines.

Midnight Navy + Warm Ivory are the identity. Sage Ivory carries hairlines and micro-labels.
Burnt Orange is the occasional accent (interaction only). Greens stay out of the page.
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_history/site-v5")
DST = os.path.join(ROOT, "site-v6")

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

p = os.path.join(DST, "index.html")
html = open(p, encoding="utf-8").read()
done = []


def rep(old, new, label=None):
    global html
    n = html.count(old)
    if not n:
        raise AssertionError(f"missing: {label or old}")
    html = html.replace(old, new)
    done.append(f"{label or old} x{n}")


# ── 1. hard colours ────────────────────────────────────────────────────────
rep("#0B1A26", "#050936", "midnight navy")
rep("#0E2130", "#121D42", "deep navy")
rep("#102838", "#293A70", "royal navy")
rep("#F4EFE6", "#FAF1D0", "warm ivory")
rep("#C9AE7C", "#E5E0AF", "sage ivory (was gold)")
rep("#7A6038", "#121D42", "labels on cream")
rep("rgba(11,26,38,", "rgba(5,9,54,", "ink alpha")
rep("rgba(244,239,230,", "rgba(250,241,208,", "ivory alpha")
rep("rgba(201,174,124,", "rgba(229,224,175,", "sage alpha")
rep("rgba(6,13,20,.96)", "rgba(3,6,36,.96)", "hero scrim")
rep("rgba(0,0,0,.9)", "rgba(5,9,54,.94)", "lightbox backdrop")

# ── 2. tokens ──────────────────────────────────────────────────────────────
rep("--gold-deep: #121D42;", "--gold-deep: #121D42;\n  --hot:        #E78223;\n  --paper:      #FAF5DC;",
    "new tokens: hot accent + paper")

# cream editorial bands use Soft Cream, not the ivory used for type
rep(".band-cream{ background:var(--cream);", ".band-cream{ background:var(--paper);", "cream band ground")

# ── 3. burnt orange only where the user acts ────────────────────────────────
rep(":focus-visible{\n  outline:2px solid var(--gold);", ":focus-visible{\n  outline:2px solid var(--hot);", "focus ring")
rep("::selection{ background:var(--gold);", "::selection{ background:var(--hot);", "selection")
rep(".nav__cta:hover{ background:var(--gold); border-color:var(--gold);",
    ".nav__cta:hover{ background:var(--hot); border-color:var(--hot);", "cta hover")

# ── 4. the wordmark asset is now ivory, not gold ───────────────────────────
rep("assets/img/logo-caps-gold.svg", "assets/img/logo-caps-ivory.svg", "nav wordmark")
rep("assets/img/logo-full-cream.svg", "assets/img/logo-full-ivory.svg", "footer wordmark")

# ── 5. let the footage carry the colour (rule 8) ───────────────────────────
rep("filter:saturate(.72) brightness(.78) contrast(1.1);",
    "filter:saturate(.88) brightness(.86) contrast(1.06);", "hero grade")
rep("rgba(5,9,54,.62) 40%, rgba(5,9,54,.34) 62%, rgba(5,9,54,.58) 100%",
    "rgba(5,9,54,.48) 40%, rgba(5,9,54,.22) 62%, rgba(5,9,54,.52) 100%", "scrim lighter")

# labels over bright sky need help now that gold is gone
rep(".hero__top .mono{ color:var(--gold); }",
    ".hero__top .mono{ color:var(--cream); text-shadow:0 1px 14px rgba(5,9,54,.85); }", "hero labels")

open(p, "w", encoding="utf-8").write(html)
print("wrote", p)
for d in done:
    print("  ✓", d)

leftover = sorted(set(re.findall(r"#(?:0B1A26|C9AE7C|F4EFE6|7A6038)", html)))
print("old colours remaining:", leftover or "none")
