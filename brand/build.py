# -*- coding: utf-8 -*-
"""Build Higher Heights logo SVGs (outlined text, real vectors).

Device: the stepped horizon (a line that gains height) — the mark.
Deployments:
  A = pure serif wordmark (primary)
  B = mark + tracked caps (evolution of the current mark-over-wordmark)
  C = stacked title card (also the end-card asset)
"""
import os
import text2svg as T

HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda n: T.Face(os.path.join(HERE, "fonts", n))
SERIF = F("InstrumentSerif-Regular.ttf")
ITAL = F("InstrumentSerif-Italic.ttf")
SANS = F("InstrumentSans-Medium.ttf")

NAVY = "#0B1A26"
CREAM = "#F4EFE6"
GOLD = "#C9AE7C"

OUT = os.path.join(HERE, "svg")
os.makedirs(OUT, exist_ok=True)

S = 100.0
TRACK = -0.010
WORDSPACE = 0.070
CAP = 72.0
DESC = 31.0


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def rect(x, y, w, h, fill):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"/>'


def path(d, fill):
    return f'<path d="{d}" fill="{fill}"/>'


def doc(x, y, w, h, body, label="Higher Heights"):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(x)} {fmt(y)} {fmt(w)} {fmt(h)}" '
        f'width="{fmt(w)}" height="{fmt(h)}" role="img" aria-label="{label}">\n'
        + "\n".join(body) + "\n</svg>\n"
    )


def step_rule(x0, x1, xstep, y_low, y_high, t, fill, il=0.0, ir=0.0):
    a, b = x0 + il, x1 - ir
    return [
        rect(a, y_low, xstep - a, t, fill),
        rect(xstep, y_high, b - xstep, t, fill),
        rect(xstep, y_high, t, (y_low + t) - y_high, fill),
    ]


def step_mark(h, fill, at=(0.0, 0.0)):
    """The mark scaled to height h, positioned at (x,y)."""
    t = h * 0.205
    y_low = h * 0.795
    y_high = h * 0.0
    w = h * 2.42
    xstep = w * 0.405
    ox, oy = at
    return [
        rect(ox, oy + y_low, xstep, t, fill),
        rect(ox + xstep, oy + y_high, w - xstep, t, fill),
        rect(ox + xstep, oy + y_high, t, y_low + t - y_high, fill),
    ], w


# ── A. WORDMARK ───────────────────────────────────────────────────────────────
def build_wordmark(ink, accent=None, rule=False):
    d, W = T.paths(SERIF, "Higher Heights", S, TRACK, WORDSPACE)
    body = [path(d, ink)]
    bottom = 2.0
    if rule:
        w_hi = SERIF.measure("Higher", S, TRACK)
        w_hi_sp = SERIF.measure("Higher ", S, TRACK, WORDSPACE)
        xstep = (w_hi + w_hi_sp) / 2.0
        y_low, y_high, t = DESC + 12, DESC + 12 - 12, 2.2
        body += step_rule(0, W, xstep, y_low, y_high, t, accent, 3.0, 2.0)
        bottom = y_low + t + 1
    top = -CAP - 2
    return doc(0, top, W + 1, bottom - top, body)


def build_wordmark_stacked(ink, accent):
    lead = 114.0
    d1, w1 = T.paths(SERIF, "Higher", S, TRACK, dy=0)
    d2, w2 = T.paths(SERIF, "Heights", S, TRACK, dy=lead)
    W = max(w1, w2)
    body = [path(d1, ink), path(d2, ink)]
    y_low, y_high, t = lead + DESC + 12, lead + DESC, 2.2
    body += step_rule(0, W, w2 * 0.47, y_low, y_high, t, accent, 3.0, 2.0)
    top = -CAP - 2
    bottom = y_low + t + 1
    return doc(0, top, W + 1, bottom - top, body)


# ── B. MARK + TRACKED CAPS ───────────────────────────────────────────────────
def build_signature_h(ink, accent):
    word_size, tr = 15.0, 0.28
    mark, mw = step_mark(26.0, accent)
    W = SANS.measure("HIGHER HEIGHTS", word_size, tr)
    gap = 19.0
    cap = SANS.cap_height(word_size)
    baseline = 13.0 + cap / 2.0
    body = list(mark)
    d, _ = T.paths(SANS, "HIGHER HEIGHTS", word_size, tr, dx=mw + gap, dy=baseline)
    body.append(path(d, ink))
    return doc(0, -1, mw + gap + W, 28.0, body)


def build_signature_stack(ink, accent):
    word_size, tr = 20.0, 0.30
    W = SANS.measure("HIGHER HEIGHTS", word_size, tr)
    mark_h = 30.0
    _, mw = step_mark(mark_h, accent)
    total = max(W, mw)
    body = list(step_mark(mark_h, accent, at=((total - mw) / 2.0, 0))[0])
    d, _ = T.paths(SANS, "HIGHER HEIGHTS", word_size, tr, dx=(total - W) / 2.0, dy=mark_h + 34.0)
    body.append(path(d, ink))
    return doc(0, 0, total, mark_h + 34.0 + 2.0, body)


# ── C. TITLE CARD ─────────────────────────────────────────────────────────────
def build_titlecard(ink, accent):
    size, tr = 100.0, 0.085
    d1, w1 = T.paths(SERIF, "HIGHER", size, tr, dy=0)
    d2, w2 = T.paths(SERIF, "HEIGHTS", size, tr, dy=116.0)
    cap = SERIF.cap_height(size)
    W = max(w1, w2)
    t = 1.6
    top_y = -cap - 30
    bot_y = 116.0 + 26
    tag_d, tag_w = T.paths(SANS, "FILM · AERIAL · PHOTOGRAPHY", 10.6, 0.36, dy=bot_y + 31)
    body = [
        rect(0, top_y, W, t, accent),
        path(d1, ink),
        path(d2, ink),
        rect(0, bot_y, W, t, accent),
        path(tag_d, ink),
    ]
    return doc(0, top_y, W, bot_y + 31 + 4 - top_y, body)


# ── icons ────────────────────────────────────────────────────────────────────
def build_icon(accent, box=100.0):
    mark_h = box * 0.40
    _, mw = step_mark(mark_h, accent)
    body = list(step_mark(mark_h, accent, at=((box - mw) / 2.0, (box - mark_h - mark_h * 0.30) / 2.0))[0])
    return doc(0, 0, box, box, body)


def build_mark_tight(accent):
    mark, w = step_mark(100.0, accent)
    return doc(0, 0, w, 100, list(mark))


def build_favicon(bg=NAVY, accent=GOLD):
    box = 64.0
    mark_h = 18.0
    _, mw = step_mark(mark_h, accent)
    body = [f'<rect width="{fmt(box)}" height="{fmt(box)}" fill="{bg}"/>']
    body += step_mark(mark_h, accent, at=((box - mw) / 2.0, (box - mark_h - mark_h * 0.30) / 2.0))[0]
    return doc(0, 0, box, box, body)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:42s} {len(content):7d} bytes")


if __name__ == "__main__":
    write("a-wordmark-navy.svg", build_wordmark(NAVY))
    write("a-wordmark-cream.svg", build_wordmark(CREAM))
    write("a-wordmark-rule-navy.svg", build_wordmark(NAVY, GOLD, rule=True))
    write("a-wordmark-rule-cream.svg", build_wordmark(CREAM, GOLD, rule=True))
    write("a-stacked-navy.svg", build_wordmark_stacked(CREAM, GOLD))
    write("a-stacked-cream.svg", build_wordmark_stacked(NAVY, GOLD))
    write("b-signature-h-cream.svg", build_signature_h(NAVY, GOLD))
    write("b-signature-h-navy.svg", build_signature_h(CREAM, GOLD))
    write("b-signature-stack-cream.svg", build_signature_stack(NAVY, GOLD))
    write("b-signature-stack-navy.svg", build_signature_stack(CREAM, GOLD))
    write("c-titlecard-cream.svg", build_titlecard(NAVY, GOLD))
    write("c-titlecard-navy.svg", build_titlecard(CREAM, GOLD))
    write("mark-gold.svg", build_icon(GOLD))
    write("mark-cream.svg", build_icon(CREAM))
    write("mark-navy.svg", build_icon(NAVY))
    write("mark-tight-gold.svg", build_mark_tight(GOLD))
    write("mark-tight-cream.svg", build_mark_tight(CREAM))
    write("mark-tight-navy.svg", build_mark_tight(NAVY))
    write("favicon.svg", build_favicon())
    write("favicon-cream.svg", build_favicon(bg=CREAM, accent=NAVY))
