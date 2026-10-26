# -*- coding: utf-8 -*-
"""Process the newly sourced logos through the same pipeline as the first 14,
then merge them into the client set and regenerate the marquee."""
import os, sys, json, shutil, colorsys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "brand", "sourced")
CLI = os.path.join(ROOT, "brand", "clients")
SITE = os.path.join(ROOT, "site-brand")
IMG = os.path.join(SITE, "assets", "img", "clients")

NEW = [
    ("ladbible",    "ladbible.png",    "LADbible Group"),
    ("matchroom",   "matchroom.png",   "Matchroom"),
    ("nobl",        "nobl.png",        "NOBL"),
    ("oakridge",    "oakridge.png",    "Oakridge Property Group"),
    ("richardmille","richardmille.png","Richard Mille"),
    ("watchtrader", "watchtrader.png", "WatchTrader & Co"),   # replaces the screenshot
]

NAVY_L = 0.075
CREAM = "#F4EFE6"


def ink_alpha(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    ink = 255.0 - rgb.min(axis=2)
    if al.min() < 250:
        ink = np.minimum(ink * 2.2, 255.0) * (al / 255.0)
        if ink.max() < 40:
            ink = al.copy()
    return np.clip(ink, 0, 255)


def crop_box(mask, pad=2):
    ys, xs = np.where(mask > 10)
    if not len(ys):
        return None
    return (max(0, xs.min() - pad), max(0, ys.min() - pad),
            min(mask.shape[1], xs.max() + 1 + pad), min(mask.shape[0], ys.max() + 1 + pad))


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def lift(h):
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    out = h
    for _ in range(16):
        out = "#%02X%02X%02X" % tuple(round(x * 255) for x in colorsys.hls_to_rgb(hh, l, s))
        if (lum(out) + .05) / (NAVY_L + .05) >= 3.0:
            break
        l = min(0.95, l + 0.055)
    return out


rep = json.load(open(os.path.join(CLI, "sized.json")))
by_slug = {r["slug"]: r for r in rep}

import math
K = 4200.0
for slug, fname, label in NEW:
    p = os.path.join(SRC, fname)
    if not os.path.exists(p):
        print("  !! missing", fname); continue
    mask = ink_alpha(p)
    box = crop_box(mask)
    if box is None:
        print("  !! empty", slug); continue
    m = mask[box[1]:box[3], box[0]:box[2]]
    cov = float((m > 32).mean())
    h, w = m.shape
    aspect = w / h

    big = Image.fromarray(np.clip(m, 0, 255).astype(np.uint8), "L")
    big.thumbnail((1400, 1400), Image.LANCZOS)
    m2 = np.asarray(big).astype(np.float32)
    out = np.zeros((*m2.shape, 4), np.uint8)
    out[..., 0:3] = 255
    out[..., 3] = m2.round().astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(CLI, slug + "-white.png"))

    # optical size
    dw = math.sqrt(K * aspect / max(cov, 0.05)); dh = dw / aspect
    if dh > 56: dh = 56; dw = dh * aspect
    if dh < 20: dh = 20; dw = dh * aspect
    if dw > 190: dw = 190; dh = dw / aspect

    # brand colour from the original
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    sel = (255 - rgb.min(2) > 60) & (al > 120)
    px = rgb[sel]
    chromatic = False
    brand = "#FFFFFF"
    if len(px):
        sat = px.max(1) - px.min(1)
        col = px[sat > 40]
        chromatic = len(col) > len(px) * 0.12
        chosen = np.median(col, 0) if chromatic else np.median(px, 0)
        brand = "#%02X%02X%02X" % tuple(int(c) for c in chosen)

    rec = {"slug": slug, "label": label, "w": w, "h": h,
           "aspect": round(aspect, 2), "coverage": round(cov, 3),
           "dw": round(dw), "dh": round(dh), "brand": brand,
           "chromatic": bool(chromatic),
           "tint": CREAM if not chromatic else lift(brand)}
    by_slug[slug] = rec
    shutil.copy(os.path.join(CLI, slug + "-white.png"), os.path.join(IMG, slug + ".png"))
    print(f"  {slug:14s} {aspect:5.2f} cov {cov:.3f} -> {rec['dw']:3d}x{rec['dh']:3d}  "
          f"{brand} -> {rec['tint']}" + ("" if chromatic else "  (achromatic)"))

# keep a sensible order: the names that argue for the positioning first
ORDER = ["richardmille", "matchroom", "watchtrader", "whoop", "ladbible", "nobl",
         "aduna", "cleanco", "oakridge", "real", "crowdcube", "jimjam",
         "melissa", "tecrec", "hybrid", "everyones", "dayswork", "piemash", "tj", "be"]
merged = [by_slug[s] for s in ORDER if s in by_slug]
merged += [r for r in by_slug.values() if r["slug"] not in ORDER]
json.dump(merged, open(os.path.join(CLI, "sized.json"), "w"), indent=2)
print(f"\n  total clients: {len(merged)}")
