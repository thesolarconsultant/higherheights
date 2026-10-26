"""Extract the two supplied logo bitmaps -> clean solid-colour assets + traced vectors.

The source art is a single hue (dark blue) on black with antialiasing, so the alpha
channel can be recovered exactly from the blue channel and the art recoloured to any
brand colour with no fringing.
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

NAVY = (0x0B, 0x1A, 0x26)
CREAM = (0xF4, 0xEF, 0xE6)
GOLD = (0xC9, 0xAE, 0x7C)


def load_mask(path):
    """Returns float alpha 0..1 cropped to the art, plus the padded bbox."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    blue = a[..., 2]
    peak = np.percentile(blue, 99.9)
    alpha = np.clip(blue / max(peak, 1.0), 0, 1)
    # kill residual noise from the black field
    alpha[alpha < 0.06] = 0.0
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return alpha, (x0, y0, x1, y1)


def colourise(alpha, rgb, crop):
    x0, y0, x1, y1 = crop
    sub = alpha[y0:y1, x0:x1]
    h, w = sub.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = (sub * 255).round().astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def write_svg(mask_bool, colour, path, scale=1.0, precision=2):
    bmp = potrace.Bitmap(~np.asarray(mask_bool, dtype=bool))
    traced = bmp.trace(turdsize=2, alphamax=1.0, opticurve=1, opttolerance=0.2)
    parts = []
    for curve in traced:
        s = curve.start_point
        seg = [f"M{s.x*scale:.{precision}f} {s.y*scale:.{precision}f}"]
        for segment in curve.segments:
            if segment.is_corner:
                c = segment.c
                e = segment.end_point
                seg.append(f"L{c.x*scale:.{precision}f} {c.y*scale:.{precision}f}")
                seg.append(f"L{e.x*scale:.{precision}f} {e.y*scale:.{precision}f}")
            else:
                c1, c2, e = segment.c1, segment.c2, segment.end_point
                seg.append(
                    f"C{c1.x*scale:.{precision}f} {c1.y*scale:.{precision}f} "
                    f"{c2.x*scale:.{precision}f} {c2.y*scale:.{precision}f} "
                    f"{e.x*scale:.{precision}f} {e.y*scale:.{precision}f}")
        seg.append("Z")
        parts.append(" ".join(seg))
    h, w = mask_bool.shape
    hexc = "#%02X%02X%02X" % colour
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}">\n'
           f'<path d="{" ".join(parts)}" fill="{hexc}" fill-rule="evenodd"/>\n</svg>\n')
    open(path, "w", encoding="utf-8").write(svg)
    return len(svg), len(parts)


def main():
    report = {}
    for name, src in SRC.items():
        alpha, crop = load_mask(src)
        h, w = alpha.shape
        cw, ch = crop[2] - crop[0], crop[3] - crop[1]
        report[name] = {"src_size": (w, h), "art_size": (cw, ch)}

        # PNG masters at source resolution, brand colours
        for label, rgb in (("gold", GOLD), ("cream", CREAM), ("navy", NAVY)):
            img = colourise(alpha, rgb, crop)
            p = os.path.join(OUT, f"{name}-{label}.png")
            img.save(p)
            report[name].setdefault("png", {})[label] = [p, img.size]

        # traced vectors from a 0.5 threshold
        x0, y0, x1, y1 = crop
        mask = alpha[y0:y1, x0:x1] > 0.5
        for label, rgb in (("gold", GOLD), ("cream", CREAM), ("navy", NAVY)):
            p = os.path.join(OUT, f"{name}-{label}.svg")
            size, ncurves = write_svg(mask, rgb, p)
            report[name].setdefault("svg", {})[label] = [size, ncurves]

    for k, v in report.items():
        print(k)
        print("   source", v["src_size"], "art", v["art_size"])
        for row in v.get("svg", {}).items():
            print("   svg", row[0], row[1])


if __name__ == "__main__":
    main()
