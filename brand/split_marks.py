"""Split the supplied marks into usable lockups:
   wordmark: full lockup (with FILMS) + caps line only (for nav)
   seal:     full badge + extracted central HH monogram (for small sizes)
"""
import os
import numpy as np
from PIL import Image
import potrace

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {
    "wordmark": r"C:\Users\Jordan\Downloads\ChatGPT Image Oct 22, 2026, 09_17_16 PM-1.png",
    "seal": r"C:\Users\Jordan\Downloads\ChatGPT Image Oct 22, 2026, 09_17_22 PM-2.png",
}
OUT = os.path.join(HERE, "logos")
os.makedirs(OUT, exist_ok=True)
NAVY, CREAM, GOLD = (0x0B, 0x1A, 0x26), (0xF4, 0xEF, 0xE6), (0xC9, 0xAE, 0x7C)
COL = {"gold": GOLD, "cream": CREAM, "navy": NAVY}


def alpha_of(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    blue = a[..., 2]
    peak = np.percentile(blue, 99.9)
    al = np.clip(blue / max(peak, 1.0), 0, 1)
    al[al < 0.06] = 0
    return al


def bbox(mask):
    ys, xs = np.where(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def png(alpha_sub, rgb, path):
    h, w = alpha_sub.shape
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = (np.clip(alpha_sub, 0, 1) * 255).round().astype(np.uint8)
    Image.fromarray(out, "RGBA").save(path)


def svg_trace(mask, rgb, path, pad=0):
    bmp = potrace.Bitmap(~np.asarray(mask, dtype=bool))
    t = bmp.trace(turdsize=2, alphamax=1.0, opticurve=1, opttolerance=0.2)
    parts = []
    for curve in t:
        s = curve.start_point
        seg = [f"M{s.x:.2f} {s.y:.2f}"]
        for sg in curve.segments:
            if sg.is_corner:
                c, e = sg.c, sg.end_point
                seg.append(f"L{c.x:.2f} {c.y:.2f}")
                seg.append(f"L{e.x:.2f} {e.y:.2f}")
            else:
                c1, c2, e = sg.c1, sg.c2, sg.end_point
                seg.append(f"C{c1.x:.2f} {c1.y:.2f} {c2.x:.2f} {c2.y:.2f} {e.x:.2f} {e.y:.2f}")
        seg.append("Z")
        parts.append(" ".join(seg))
    h, w = mask.shape
    hexc = "#%02X%02X%02X" % rgb
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
         f'<path d="{" ".join(parts)}" fill="{hexc}" fill-rule="evenodd"/>\n</svg>\n')
    open(path, "w", encoding="utf-8").write(s)
    return len(s)


def row_gaps(mask, min_gap=4):
    rows = mask.any(axis=1)
    gaps, start = [], None
    for i, v in enumerate(rows):
        if not v and start is None:
            start = i
        elif v and start is not None:
            if i - start >= min_gap:
                gaps.append((start, i))
            start = None
    return gaps


def emit(name, alpha, crop, note=""):
    x0, y0, x1, y1 = crop
    sub = alpha[y0:y1, x0:x1]
    m = sub > 0.5
    info = {"name": name, "size": (x1 - x0, y1 - y0), "note": note}
    for label, rgb in COL.items():
        png(sub, rgb, os.path.join(OUT, f"{name}-{label}.png"))
        n = svg_trace(m, rgb, os.path.join(OUT, f"{name}-{label}.svg"))
        info.setdefault("svg_bytes", n)
    return info


# ── wordmark ────────────────────────────────────────────────────────────────
wa = alpha_of(SRC["wordmark"])
wb = bbox(wa > 0.5)
full = emit("wm-full", wa, (wb[0], wb[1], wb[2], wb[3]), "HIGHER HEIGHTS + FILMS")

gaps = row_gaps(wa[wb[1]:wb[3], wb[0]:wb[2]] > 0.5, 6)
print("row gaps (relative):", gaps)
# split above the descriptor line: the largest gap in the lower half
if gaps:
    gy = max(gaps, key=lambda g: g[1] - g[0])
    split = wb[1] + gy[0] + (gy[1] - gy[0]) // 2
    caps = emit("wm-caps", wa, (wb[0], wb[1], wb[2], split), "caps line only")
    desc = emit("wm-films", wa, (wb[0], split, wb[2], wb[3]), "FILMS descriptor only")
    print(full, caps, desc)

# ── seal ────────────────────────────────────────────────────────────────────
sa = alpha_of(SRC["seal"])
sb = bbox(sa > 0.5)
seal = emit("seal", sa, (sb[0], sb[1], sb[2], sb[3]), "full badge")
print(seal)

# central monogram: ink inside a centred disc, ignoring the ring & arced type
h, w = sa.shape
cy, cx = (sb[1] + sb[3]) / 2, (sb[0] + sb[2]) / 2
yy, xx = np.mgrid[0:h, 0:w]
r = 0.30 * max(w, h)
inner = ((yy - cy) ** 2 + (xx - cx) ** 2) < r * r
mono = sa * inner
mb = bbox(mono > 0.5)
mono_lk = emit("seal-mark", sa, (mb[0], mb[1], mb[2], mb[3]), "central HH + ribbon")
print(mono_lk)
