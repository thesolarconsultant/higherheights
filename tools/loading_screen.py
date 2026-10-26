# -*- coding: utf-8 -*-
"""On-brand loading screen, on every page, on every load.

Requirements taken literally:
  - every load, not once per session (so no sessionStorage flag)
  - the refined monogram, at size
  - on brand: the site's own ground and cream, no spinner, no bounce

Safety matters more than the animation here. A loader that fails to dismiss
hides the entire site, so there are three independent ways out:
  1. window 'load' fires            -> normal path
  2. a CSS animation at 3.5s        -> fires even if JS never runs at all
  3. a JS timeout at 4s             -> belt and braces if 'load' is missed
Whichever lands first wins, and the overlay is removed from the flow after.

It is aria-hidden and inert so it never traps a screen reader or keyboard,
and prefers-reduced-motion gets a plain fade with no movement.
"""
import os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site-brand")

CSS = """
/* ══ Loading screen ═══════════════════════════════════════════════
   Shows on every load. Three independent dismissals so a JS failure
   can never leave the site hidden. ══ */
#hhload{
  position:fixed; inset:0; z-index:9999;
  display:grid; place-items:center;
  background:var(--deep,#070D0B);
  opacity:1; visibility:visible;
  transition:opacity .72s var(--ease,cubic-bezier(.16,1,.3,1)), visibility 0s linear .72s;
  /* fallback: dismiss at 3.5s even with no JS at all */
  animation:hhload-auto 0s linear 3.5s forwards;
}
#hhload.is-done{ opacity:0; visibility:hidden; pointer-events:none; }
@keyframes hhload-auto{ to{ opacity:0; visibility:hidden; pointer-events:none; } }

.hhload__in{ display:flex; flex-direction:column; align-items:center; gap:clamp(1.6rem,3vw,2.4rem); }
.hhload__mark{
  width:clamp(170px,22vw,300px); height:auto; color:var(--cream,#E9E5DB);
  opacity:0; transform:translateY(10px) scale(.985);
  animation:hhload-mark .95s var(--ease,cubic-bezier(.16,1,.3,1)) .06s forwards;
}
.hhload__mark svg,.hhload__mark img{ display:block; width:100%; height:auto; }
@keyframes hhload-mark{ to{ opacity:1; transform:none; } }

/* a hairline that fills -- reads as a film leader, not a spinner */
.hhload__bar{ position:relative; width:clamp(120px,16vw,210px); height:1px;
  background:rgba(233,229,219,.16); overflow:hidden; }
.hhload__bar::after{ content:""; position:absolute; inset:0;
  background:var(--cream,#E9E5DB); transform:scaleX(0); transform-origin:left center;
  animation:hhload-bar 2.6s var(--ease,cubic-bezier(.16,1,.3,1)) forwards; }
@keyframes hhload-bar{ 0%{transform:scaleX(0)} 62%{transform:scaleX(.72)} 100%{transform:scaleX(1)} }

.hhload__word{ font-family:var(--mono,ui-monospace); font-size:var(--fs-micro,.72rem);
  letter-spacing:.22em; text-transform:uppercase; color:rgba(233,229,219,.42); }

@media(prefers-reduced-motion:reduce){
  #hhload{ transition:opacity .2s linear, visibility 0s linear .2s; animation-delay:1.2s; }
  .hhload__mark{ opacity:1; transform:none; animation:none; }
  .hhload__bar::after{ animation:none; transform:scaleX(1); }
}
"""

MARKUP = """<div id="hhload" aria-hidden="true" role="presentation">
  <div class="hhload__in">
    <div class="hhload__mark">{SVG}</div>
    <div class="hhload__bar"></div>
    <div class="hhload__word">Higher Heights</div>
  </div>
</div>
"""

JS = """<script>
/* Loading screen: dismiss on load, with a hard timeout behind it. Runs on
   every page load by design -- no session flag. */
(function () {
  var el = document.getElementById("hhload");
  if (!el) return;
  var gone = false;
  function hide() {
    if (gone) return;
    gone = true;
    el.classList.add("is-done");
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 900);
  }
  if (document.readyState === "complete") setTimeout(hide, 420);
  else window.addEventListener("load", function () { setTimeout(hide, 280); });
  setTimeout(hide, 4000);                 /* never hold the page hostage */
  window.addEventListener("pageshow", function (e) { if (e.persisted) hide(); });
})();
</script>
"""

svg = open(os.path.join(SITE, "assets", "img", "hh-cream.svg"), encoding="utf-8").read()
svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()

n = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(f, encoding="utf-8").read()
    if 'id="hhload"' in s:
        print(f"   {os.path.basename(f)}: already has it"); continue
    s = s.replace("</style>", CSS + "</style>", 1)
    m = re.search(r"<body[^>]*>", s)
    if not m:
        print(f"   no <body> in {os.path.basename(f)}"); continue
    s = s[:m.end()] + "\n" + MARKUP.replace("{SVG}", svg) + s[m.end():]
    s = s.replace("</body>", JS + "</body>", 1)
    open(f, "w", encoding="utf-8").write(s)
    n += 1
    print(f"   {os.path.basename(f)}")

print(f"\nloading screen on {n} pages")
