# -*- coding: utf-8 -*-
"""Optically balance the client logos, then proof them on the brand field."""
import os, json, math
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(ROOT, "clients")
rep = json.load(open(os.path.join(C, "report.json")))
rep = [r for r in rep if "error" not in r]

# each logo should carry the same amount of ink on screen, not the same height.
# ink_area = w * h * coverage ; with h = w/aspect  ->  w = sqrt(K * aspect / coverage)
K = 4200.0
for r in rep:
    w = math.sqrt(K * r["aspect"] / max(r["coverage"], 0.05))
    h = w / r["aspect"]
    # nothing may tower over or vanish beside its neighbours
    if h > 56:
        h = 56; w = h * r["aspect"]
    if h < 20:
        h = 20; w = h * r["aspect"]
    if w > 190:
        w = 190; h = w / r["aspect"]
    r["dw"], r["dh"] = round(w), round(h)

json.dump(rep, open(os.path.join(C, "sized.json"), "w"), indent=2)
for r in rep:
    print(f"{r['slug']:12s} aspect {r['aspect']:5.2f}  cover {r['coverage']:.3f}  ->  {r['dw']:3d} x {r['dh']:3d}")

# ── proof sheet on midnight ────────────────────────────────────────────────
PAD, COLS = 46, 4
cellw = 190 + PAD * 2
cellh = 56 + PAD * 2
rows = (len(rep) + COLS - 1) // COLS
sheet = Image.new("RGB", (cellw * COLS, cellh * rows), (8, 8, 10))
for i, r in enumerate(rep):
    im = Image.open(os.path.join(C, r["slug"] + "-white.png")).convert("RGBA")
    im = im.resize((r["dw"], r["dh"]), Image.LANCZOS)
    cx = (i % COLS) * cellw + (cellw - r["dw"]) // 2
    cy = (i // COLS) * cellh + (cellh - r["dh"]) // 2
    sheet.paste(im, (cx, cy), im)
sheet.save(os.path.join(ROOT, "clients-proof.jpg"), quality=90)
print("proof", sheet.size)
