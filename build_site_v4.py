# -*- coding: utf-8 -*-
"""site-v4 (final): wordmark primary + HH icon, Bodoni Moda display, Instrument Sans text."""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site-v3")
DST = os.path.join(ROOT, "site-v4")

if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

p = os.path.join(DST, "index.html")
html = open(p, encoding="utf-8").read()
done = []


def sub(old, new, count=None, label=""):
    global html
    n = html.count(old)
    assert n >= 1 and (count is None or n == count), f"{label}: got {n}"
    html = html.replace(old, new)
    done.append(f"{label} x{n}")


# 1. fonts: drop Instrument Serif, add Bodoni Moda
sub('family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Instrument+Serif:ital@0;1&display=swap',
    'family=Instrument+Sans:ital,wght@0,400..700;1,400..700&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&display=swap',
    label="font link")

# 2. every serif role -> Bodoni Moda
n = html.count('"Instrument Serif",Georgia,serif')
html = html.replace('"Instrument Serif",Georgia,serif', '"Bodoni Moda",Georgia,serif')
done.append(f"serif->Bodoni x{n}")

# 3. didone metrics: scale up (narrower face), relax tracking, more leading
sub('--fs-hero:  clamp(3rem, 8.6vw, 9.2rem);', '--fs-hero:  clamp(3.1rem, 9.3vw, 10.1rem);', label="hero scale")
sub('--fs-h2:    clamp(2.1rem, 4.6vw, 4.4rem);', '--fs-h2:    clamp(2.3rem, 5.15vw, 4.95rem);', label="h2 scale")
sub('--fs-state: clamp(1.55rem, 3.5vw, 3.15rem);', '--fs-state: clamp(1.65rem, 3.7vw, 3.4rem);', label="statement scale")
sub('  line-height:.90;', '  line-height:.955;', label="hero leading")
sub('  letter-spacing:-.024em;', '  letter-spacing:-.014em;', label="hero tracking")
sub('font-weight:400; line-height:1.02; letter-spacing:-.022em;',
    'font-weight:400; line-height:1.06; letter-spacing:-.012em;', label="h2 metrics")
sub('font-weight:400; letter-spacing:-.022em; line-height:1.04;',
    'font-weight:400; letter-spacing:-.012em; line-height:1.07;', label="h2 metrics alt")
sub('  line-height:.96; letter-spacing:-.026em; margin-top:1.2rem; text-wrap:balance;',
    '  line-height:1.0; letter-spacing:-.016em; margin-top:1.2rem; text-wrap:balance;', label="contact metrics")
sub('  font-size:var(--fs-state); line-height:1.14; letter-spacing:-.022em;',
    '  font-size:var(--fs-state); line-height:1.16; letter-spacing:-.012em;', label="statement metrics")
sub('  font-size:clamp(1.35rem,2.2vw,1.95rem); line-height:1.22; letter-spacing:-.02em;',
    '  font-size:clamp(1.35rem,2.2vw,1.95rem); line-height:1.26; letter-spacing:-.01em;', label="quote metrics")
sub('font-size:clamp(2.4rem,6.4vw,6.2rem); font-weight:400;',
    'font-size:clamp(2.6rem,6.9vw,6.7rem); font-weight:400;', label="contact scale")

open(p, "w", encoding="utf-8").write(html)
print("wrote", p)
for d in done:
    print("  ✓", d)
