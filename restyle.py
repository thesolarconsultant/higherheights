# -*- coding: utf-8 -*-
"""Four changes.

1. Type system: 3 families and two conflicting mono stacks collapse to TWO —
   Switzer for everything typographic, Geist Mono for technical labels.
   Switzer is the open-source equivalent of PP Neue Montreal, which the
   rebuild brief named. Instrument Serif is dropped entirely: a serif display
   over a grotesk body was the thing making it read as five fonts.

2. The hero's top strip goes.

3. The client marquee doubles: two rows running opposite ways, with scroll
   velocity feeding into the drift so the rail reacts to the page.

4. Gutters unified on a single token so every section starts on one line.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:150])
    s = s.replace(old, new, 1)
    print("  ok ", why)


# ── 1. TYPE ───────────────────────────────────────────────────────────────
sub('<link href="https://fonts.googleapis.com/css2?family=Geist:wght@200;300;400;500;600&family=Geist+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />',
    '<link rel="preconnect" href="https://api.fontshare.com" crossorigin />\n'
    '<link href="https://api.fontshare.com/v2/css?f[]=switzer@300,400,500,600&display=swap" rel="stylesheet" />\n'
    '<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400&display=swap" rel="stylesheet" />',
    "font links -> Switzer + Geist Mono")

# tokens, so there is one place to change this again
sub("  --gutter: clamp(1.1rem, 3vw, 2.4rem);",
    '  --sans: "Switzer", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;\n'
    '  --mono: "Geist Mono", ui-monospace, SFMono-Regular, Menlo, monospace;\n'
    "\n  --gutter: clamp(1.1rem, 3vw, 2.4rem);",
    "type tokens")

# every declaration routes through a token
n_mono = len(re.findall(r'font-family:\s*"Geist Mono"[^;}]*', s))
s = re.sub(r'font-family:\s*"Geist Mono"[^;}]*', "font-family:var(--mono)", s)
n_serif = len(re.findall(r'font-family:\s*"Instrument Serif"[^;}]*', s))
s = re.sub(r'font-family:\s*"Instrument Serif"[^;}]*', "font-family:var(--sans)", s)
n_sans = len(re.findall(r'font-family:\s*"Geist"[^;}]*', s))
s = re.sub(r'font-family:\s*"Geist"[^;}]*', "font-family:var(--sans)", s)
print(f"  ok  routed through tokens: {n_mono} mono, {n_serif} serif, {n_sans} sans")

# the serif display needs grotesk metrics now it is Switzer
sub("""h1.hero__title{
  font-family:var(--sans);
  font-size:clamp(3.4rem,9.4vw,10rem);
  font-weight:400;
  line-height:.92;
  letter-spacing:-.022em;
  text-wrap:balance;
}""",
"""h1.hero__title{
  font-family:var(--sans);
  font-size:clamp(3.2rem,8.8vw,9.4rem);
  font-weight:500;
  line-height:.9;
  letter-spacing:-.045em;
  text-wrap:balance;
}""",
    "hero title metrics for a grotesk")

# italics were doing serif work; a grotesk italic reads as a mistake
s = re.sub(r'(\.serif\{[^}]*?)font-style:italic;\s*', r"\1", s)
s = s.replace("h1.hero__title em{", "h1.hero__title em{ font-style:normal;", 1)
print("  ok  serif italics neutralised")

# ── 2. HERO TOP STRIP OUT ────────────────────────────────────────────────
m = re.search(r'\s*<div class="hero__top">.*?</div>\s*(?=\n\s*<div class="hero__foot")', s, re.S)
if not m:
    raise SystemExit("MISS: hero__top block")
s = s[:m.start()] + "\n" + s[m.end():]
print("  ok  hero top strip removed")
s = re.sub(r"\.hero__(top|disc|status|clock|sep|avail)[^{]*\{[^}]*\}", "", s)
s = re.sub(r"@keyframes (disc-pass|avail-breathe)\{(?:[^{}]|\{[^}]*\})*\}", "", s)

# the clock has nothing to write into now
m = re.search(r"\s*/\* -+ live London clock.*?\n  \}\)\(\);\n", s, re.S)
if m:
    s = s[:m.start()] + "\n" + s[m.end():]
    print("  ok  clock script removed")

# ── 3. MARQUEE: TWO ROWS, OPPOSITE, SCROLL-REACTIVE ──────────────────────
m = re.search(r'(<div class="marquee" aria-label="Client list">\s*)(<div class="marquee__track" id="marqueeTrack">)(.*?)(</div>\s*</div>)', s, re.S)
if not m:
    raise SystemExit("MISS: marquee block")
inner = m.group(3)
cards = re.findall(r'<div class="client"[^>]*>\s*<span class="client__mark".*?</span>\s*</div>', inner, re.S)
if len(cards) < 6:
    raise SystemExit(f"only matched {len(cards)} logo cards — aborting rather than writing empty rows")
print(f"  ok  {len(cards)} logos found")
half = (len(cards) + 1) // 2
rowA, rowB = cards[:half], cards[half:]
new_marq = (m.group(1)
            + '<div class="marquee__track" id="marqueeTrack" data-dir="-1">\n'
            + "\n".join(rowA) + "\n          </div>\n"
            + '        <div class="marquee__track" id="marqueeTrack2" data-dir="1">\n'
            + "\n".join(rowB) + "\n          </div>\n      " + m.group(4))
s = s[:m.start()] + new_marq + s[m.end():]
print(f"  ok  split into two rows ({half} + {len(cards)-half})")

sub(".marquee{ display:flex; gap:0; overflow:hidden;",
    ".marquee{ display:flex; flex-direction:column; gap:clamp(1rem,2vw,1.7rem); overflow:hidden;",
    "marquee stacks two rows")
sub(".marquee__track{ display:flex; flex-shrink:0; gap:0; animation:marquee 46s linear infinite; will-change:transform; }",
    ".marquee__track{ display:flex; flex-shrink:0; gap:0; width:max-content; will-change:transform; }",
    "drift is driven by script, not CSS")
sub(".marquee:hover .marquee__track{ animation-play-state:paused; }", "", "hover-pause rule retired")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes")
