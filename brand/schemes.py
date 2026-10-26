# -*- coding: utf-8 -*-
"""Recolour the HH icon set for each candidate scheme, then build the board."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "schemes")
os.makedirs(OUT, exist_ok=True)

SRC = {
    "wordmark": os.path.join(ROOT, "logos2", "wordmark-gold.svg"),   # HIGHER HEIGHTS / FILMS
    "caps":     os.path.join(ROOT, "logos", "wm-caps-gold.svg"),      # nav lockup
    "hh":       os.path.join(ROOT, "logos2", "hh-flat-gold.svg"),     # the monogram
}

SCHEMES = [
    dict(id="ink",      name="Ink & Bone",
         bg="#0A0A0B", bg2="#141416", ink="#F7F4EF", dim="rgba(247,244,239,.58)",
         accent="#E78223", line="rgba(247,244,239,.16)", light=False,
         note="Near-black, bone white, ember. The film carries every colour."),
    dict(id="midnight", name="Midnight Cinema",
         bg="#050936", bg2="#121D42", ink="#FFFFFF", dim="rgba(255,255,255,.62)",
         accent="#E78223", line="rgba(255,255,255,.18)", light=False,
         note="His theme 01, pure white type. Navy reads as a brand, not a ground."),
    dict(id="deepsea",  name="Deep Sea & Brass",
         bg="#0B1620", bg2="#13212E", ink="#F2EFE9", dim="rgba(242,239,233,.60)",
         accent="#B98A4B", line="rgba(185,138,75,.30)", light=False,
         note="Ink blue-black with brass. Maritime without saying navy."),
    dict(id="bone",     name="Bone & Ink",
         bg="#F4F1EA", bg2="#E9E5DC", ink="#111113", dim="rgba(17,17,19,.62)",
         accent="#C2410C", line="rgba(17,17,19,.16)", light=True,
         note="Light. A gallery, not a cinema. Almost nobody in film does this."),
    dict(id="carbon",   name="Carbon & Steel",
         bg="#121214", bg2="#1C1C20", ink="#E8EAED", dim="rgba(232,234,237,.55)",
         accent="#9AA3AE", line="rgba(232,234,237,.14)", light=False,
         note="No colour at all. The most automotive of the five."),
]


def recolour(src, colour, dst):
    s = open(src, encoding="utf-8").read()
    s = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{colour}"', s)
    open(dst, "w", encoding="utf-8").write(s)


for sc in SCHEMES:
    for key, path in SRC.items():
        recolour(path, sc["ink"], os.path.join(OUT, f"{sc['id']}-{key}.svg"))
    # the monogram also in the accent, for the "icon" treatment
    recolour(SRC["hh"], sc["accent"], os.path.join(OUT, f"{sc['id']}-hh-accent.svg"))

json.dump(SCHEMES, open(os.path.join(OUT, "schemes.json"), "w"), indent=2)
print(f"wrote {len(SCHEMES)} schemes x 4 assets -> {OUT}")
for sc in SCHEMES:
    print(f"  {sc['id']:9s} {sc['bg']} / {sc['ink']} / {sc['accent']}  {sc['name']}")
