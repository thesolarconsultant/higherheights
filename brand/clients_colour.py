# -*- coding: utf-8 -*-
"""Pull each client's real brand colour, so hover can restore it."""
import numpy as np, json, os
from PIL import Image

SRC = r"C:\Users\Jordan\AppData\Roaming\Hermes\composer-images"
ROOT = os.path.dirname(os.path.abspath(__file__))
rep = json.load(open(os.path.join(ROOT, "clients", "sized.json")))

FILES = {
    "whoop": "whoop-logo-vector_9f998a.png",
    "aduna": "aduna-logo-sunset-rgb-900px-w-72ppi_cdbe0e.png",
    "cleanco": "C0105.00_00_16_13.Still001_b5570f.png",
    "watchtrader": "Screenshot_2026-10-22_at_10.22.36_ebe7fe.png",
    "real": "The_REAL_Drinks_Co._Logo_Wordmark_Horizontal_1_1_348c34.png",
    "crowdcube": "Cc_logo-RGB-orange_1b41eb.png",
    "tecrec": "TR_Wide_RGB_HR_8b6c4e.png",
    "hybrid": "Hybrid_Combination_Master_Horizontal_RGB300_49e936.png",
    "everyones": "EE_Logo_No_Slogan_b7ac5a.png",
    "dayswork": "Dayswork_png_black_writing_373a86.png",
    "jimjam": "JIM_JAM_THE_LABEL_LOGO_863e6b.jpg",
    "piemash": "Untitled_design_5_1f6bb9.png",
    "tj": "Screenshot_2026-10-22_at_10.21.55_6e32a3.png",
    "be": "PHOTO-2024-09-08-05-39-35_2_599118.jpg",
}

for r in rep:
    a = np.asarray(Image.open(os.path.join(SRC, FILES[r["slug"]])).convert("RGBA")).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3]
    ink = (255 - rgb.min(2) > 60) & (al > 120)
    px = rgb[ink]
    if not len(px):
        r["brand"] = "#FFFFFF"
        r["chromatic"] = False
        continue
    sat = px.max(1) - px.min(1)
    col = px[sat > 40]
    chromatic = len(col) > len(px) * 0.12
    chosen = np.median(col, 0) if chromatic else np.median(px, 0)
    # lift it off the dark field so it still reads when restored
    if chosen.max() < 110:
        chosen = np.clip(chosen * (130.0 / max(chosen.max(), 1)), 0, 255)
    r["brand"] = "#%02X%02X%02X" % tuple(int(c) for c in chosen)
    r["chromatic"] = bool(chromatic)

json.dump(rep, open(os.path.join(ROOT, "clients", "sized.json"), "w"), indent=2)
for r in rep:
    print(f"{r['slug']:12s} {r['brand']}  chromatic={r['chromatic']}")
