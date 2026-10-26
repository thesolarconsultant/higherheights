# -*- coding: utf-8 -*-
"""The numerals survived in two places I had not swept.

The eyebrow labels were de-numbered earlier, but the mobile drawer and every
film card still carried 01-08. Removing both, plus the last accessibility
gaps the audit found: a 9.28px 'Scroll' label and touch targets under 44px.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)

# ── 1. the drawer: numerals out, names stay ──────────────────────────────
s, n1 = re.subn(r'(<a href="#[a-z]+">)<span>\d\d</span>', r"\1", s)
print(f"  ok  drawer numerals removed ({n1})")

# ── 2. film cards: the index span goes entirely ──────────────────────────
s, n2 = re.subn(r'\s*<span class="film__idx">\d\d</span>', "", s)
print(f"  ok  film card numerals removed ({n2})")
s = re.sub(r"\.film__idx\{[^}]*\}", "", s)

# ── 3. the remaining sub-11px label ──────────────────────────────────────
m = re.search(r"\.hero__scroll\{([^}]*)\}", s)
if m and "font-size" in m.group(1):
    s = s[:m.start(1)] + re.sub(r"font-size:[^;]+;", "font-size:var(--fs-micro);", m.group(1)) + s[m.end(1):]
    print("  ok  hero scroll label -> micro token")
else:
    print("  -- hero__scroll has no explicit size")

# ── 4. touch targets to 44px ─────────────────────────────────────────────
ADD = """
/* ── Touch targets: 44px minimum on coarse pointers (WCAG 2.5.8) ── */
@media (pointer:coarse){
  .carousel__arrow{ width:44px; height:44px; }
  .band__mail, .foot__col a, .nav__drawer a, .enq__back{
    min-height:44px; display:flex; align-items:center;
  }
  .foot__col a{ padding:.55rem 0; }
  .marquee__track .client{ min-height:52px; }
}
"""
anchor = "/* ══ Contact band"
if anchor in s:
    s = s.replace(anchor, ADD + "\n" + anchor, 1)
    print("  ok  44px touch targets on coarse pointers")
else:
    raise SystemExit("MISS: anchor for touch-target CSS")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
print("numerals left:", re.findall(r'<span[^>]*>0[1-9]</span>', s) or "none")
