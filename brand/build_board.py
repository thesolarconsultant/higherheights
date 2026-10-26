# -*- coding: utf-8 -*-
"""Build the brand board HTML (self-contained, SVGs inlined, screenshots embedded)."""
import os, re, shutil, base64

HERE = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(HERE, "svg")
QA = os.path.join(HERE, "..", "qa")

NAVY, CREAM, GOLD = "#0B1A26", "#F4EFE6", "#C9AE7C"


def svg(name, width=None, cls=""):
    s = open(os.path.join(SVG, name), encoding="utf-8").read()
    s = re.sub(r'\swidth="[^"]*"\s*height="[^"]*"', "", s, count=1)
    s = s.replace("<svg ", f'<svg class="{cls}" ', 1)
    if width:
        s = s.replace("<svg ", f'<svg style="width:{width}" ', 1)
    return s


def png(path):
    b = open(path, "rb").read()
    return "data:image/png;base64," + base64.b64encode(b).decode()


OLD = os.path.join(HERE, "..", "higher-heights", "raw", "Logo", "HigherHeights_Logo_Dark.png")
shot_hero = png(os.path.join(QA, "v2-hero.png"))
shot_studio = png(os.path.join(QA, "v2-studio.png"))
shot_contact = png(os.path.join(QA, "v2-contact-el.png"))
old_logo = "data:image/png;base64," + base64.b64encode(open(OLD, "rb").read()).decode()

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Higher Heights — Identity</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
  :root{{
    --navy:{NAVY}; --cream:{CREAM}; --gold:{GOLD};
    --line:rgba(201,174,124,.22); --line-soft:rgba(244,239,230,.12);
    --muted:rgba(244,239,230,.62); --muted-2:rgba(244,239,230,.42);
    --serif:"Instrument Serif",Georgia,serif;
    --sans:"Instrument Sans",-apple-system,"Segoe UI",sans-serif;
  }}
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  body{{ background:var(--navy); color:var(--cream); font-family:var(--sans);
         font-size:15px; line-height:1.62; -webkit-font-smoothing:antialiased; }}
  .wrap{{ max-width:1180px; margin:0 auto; padding:0 clamp(20px,4vw,56px); }}
  .micro{{ font-size:10px; font-weight:500; letter-spacing:.20em; text-transform:uppercase; color:var(--gold); }}
  .micro--dim{{ color:var(--muted-2); }}
  h1,h2,h3{{ font-family:var(--serif); font-weight:400; letter-spacing:-.022em; line-height:1.02; }}
  h1{{ font-size:clamp(46px,7.4vw,88px); line-height:.92; }}
  h2{{ font-size:clamp(30px,4vw,50px); }}
  h3{{ font-size:clamp(21px,2.2vw,27px); }}
  p{{ color:var(--muted); max-width:62ch; }}
  p + p{{ margin-top:.9em; }}
  em{{ font-style:italic; }}
  strong{{ color:var(--cream); font-weight:500; }}
  section{{ padding:clamp(48px,7vw,104px) 0; border-top:1px solid var(--line-soft); }}
  .head{{ display:flex; align-items:baseline; gap:18px; margin-bottom:clamp(26px,3vw,44px); }}
  .num{{ font-size:10px; letter-spacing:.18em; font-weight:500; color:var(--gold); }}
  .rule{{ width:clamp(24px,4vw,64px); height:1px; background:var(--gold); opacity:.5; transform:translateY(-3px); }}
  .hero{{ padding-block:clamp(54px,9vw,120px) clamp(40px,6vw,72px); }}
  .hero__meta{{ display:flex; justify-content:space-between; gap:24px; flex-wrap:wrap;
                border-bottom:1px solid var(--line-soft); padding-bottom:18px; margin-bottom:clamp(36px,5vw,64px); }}
  .hero__title{{ display:flex; flex-direction:column; gap:clamp(20px,3vw,32px); }}
  .hero__lede{{ font-size:clamp(15px,1.35vw,18px); max-width:52ch; }}
  .grid2{{ display:grid; grid-template-columns:1fr 1fr; gap:clamp(24px,4vw,56px); align-items:start; }}
  .grid3{{ display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(18px,2.4vw,34px); }}
  .panel{{ border:1px solid var(--line-soft); padding:clamp(22px,3vw,38px); }}
  .panel--cream{{ background:var(--cream); color:var(--navy); border-color:rgba(11,26,38,.12); }}
  .panel--cream p{{ color:rgba(11,26,38,.68); }}
  .panel--cream .micro{{ color:rgba(11,26,38,.5); }}
  .panel__foot{{ margin-top:22px; padding-top:16px; border-top:1px solid var(--line-soft);
                 display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; }}
  .panel--cream .panel__foot{{ border-color:rgba(11,26,38,.14); }}
  .old{{ border:1px solid var(--line-soft); background:var(--cream); padding:clamp(26px,4vw,54px); display:grid; place-items:center; }}
  .old img{{ width:min(100%,520px); display:block; }}
  ul{{ list-style:none; display:flex; flex-direction:column; gap:14px; }}
  li{{ display:grid; grid-template-columns:14px 1fr; gap:14px; color:var(--muted); align-items:start; }}
  li b{{ color:var(--cream); font-weight:500; }}
  .dot{{ display:block; width:10px; height:1px; background:var(--gold); margin-top:.78em; }}
  .specimen{{ font-size:clamp(28px,4.6vw,64px); line-height:1.06; letter-spacing:-.02em; }}
  .specimen--sans{{ font-family:var(--sans); font-weight:400; letter-spacing:-.032em; }}
  .type-table{{ width:100%; border-collapse:collapse; margin-top:8px; }}
  .type-table td{{ padding:13px 0; border-top:1px solid var(--line-soft); vertical-align:top; font-size:13.5px; }}
  .type-table td:first-child{{ width:30%; color:var(--cream); font-weight:500; }}
  .type-table td:nth-child(2){{ width:27%; color:var(--muted); }}
  .type-table td:last-child{{ color:var(--muted-2); }}
  .shot{{ border:1px solid var(--line-soft); overflow:hidden; }}
  .shot img{{ display:block; width:100%; }}
  .cap{{ margin-top:12px; font-size:11.5px; letter-spacing:.06em; color:var(--muted-2); }}
  .files{{ display:grid; grid-template-columns:repeat(5,1fr); gap:1px; background:var(--line-soft); }}
  .file{{ background:var(--navy); padding:16px 18px; font-size:12.5px; word-break:break-word; }}
  .file span{{ display:block; color:var(--muted-2); font-size:11px; margin-top:3px; }}
  .kit{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:clamp(16px,2.4vw,30px); align-items:center; }}
  .swatch{{ height:74px; border:1px solid rgba(244,239,230,.26); }}
  .foot{{ padding-block:40px 64px; border-top:1px solid var(--line-soft); }}
  @media (max-width:820px){{
    .grid2,.grid3{{ grid-template-columns:1fr; }}
    .files{{ grid-template-columns:repeat(2,1fr); }}
  }}
</style>
</head>
<body>

<div class="wrap hero">
  <div class="hero__meta">
    <span class="micro">Higher Heights — Identity</span>
    <span class="micro micro--dim">Draft 01 · October 2026</span>
    <span class="micro micro--dim">Film · Aerial · Photography</span>
  </div>
  <div class="hero__title">
    {svg("a-wordmark-cream.svg", width="min(100%,760px)")}
    <p class="hero__lede">A new mark, a new wordmark, and the type system that follows from them.
    The old identity was a mountain zigzag above airy tracked capitals — a stock outdoor-brand
    device, and a wordmark that vanished below 40px. This one is built from one idea that the
    studio already owns: <strong>altitude</strong>.</p>
  </div>
</div>

<section><div class="wrap">
  <div class="head"><span class="num">01</span><span class="rule"></span><span class="micro">What was wrong</span></div>
  <div class="grid2">
    <div>
      <ul>
        <li><span class="dot"></span><span><b>The mark was a generic mountain.</b> A thin zigzag peak is the default icon for every drone, outdoor and travel brand. It said “outdoors”, not “commercial film”.</span></li>
        <li><span class="dot"></span><span><b>Mark and wordmark had no relationship.</b> A 4px gold line drawing, then 60px capitals — different weights, different rhythm, floating apart.</span></li>
        <li><span class="dot"></span><span><b>The wordmark disappeared at small sizes.</b> Ultra-wide tracking on thin geometric capitals means the name reads as a texture, not a name, in a nav bar or a favicon.</span></li>
        <li><span class="dot"></span><span><b>The gold tagline got lost on light backgrounds.</b> It’s the least legible line in the logo on the one background it’s most often used on.</span></li>
      </ul>
    </div>
    <div class="old"><img src="{old_logo}" alt="The previous Higher Heights logo"></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="num">02</span><span class="rule"></span><span class="micro">The idea</span></div>
  <div class="grid2" style="align-items:center">
    <div>
      <h2>One line that<br>gains height.</h2>
      <p style="margin-top:22px">A horizon — then the same horizon, stepped up. It reads three ways at once:
      <strong>altitude</strong> (the ground rises), <strong>a cut</strong> (a film edit is a line moving
      forward), and <strong>a measurement</strong> (the tick marks on a lens or an altimeter).</p>
      <p>It survives as a 16px favicon because it is only three rectangles. And it is not decoration
      applied to the page — the site already uses short gold hairlines beside every index number, so the
      mark is native to the layout.</p>
    </div>
    <div class="panel" style="display:grid;place-items:center;min-height:260px">
      {svg("mark-gold.svg", width="min(100%,260px)")}
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="num">03</span><span class="rule"></span><span class="micro">The system — four components</span></div>

  <div class="grid2" style="margin-bottom:clamp(24px,4vw,56px)">
    <div class="panel panel--cream">
      {svg("a-wordmark-navy.svg", width="100%")}
      <div class="panel__foot">
        <span class="micro">01 · Primary wordmark</span><span class="micro">Instrument Serif · opt. −0.010em</span>
      </div>
    </div>
    <div class="panel" style="display:flex;flex-direction:column;justify-content:center;gap:26px">
      <h3>Primary wordmark</h3>
      <p>The name, set in a high-contrast serif at mixed case, tightened optically. This is the identity
      at its largest — hero, end cards, print, email sign-off. No symbol attached: at this quality the
      type <em>is</em> the logo.</p>
      <div class="panel__foot"><span class="micro micro--dim">Min width 120px</span><span class="micro micro--dim">Never letterspace it out</span></div>
    </div>
  </div>

  <div class="grid2" style="margin-bottom:clamp(24px,4vw,56px)">
    <div class="panel" style="display:flex;flex-direction:column;justify-content:center;gap:26px">
      <h3>Mark</h3>
      <p>The step alone. Used where the name is already known: favicon, social avatar, watermarks on
      footage, set stencils. Solid gold on navy, navy on cream — never outlined, never on a photo
      without a scrim.</p>
      <div class="panel__foot"><span class="micro micro--dim">Min size 16px</span><span class="micro micro--dim">Square crop</span></div>
    </div>
    <div class="panel" style="display:flex;align-items:center;justify-content:center;gap:clamp(18px,3vw,42px);min-height:210px">
      {svg("favicon.svg", width="88px")}
      {svg("favicon-cream.svg", width="88px")}
      {svg("mark-gold.svg", width="44px")}
      {svg("mark-gold.svg", width="20px")}
      {svg("mark-gold.svg", width="16px")}
    </div>
  </div>

  <div class="grid2">
    <div class="panel panel--cream" style="display:flex;flex-direction:column;justify-content:center;gap:34px;min-height:220px">
      {svg("b-signature-h-cream.svg", width="min(100%,340px)")}
      <div class="panel__foot">
        <span class="micro">02 · Signature</span><span class="micro">Nav · letterhead · email</span>
      </div>
    </div>
    <div class="panel" style="display:flex;flex-direction:column;justify-content:center;gap:26px">
      <h3>Signature</h3>
      <p>Mark plus the name in tracked capitals — the version that stays legible at 22px in a nav bar.
      This is what the site header, invoices and email footers use.</p>
      <div class="panel__foot"><span class="micro micro--dim">Mark height = cap height</span><span class="micro micro--dim">Gap = 0.7 × cap</span></div>
    </div>
  </div>

  <div class="grid2" style="margin-top:clamp(24px,4vw,56px)">
    <div class="panel" style="display:grid;place-items:center;padding:clamp(26px,3vw,44px)">
      {svg("c-titlecard-navy.svg", width="min(100%,420px)")}
      <div class="panel__foot" style="width:100%"><span class="micro">03 · Title card</span><span class="micro micro--dim">End card · deck cover</span></div>
    </div>
    <div class="panel panel--cream" style="display:flex;flex-direction:column;justify-content:center;gap:26px">
      <h3>Title card</h3>
      <p>The identity as it appears in the work itself: stacked capitals between two hairlines, tagline
      on the lower rule. Use it as the end card on every film and as the cover of any document — it is
      the one form that looks at home on screen.</p>
      <div class="panel__foot"><span class="micro">Easily the most useful asset for pitching</span></div>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="num">04</span><span class="rule"></span><span class="micro">Type</span></div>
  <div class="grid2" style="margin-bottom:clamp(28px,4vw,52px)">
    <div>
      <span class="micro micro--dim">Display — Instrument Serif 400</span>
      <div class="specimen" style="margin-top:14px">Have something<br><em>worth filming?</em></div>
      <p style="margin-top:18px">One family, roman and italic. The italic is no longer a foreign accent
      dropped into a sans page — it is the same hand, leaning.</p>
    </div>
    <div>
      <span class="micro micro--dim">Text — Instrument Sans 400 / 500</span>
      <div class="specimen specimen--sans" style="margin-top:14px;font-size:clamp(22px,2.6vw,34px)">
      Commercial films, brand stories and aerial cinematography — made for clients who care how it looks.</div>
      <p style="margin-top:18px">Instrument Sans was drawn as the companion to Instrument Serif:
      same proportions, same skeleton. Set body at 400, labels at 500 with wide tracking.</p>
    </div>
  </div>

  <table class="type-table">
    <tr><td>Display / h1 · h2</td><td>Instrument Serif 400</td><td>−0.022em · line-height 1.02</td></tr>
    <tr><td>Statements, quotes</td><td>Instrument Serif Italic 400</td><td>−0.02em</td></tr>
    <tr><td>Body</td><td>Instrument Sans 400</td><td>−0.005em · 1.62</td></tr>
    <tr><td>Labels, nav, meta</td><td>Instrument Sans 500</td><td>+0.17em · uppercase · 10px</td></tr>
    <tr><td>Wordmark</td><td>Instrument Serif 400</td><td>−0.010em · outlined</td></tr>
  </table>

  <div class="grid2" style="margin-top:clamp(30px,4vw,52px)">
    <div>
      <h3 style="margin-bottom:14px">Why the logo forced this</h3>
      <p>The wordmark is a serif, so the display face had to become that serif — otherwise the logo and
      the headline are two different voices on the same screen. Once the display is a serif, the body
      wants a sans that belongs to it, and Geist does not: it is a tech grotesque, the face of dashboards
      and dev tools, with a flat, closed rhythm that fights a high-contrast serif.</p>
      <p><strong>Geist and Geist Mono are gone.</strong> The mono was doing the job of “technical
      label” — small tracked capitals — which Instrument Sans 500 does in the same voice as the rest of
      the page. Two families instead of three, and they were designed together.</p>
    </div>
    <div>
      <h3 style="margin-bottom:14px">Palette — unchanged, re-weighted</h3>
      <div class="kit" style="margin-bottom:16px">
        <div><div class="swatch" style="background:{NAVY}"></div><div class="micro" style="margin-top:9px">Navy</div><div class="micro micro--dim">#0B1A26</div></div>
        <div><div class="swatch" style="background:{CREAM}"></div><div class="micro" style="margin-top:9px">Cream</div><div class="micro micro--dim">#F4EFE6</div></div>
        <div><div class="swatch" style="background:{GOLD}"></div><div class="micro" style="margin-top:9px">Gold</div><div class="micro micro--dim">#C9AE7C</div></div>
      </div>
      <p>The three colours were sampled from the existing logo and stay. Gold is now strictly an accent:
      rules, the mark, index numbers. It never carries body text again — that was the old logo’s
      legibility problem, repeated at page scale.</p>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="num">05</span><span class="rule"></span><span class="micro">Applied — live site, same copy, new identity</span></div>
  <div class="grid2">
    <div><div class="shot"><img src="{shot_hero}" alt="Hero with the new wordmark and serif display"></div>
      <div class="cap">Hero — serif display at 138px, signature in the nav</div></div>
    <div><div class="shot"><img src="{shot_studio}" alt="Studio section set in Instrument Serif and Instrument Sans"></div>
      <div class="cap">Studio — headline and body from one superfamily</div></div>
  </div>
  <div style="margin-top:clamp(24px,4vw,44px)"><div class="shot"><img src="{shot_contact}" alt="Contact section"></div>
    <div class="cap">Contact — roman and italic of the same face</div></div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="num">06</span><span class="rule"></span><span class="micro">Files</span></div>
  <div class="files">
    <div class="file">a-wordmark-cream.svg<span>Primary · on navy</span></div>
    <div class="file">a-wordmark-navy.svg<span>Primary · on cream</span></div>
    <div class="file">a-stacked-cream.svg<span>Stacked · square spaces</span></div>
    <div class="file">mark-tight-gold.svg<span>Mark · navy</span></div>
    <div class="file">mark-tight-navy.svg<span>Mark · cream</span></div>
    <div class="file">favicon.svg<span>64px app icon</span></div>
    <div class="file">b-signature-h-cream.svg<span>Signature · horizontal</span></div>
    <div class="file">b-signature-stack-navy.svg<span>Signature · stacked</span></div>
    <div class="file">c-titlecard-navy.svg<span>Title card · end card</span></div>
    <div class="file">c-titlecard-cream.svg<span>Title card · light</span></div>
  </div>
  <p style="margin-top:26px">All text is outlined to paths, so the files do not depend on a font being
  installed. Instrument Serif and Instrument Sans are OFL-licensed, which permits outlining for a
  wordmark. <strong>Still to do:</strong> a proper 1200×630 share image built from the title card, a
  16/32/180px raster fallback set for older browsers, and the same end card in 16:9 and 9:16 for the
  film exports.</p>
</div></section>

<div class="wrap foot">
  <span class="micro micro--dim">Higher Heights · Identity draft 01 · built from the brand’s own assets</span>
</div>

</body>
</html>
"""

out = os.path.join(HERE, "Higher Heights — Identity.html")
open(out, "w", encoding="utf-8").write(HTML)
print("wrote", out, len(HTML), "bytes")
