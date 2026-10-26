# -*- coding: utf-8 -*-
"""Build the colour-direction board: each scheme as a real hero, with his icon set."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEMES = json.load(open(os.path.join(ROOT, "schemes", "schemes.json")))
SHOT = "../site-v8/assets/img/poster-roller.jpg"
SHOT2 = "../site-v8/assets/img/poster-highland.jpg"

CARDS = []
for i, s in enumerate(SCHEMES):
    sid = s["id"]
    lightcls = " is-light" if s["light"] else ""
    CARDS.append(f"""
<article class="dir{lightcls}" style="--bg:{s['bg']};--bg2:{s['bg2']};--ink:{s['ink']};
     --dim:{s['dim']};--accent:{s['accent']};--line:{s['line']}">
  <div class="dir__tag">
    <span class="k">{chr(65+i)}</span>
    <span class="n">{s['name']}</span>
    <span class="hex">{s['bg']} · {s['ink']} · {s['accent']}</span>
  </div>

  <!-- the hero, as it would actually run -->
  <div class="hero">
    <img class="hero__plate" src="{SHOT}" alt="">
    <div class="hero__scrim"></div>
    <div class="hero__nav">
      <img class="hero__wm" src="schemes/{sid}-caps.svg" alt="">
      <div class="hero__links"><span>Work</span><span>Who</span><span>Contact</span></div>
    </div>
    <div class="hero__foot">
      <div>
        <h3 class="hero__title">A Rolls, a winter,<br>and its <em>owner.</em></h3>
        <div class="hero__credit">Spens Motors · 2025</div>
      </div>
      <div class="hero__aside">
        <span class="hero__k">Client</span>
        <span class="hero__v">Spens Motors</span>
      </div>
    </div>
    <div class="strip">
      <span class="strip__i is-live"><b>Heritage</b><i>Spens Motors</i></span>
      <span class="strip__i"><b>Styled By You</b><i>NOBL</i></span>
      <span class="strip__i"><b>In the Case</b><i>WatchTrader &amp; Co</i></span>
      <span class="strip__i"><b>RM 69</b><i>Richard Mille</i></span>
    </div>
  </div>

  <!-- his marks, in this scheme -->
  <div class="icons">
    <div class="icons__row">
      <div class="ico"><div class="ico__box"><img src="schemes/{sid}-hh.svg" style="height:46px"></div><span>Monogram</span></div>
      <div class="ico"><div class="ico__box"><img src="schemes/{sid}-hh-accent.svg" style="height:46px"></div><span>Accent</span></div>
      <div class="ico"><div class="ico__box tile"><img src="schemes/{sid}-hh.svg" style="height:30px"></div><span>App icon</span></div>
      <div class="ico"><div class="ico__box"><img src="../brand/logos2/hh-3d-256.png" style="height:46px"></div><span>3D</span></div>
      <div class="ico sizes"><div class="ico__box">
        <img src="schemes/{sid}-hh.svg" style="height:26px">
        <img src="schemes/{sid}-hh.svg" style="height:18px">
        <img src="schemes/{sid}-hh.svg" style="height:13px">
      </div><span>Small sizes</span></div>
    </div>
    <div class="icons__wm">
      <img src="schemes/{sid}-wordmark.svg" alt="">
    </div>
    <p class="icons__note">{s['note']}</p>
  </div>
</article>""")

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Higher Heights Films — colour directions</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#1A1A1D;color:#EDEDF0;font:15px/1.6 "Instrument Sans",system-ui,sans-serif;
        -webkit-font-smoothing:antialiased;padding:0 clamp(16px,2.6vw,38px) 70px}}
  img{{display:block;max-width:100%}}
  header.page{{padding:52px 0 30px;border-bottom:1px solid rgba(255,255,255,.14)}}
  .eyebrow{{font-size:10px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:#E78223}}
  h1{{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:clamp(32px,4.4vw,54px);
      line-height:1;letter-spacing:-.02em;margin:16px 0 14px}}
  header.page p{{color:rgba(237,237,240,.68);max-width:72ch}}

  .dir{{margin-top:40px;border:1px solid rgba(255,255,255,.12);overflow:hidden;background:var(--bg)}}
  .dir__tag{{display:flex;align-items:baseline;gap:16px;padding:16px 20px;background:var(--bg2);
            border-bottom:1px solid var(--line);flex-wrap:wrap}}
  .dir__tag .k{{font-family:"Bodoni Moda",serif;font-size:22px;color:var(--accent);line-height:1}}
  .dir__tag .n{{font-size:13.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}}
  .dir__tag .hex{{margin-left:auto;font-size:11px;letter-spacing:.1em;color:var(--dim)}}

  /* ── hero mock ── */
  .hero{{position:relative;height:420px;overflow:hidden;background:var(--bg)}}
  .hero__plate{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
  .hero__scrim{{position:absolute;inset:0;
    background:linear-gradient(to top,var(--bg) 2%,color-mix(in srgb,var(--bg) 55%,transparent) 32%,transparent 66%),
               linear-gradient(to bottom,color-mix(in srgb,var(--bg) 75%,transparent),transparent 26%)}}
  .hero__nav{{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;
             align-items:center;padding:18px 22px;z-index:2}}
  .hero__wm{{height:12px;width:auto}}
  .hero__links{{display:flex;gap:20px;font-size:9.5px;font-weight:500;letter-spacing:.2em;
               text-transform:uppercase;color:var(--ink);opacity:.9}}
  .hero__foot{{position:absolute;left:22px;right:22px;bottom:74px;z-index:2;display:flex;
              justify-content:space-between;align-items:flex-end;gap:20px}}
  .hero__title{{font-family:"Bodoni Moda",Georgia,serif;font-weight:400;font-size:40px;line-height:.98;
               letter-spacing:-.018em;color:var(--ink)}}
  .hero__title em{{font-style:italic}}
  .hero__credit{{margin-top:12px;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim)}}
  .hero__aside{{text-align:right}}
  .hero__k{{display:block;font-size:9px;letter-spacing:.22em;text-transform:uppercase;color:var(--dim)}}
  .hero__v{{display:block;margin-top:5px;font-size:13px;color:var(--ink)}}
  .strip{{position:absolute;left:0;right:0;bottom:0;z-index:3;display:flex;
         border-top:1px solid var(--line);background:color-mix(in srgb,var(--bg) 55%,transparent);
         backdrop-filter:blur(8px)}}
  .strip__i{{flex:1;position:relative;padding:13px 14px;border-right:1px solid var(--line)}}
  .strip__i:last-child{{border-right:0}}
  .strip__i i{{display:block;font-style:normal;font-size:9px;letter-spacing:.15em;text-transform:uppercase;color:var(--dim);margin-top:4px}}
  .strip__i b{{display:block;font-size:11.5px;font-weight:400;color:var(--ink);opacity:.85}}
  .strip__i.is-live::before{{content:"";position:absolute;left:0;top:-1px;height:1px;width:100%;background:var(--accent)}}
  .strip__i.is-live b{{opacity:1}}

  /* ── icon set ── */
  .icons{{padding:26px 22px 28px;border-top:1px solid var(--line)}}
  .icons__row{{display:flex;gap:14px;flex-wrap:wrap;align-items:stretch}}
  .ico{{display:flex;flex-direction:column;gap:9px;align-items:center}}
  .ico__box{{display:flex;align-items:center;justify-content:center;gap:12px;min-width:104px;height:84px;
            padding:0 16px;border:1px solid var(--line);background:var(--bg2)}}
  .ico__box.tile{{background:var(--accent)}}
  .dir.is-light .ico__box.tile{{background:var(--ink)}}
  .dir.is-light .ico__box.tile img{{filter:invert(1) brightness(3)}}
  .ico span{{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}}
  .ico.sizes .ico__box{{min-width:150px}}
  .icons__wm{{margin-top:22px;padding:22px 0 0;border-top:1px solid var(--line)}}
  .icons__wm img{{height:38px;width:auto}}
  .icons__note{{margin-top:16px;font-size:13.5px;color:var(--dim);max-width:68ch}}
</style></head><body>

<header class="page">
  <div class="eyebrow">Higher Heights Films</div>
  <h1>Five colour directions, his marks in each</h1>
  <p>The same hero, the same film, the same type. Only the colour changes — and the monogram,
  wordmark and app icon are shown inside each one, at the sizes they actually get used.
  Pick a letter and I'll build it out.</p>
</header>

{''.join(CARDS)}

</body></html>"""

p = os.path.join(ROOT, "directions.html")
open(p, "w", encoding="utf-8").write(HTML)
print("wrote", p, len(HTML), "bytes")
