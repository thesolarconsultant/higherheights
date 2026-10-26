# -*- coding: utf-8 -*-
"""Build a reference board from the captured studio homepages."""
import os, json, base64

B = os.path.dirname(os.path.abspath(__file__))
MID, IVY, SAGE, ORANGE = "#121D42", "#FAF1D0", "#E5E0AF", "#E78223"


def img(path, caption):
    p = os.path.join(B, path)
    if not os.path.exists(p):
        return ""
    b64 = base64.b64encode(open(p, "rb").read()).decode()
    return (f'<figure><img src="data:image/png;base64,{b64}" alt="">'
            f'<figcaption>{caption}</figcaption></figure>')


GROUPS = [
    ("The film is the interface", [
        ("../refs/caviar.png", "<b>Caviar</b> — one letterboxed film, caption underneath, everything else tiny. 23 films on the page, no scrolling sections."),
        ("../refs2/blink.png", "<b>Blink</b> — full-bleed film with the title card set over it. The work names itself."),
        ("../refs/iconoclast.png", "<b>Iconoclast</b> — a numbered filmstrip (1–10) along the bottom edge. You step through films like frames."),
    ]),
    ("The index instead of the grid", [
        ("../refs2/corner-shop.png", "<b>The Corner Shop</b> — nothing but a list of directors' names in red on white. No images, no copy. Perfect confidence."),
        ("../refs/biscuit.png", "<b>Biscuit</b> — a face on film behind a directory of the roster. People are the product."),
        ("../refs2/reset.png", "<b>Reset</b> — one film, arrows, and a five-frame strip of other films with director names."),
    ]),
    ("Empty on purpose", [
        ("../refs/mjz.png", "<b>MJZ</b> — a logo and three words: DIRECTORS, CONTACT, SALES. Nothing else."),
        ("../refs2/academy-films.png", "<b>Academy Films</b> — screen split in two, two films playing edge to edge, nav reduced to eight small words."),
    ]),
    ("The competition", [
        ("../refs/ocean-air.png", "<b>Ocean Air Media</b> — clean, but a brochure: full-bleed still, tiny nav, no motion."),
        ("../refs/yacht-media-crew.png", "<b>Yacht Media Crew</b> — big italic serif, orange button, stock layout. This is who he's being compared against."),
    ]),
]

rows = []
for title, items in GROUPS:
    cards = "".join(img(p, c) for p, c in items)
    rows.append(f'<section><h2>{title}</h2><div class="grid">{cards}</div></section>')

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reference — how film companies present themselves</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500&family=Bodoni+Moda:opsz,wght@6..96,400&display=swap" rel="stylesheet">
<style>
  :root{{ --mid:{MID}; --ivy:{IVY}; --sage:{SAGE}; --orange:{ORANGE}; }}
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  body{{ background:var(--mid); color:var(--ivy); font-family:"Instrument Sans",system-ui,sans-serif;
         font-size:15px; line-height:1.6; padding:0 clamp(20px,4vw,56px) 80px; -webkit-font-smoothing:antialiased; }}
  header{{ padding:56px 0 34px; border-bottom:1px solid rgba(229,224,175,.22); }}
  .micro{{ font-size:10px; font-weight:500; letter-spacing:.2em; text-transform:uppercase; color:var(--sage); }}
  h1{{ font-family:"Bodoni Moda",Georgia,serif; font-weight:400; font-size:clamp(34px,4.6vw,58px);
       line-height:1; letter-spacing:-.02em; margin:18px 0 16px; }}
  h2{{ font-family:"Bodoni Moda",Georgia,serif; font-weight:400; font-size:clamp(22px,2.4vw,30px);
       letter-spacing:-.015em; margin-bottom:18px; }}
  p{{ color:rgba(250,241,208,.72); max-width:64ch; }}
  section{{ padding:44px 0; border-bottom:1px solid rgba(229,224,175,.14); }}
  .grid{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:22px; }}
  figure{{ margin:0; }}
  figure img{{ width:100%; display:block; border:1px solid rgba(229,224,175,.16); }}
  figcaption{{ font-size:12.5px; line-height:1.5; color:rgba(250,241,208,.62); margin-top:9px; }}
  figcaption b{{ color:var(--ivy); font-weight:500; }}
  .lead{{ font-size:17px; color:rgba(250,241,208,.85); max-width:70ch; }}
  .rules{{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:26px; margin-top:8px; }}
  .rule{{ border-top:2px solid var(--orange); padding-top:14px; }}
  .rule b{{ display:block; color:var(--ivy); font-weight:500; margin-bottom:6px; }}
  .rule span{{ font-size:13.5px; color:rgba(250,241,208,.66); }}
</style></head><body>

<header>
  <div class="micro">Higher Heights Films — reference study</div>
  <h1>How the best film companies present themselves</h1>
  <p class="lead">Eleven homepages from the top of the commercial film industry, captured live. The pattern is
  consistent and it is the opposite of what our site does: they never explain the work, they only show it.</p>
</header>

{''.join(rows)}

<section>
  <h2>What every one of them does — and we don't</h2>
  <div class="rules">
    <div class="rule"><b>No paragraphs</b><span>Almost no body copy anywhere. Names, titles, films. A booker does not read.</span></div>
    <div class="rule"><b>Film full-bleed</b><span>The player is the page, edge to edge. Not a poster in a card with rounded corners.</span></div>
    <div class="rule"><b>Type on the image</b><span>Title, client and director are set over the film — not in a caption under a grid.</span></div>
    <div class="rule"><b>An index, not a grid</b><span>A list of names, a numbered filmstrip, five frames. Something you move through.</span></div>
    <div class="rule"><b>Two type sizes</b><span>Enormous display, or 10px caps. Nothing in the middle — no 16px marketing sentences.</span></div>
    <div class="rule"><b>Colour from the footage</b><span>Black, white, one accent. The brand does not compete with the film for attention.</span></div>
  </div>
</section>

<section>
  <h2>Why ours reads as stiff</h2>
  <p>Our page is organised like a brochure: a statement of intent, then a section for each service, a grid of
  eight films behind a click, an "aerial unit" explainer, a process list. That is the structure of a company
  describing itself. Every reference above does the opposite — it hands you the work and says nothing.</p>
  <p style="margin-top:14px">Two more specific things. There is no sound and no motion in the grid: the films sit still
  as thumbnails until clicked. And there is no person on the page — for a company whose differentiator is a
  presenter, the founder appears once, in a section called Studio, below the fold.</p>
</section>

</body></html>
"""
open(os.path.join(B, "references.html"), "w", encoding="utf-8").write(HTML)
print("wrote references.html", len(HTML), "bytes")
