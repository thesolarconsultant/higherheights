# -*- coding: utf-8 -*-
"""Pass A — two library mechanics, restyled.

softfocus : images rack into focus out of blur as they arrive, with a
            viewfinder frame that tightens onto them. Camera language.
herotype  : the hero's two lines rise out of their own masks, staggered.

Both ride the site's existing .reveal observer, so nothing new has to watch
the scroll position.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(ROOT, "site-brand", "index.html")
s = open(p, encoding="utf-8").read()
start = len(s)


def sub(old, new, why):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n   " + old[:140])
    s = s.replace(old, new, 1)
    print("  ok ", why)


# ── CSS ───────────────────────────────────────────────────────────────────
sub(".reveal{ opacity:0; transform:translate3d(0,26px,0); transition:opacity .85s var(--ease), transform .85s var(--ease); }\n.reveal.in{ opacity:1; transform:none; }",
""".reveal{ opacity:0; transform:translate3d(0,26px,0); transition:opacity .85s var(--ease), transform .85s var(--ease); }
.reveal.in{ opacity:1; transform:none; }

/* ── Rack focus. Mechanic from Goodwork Library v1.3.0 'softfocus',
      restyled: no glass, no rounded corners, hairline frame only. ── */
.rack{ position:relative; overflow:hidden; }
.rack img{
  filter:blur(14px); transform:scale(1.06); opacity:.55;
  transition:filter 1.15s var(--ease), transform 1.4s var(--ease), opacity .9s var(--ease);
  will-change:filter, transform;
}
.rack.in img{ filter:blur(0); transform:scale(1); opacity:1; }
.rack__vf{ position:absolute; inset:0; pointer-events:none; z-index:2; opacity:0;
  transition:opacity .5s var(--ease) .15s; }
.rack.in .rack__vf{ opacity:1; }
.rack__vf i{
  position:absolute; width:17px; height:17px;
  border:1px solid var(--gold); opacity:.72;
  transition:inset .95s var(--ease), opacity .6s var(--ease) .9s;
}
.rack__vf i:nth-child(1){ inset:-10px auto auto -10px; border-right:0; border-bottom:0; }
.rack__vf i:nth-child(2){ inset:-10px -10px auto auto; border-left:0; border-bottom:0; }
.rack__vf i:nth-child(3){ inset:auto auto -10px -10px; border-right:0; border-top:0; }
.rack__vf i:nth-child(4){ inset:auto -10px -10px auto; border-left:0; border-top:0; }
.rack.in .rack__vf i:nth-child(1){ inset:11px auto auto 11px; opacity:0; }
.rack.in .rack__vf i:nth-child(2){ inset:11px 11px auto auto; opacity:0; }
.rack.in .rack__vf i:nth-child(3){ inset:auto auto 11px 11px; opacity:0; }
.rack.in .rack__vf i:nth-child(4){ inset:auto 11px 11px auto; opacity:0; }

/* ── Masked line rise. Mechanic from 'herotype', restyled. ── */
.rise{ display:block; overflow:hidden; }
.rise > span{
  display:block; transform:translateY(105%);
  transition:transform 1.05s cubic-bezier(.16,1,.3,1);
}
.hero__title.is-up .rise:nth-child(1) > span{ transform:none; transition-delay:.08s; }
.hero__title.is-up .rise:nth-child(2) > span{ transform:none; transition-delay:.22s; }

@media (prefers-reduced-motion:reduce){
  .rack img{ filter:none; transform:none; opacity:1; transition:none }
  .rack__vf{ display:none }
  .rise > span{ transform:none; transition:none }
}""",
    "rack + rise CSS")

# ── hero title: wrap each line in its own mask ────────────────────────────
sub('<h1 class="hero__title"><em>Higher</em><em>Heights</em></h1>',
    '<h1 class="hero__title"><em class="rise"><span>Higher</span></em>'
    '<em class="rise"><span>Heights</span></em></h1>',
    "hero title masks")

# the h1 uses `em + em` for spacing; masks are block so restate the rhythm
sub("h1.hero__title em + em{ padding-left:.09em; }",
    "h1.hero__title em + em{ padding-left:.09em; }\n"
    "h1.hero__title .rise{ padding-bottom:.04em; }",
    "mask descender room")

# ── wire it all up ────────────────────────────────────────────────────────
sub("  const reveals = $$(\".reveal\");",
"""  /* rack focus on every framed image — mechanic from 'softfocus' */
  document.querySelectorAll(".film__frame, .strip figure, .studio__figure, .studio__bandFrame")
    .forEach(function (el) {
      if (!el.querySelector("img") || el.classList.contains("rack")) return;
      el.classList.add("rack", "reveal");
      const vf = document.createElement("span");
      vf.className = "rack__vf";
      vf.setAttribute("aria-hidden", "true");
      vf.innerHTML = "<i></i><i></i><i></i><i></i>";
      el.appendChild(vf);
    });

  /* the hero lines rise once, on load — mechanic from 'herotype' */
  (function () {
    const t = document.querySelector(".hero__title");
    if (!t) return;
    if (reduced) { t.classList.add("is-up"); return; }
    requestAnimationFrame(function () {
      setTimeout(function () { t.classList.add("is-up"); }, 90);
    });
  })();

  const reveals = $$(\".reveal\");""",
    "wire rack + rise")

open(p, "w", encoding="utf-8").write(s)
print(f"\nwritten: {start} -> {len(s)} bytes  (+{len(s)-start})")
