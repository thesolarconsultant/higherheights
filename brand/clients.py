# -*- coding: utf-8 -*-
"""Normalise client logos: knock out the background, render as one ink colour,
   crop to content, and balance optical weight so a wide wordmark and a round
   seal carry the same presence on the wall."""
import os, json
import numpy as np
from PIL import Image

SRC = r"C:\Users\Jordan\AppData\Roaming\Hermes\composer-images"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "clients")
os.makedirs(OUT, exist_ok=True)

LOGOS = [
    ("whoop",       "whoop-logo-vector_9f998a.png",                       "WHOOP"),
    ("aduna",       "aduna-logo-sunset-rgb-900px-w-72ppi_cdbe0e.png",     "Aduna Superfoods"),
    ("cleanco",     "C0105.00_00_16_13.Still001_b5570f.png",              "Clean Co"),
    ("watchtrader", "Screenshot_2026-10-22_at_10.22.36_ebe7fe.png",       "WatchTrader & Co"),
    ("real",        "The_REAL_Drinks_Co._Logo_Wordmark_Horizontal_1_1_348c34.png", "The REAL Drinks Co"),
    ("crowdcube",   "Cc_logo-RGB-orange_1b41eb.png",                      "Crowdcube"),
    ("tecrec",      "TR_Wide_RGB_HR_8b6c4e.png",                          "TecRec"),
    ("hybrid",      "Hybrid_Combination_Master_Horizontal_RGB300_49e936.png", "Hybrid Fitness"),
    ("everyones",   "EE_Logo_No_Slogan_b7ac5a.png",                       "Everyone's Energy"),
    ("dayswork",    "Dayswork_png_black_writing_373a86.png",              "Days Work"),
    ("jimjam",      "JIM_JAM_THE_LABEL_LOGO_863e6b.jpg",                  "JimJam The Label"),
    ("piemash",     "Untitled_design_5_1f6bb9.png",                       "Tony's Pie & Mash"),
    ("tj",          "Screenshot_2026-10-22_at_10.21.55_6e32a3.png",       "TJ"),
    ("be",          "PHOTO-2024-09-08-05-39-35_2_599118.jpg",             "Be"),
]


def ink_alpha(path):
    """Alpha mask of the artwork, whatever the source background."""
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]

    # how far each pixel is from white = how much ink it carries
    ink = 255.0 - rgb.min(axis=2)

    # a genuinely transparent source already tells us the shape
    if al.min() < 250:
        ink = np.minimum(ink * 2.2, 255.0)        # lift pale-but-present strokes
        ink = ink * (al / 255.0)
        # a transparent PNG whose art is near-white (e.g. knockout) still needs shape
        if ink.max() < 40:
            ink = al.copy()
    return np.clip(ink, 0, 255)


def crop(mask, pad=2):
    ys, xs = np.where(mask > 10)
    if not len(ys):
        return None
    return (max(0, xs.min() - pad), max(0, ys.min() - pad),
            min(mask.shape[1], xs.max() + 1 + pad), min(mask.shape[0], ys.max() + 1 + pad))


def render(mask, colour, path):
    h, w = mask.shape
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = colour
    out[..., 3] = mask.round().astype(np.uint8)
    Image.fromarray(out, "RGBA").save(path)


report = []
for slug, fname, label in LOGOS:
    p = os.path.join(SRC, fname)
    if not os.path.exists(p):
        report.append({"slug": slug, "error": "missing " + fname})
        continue
    mask = ink_alpha(p)
    box = crop(mask)
    if box is None:
        report.append({"slug": slug, "error": "empty mask"})
        continue
    m = mask[box[1]:box[3], box[0]:box[2]]

    # optical weight: how much of the box is actually inked
    coverage = float((m > 32).mean())
    h, w = m.shape
    report.append({
        "slug": slug, "label": label, "w": w, "h": h,
        "aspect": round(w / h, 2), "coverage": round(coverage, 3),
    })

    big = Image.fromarray(np.clip(m, 0, 255).astype(np.uint8), "L")
    big.thumbnail((1400, 1400), Image.LANCZOS)
    m2 = np.asarray(big).astype(np.float32)
    render(m2, (255, 255, 255), os.path.join(OUT, slug + "-white.png"))
    render(m2, (5, 9, 54), os.path.join(OUT, slug + "-navy.png"))

json.dump(report, open(os.path.join(OUT, "report.json"), "w"), indent=2)
for r in report:
    print(r)
