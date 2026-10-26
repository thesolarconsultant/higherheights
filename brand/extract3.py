"""Extract the three new logo files.

#1 Polished Navy Double H Emblem  -> 3D render, keep as PNG (gradients can't be vectorised)
#2 Elegant Double H Monogram      -> flat mark, trace to vector
#3 HIGHER HEIGHTS / FILMS         -> wordmark, trace to vector
"""
import os
import numpy as np
from PIL import Image
import potrace

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "logos2")
os.makedirs(OUT, exist_ok=True)

SRC = {
    "hh3d": r"C:\Users\Jordan\Downloads\Polished Navy Double H Emblem.png",
    "hhflat": r"C:\Users\Jordan\Downloads\Elegant Double H Monogram Logo.png",
    "wordmark": r"C:\Users\Jordan\Downloads\ChatGPT Image Oct 23, 2026, 08_57_00 PM-2.png",
}
NAVY, CREAM, GOLD = (0x0B, 0x1A, 0x26), (0xF4, 0xEF, 0xE6), (0xC9, 0xAE, 0x7C)
COL = {"navy": NAVY, "cream": CREAM, "gold": GOLD}


def rgba(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)


def crop(a, pad=0):
    al = a[..., 3]
    ys, xs = np.where(al > 8)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + 1 + pad)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + 1 + pad)
    return a[y0:y1, x0:x1]


def recolour(a, rgb, path):
    """Keep the source antialiasing, replace the colour."""
    h, w = a.shape[:2]
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = a[..., 3].round().astype(np.uint8)
    Image.fromarray(out, "RGBA").save(path)
    return (w, h)


def trace(a, rgb, path):
    mask = (a[..., 3] > 127)
    bmp = potrace.Bitmap(~mask)
    t = bmp.trace(turdsize=2, alphamax=1.0, opticurve=1, opttolerance=0.2)
    parts = []
    for c in t:
        s = c.start_point
        seg = [f"M{s.x:.2f} {s.y:.2f}"]
        for sg in c.segments:
            if sg.is_corner:
                p, e = sg.c, sg.end_point
                seg.append(f"L{p.x:.2f} {p.y:.2f}")
                seg.append(f"L{e.x:.2f} {e.y:.2f}")
            else:
                c1, c2, e = sg.c1, sg.c2, sg.end_point
                seg.append(f"C{c1.x:.2f} {c1.y:.2f} {c2.x:.2f} {c2.y:.2f} {e.x:.2f} {e.y:.2f}")
        seg.append("Z")
        parts.append(" ".join(seg))
    h, w = mask.shape
    hexc = "#%02X%02X%02X" % rgb
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
           f'<path d="{" ".join(parts)}" fill="{hexc}" fill-rule="evenodd"/>\n</svg>\n')
    open(path, "w", encoding="utf-8").write(svg)
    return w, h, len(svg), len(parts)


report = {}

# ── 2. flat monogram ────────────────────────────────────────────────────────
a = crop(rgba(SRC["hhflat"]))
report["hhflat"] = {"size": (a.shape[1], a.shape[0])}
for name, rgb in COL.items():
    recolour(a, rgb, os.path.join(OUT, f"hh-flat-{name}.png"))
    w, h, n, curves = trace(a, rgb, os.path.join(OUT, f"hh-flat-{name}.svg"))
    report["hhflat"][name] = {"curves": curves, "bytes": n}

# ── 3. wordmark ─────────────────────────────────────────────────────────────
b = crop(rgba(SRC["wordmark"]))
report["wordmark"] = {"size": (b.shape[1], b.shape[0])}
for name, rgb in COL.items():
    recolour(b, rgb, os.path.join(OUT, f"wordmark-{name}.png"))
    w, h, n, curves = trace(b, rgb, os.path.join(OUT, f"wordmark-{name}.svg"))
    report["wordmark"][name] = {"curves": curves, "bytes": n}

# ── 1. 3D render: keep as PNG, a couple of sizes for social/end-card use ───
c = crop(rgba(SRC["hh3d"]))
im = Image.fromarray(c.astype(np.uint8), "RGBA")
report["hh3d"] = {"size": im.size, "sizes": {}}
for px in (1024, 512, 256):
    r = im.copy()
    r.thumbnail((px, px), Image.LANCZOS)
    p = os.path.join(OUT, f"hh-3d-{px}.png")
    r.save(p)
    report["hh3d"]["sizes"][px] = os.path.getsize(p)

for k, v in report.items():
    print(k, v)
