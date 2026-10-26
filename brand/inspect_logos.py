from PIL import Image
import numpy as np, os, sys

SRC = [
    r"C:\Users\Jordan\Downloads\ChatGPT Image Oct 22, 2026, 09_17_16 PM-1.png",
    r"C:\Users\Jordan\Downloads\ChatGPT Image Oct 22, 2026, 09_17_22 PM-2.png",
]
for p in SRC:
    im = Image.open(p)
    print("---", os.path.basename(p), im.size, im.mode)
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    lum = rgb.mean(axis=2)
    print("  alpha min/max", al.min(), al.max())
    print("  lum min/max/mean", lum.min(), round(float(lum.max()), 1), round(float(lum.mean()), 1))
    print("  pixels lum<8:", int((lum < 8).sum()), "of", lum.size)
    idx = np.unravel_index(lum.argmax(), lum.shape)
    print("  brightest rgb", rgb[idx[0], idx[1]], "luma", lum[idx])
    mask = lum > 8
    ys, xs = np.where(mask)
    print("  bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max())
    vals = rgb[mask]
    print("  art mean colour", vals.mean(axis=0).round(1), "p95", np.percentile(vals, 95, axis=0).round(1))
    print("  unique-ish colours (rounded/8):", len(np.unique((rgb[mask] // 8).astype(np.int32), axis=0)))
