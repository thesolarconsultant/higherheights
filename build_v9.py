# -*- coding: utf-8 -*-
"""v9: remove every numeric index. Names and disciplines do the work instead."""
import re, shutil, os

SRC, DST = "site-v8", "site-v9"
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
p = os.path.join(DST, "index.html")
s = open(p, encoding="utf-8").read()
before = s


def sub(old, new, why, count=1):
    global s
    if old not in s:
        raise SystemExit("MISS: " + why + "\n  " + old[:110])
    s = s.replace(old, new, count)
    print("  ok  " + why)


# ── 1. each film gets a discipline, which is what the index line should say ──
KINDS = {
    '"Heritage", c:"Spens Motors"': "Heritage film",
    '"Styled By You", c:"NOBL"': "Brand film",
    '"In the Case", c:"WatchTrader & Co"': "Machine story",
    '"RM 69", c:"Richard Mille"': "Machine story",
    '"Walking", c:"Clean Co"': "Brand film",
}
for key, kind in KINDS.items():
    old = "{ t:" + key
    if old in s:
        s = s.replace(old, "{ k:\"" + kind + "\", t:" + key, 1)
print("  ok  disciplines tagged")
# anything untagged still needs the field
s = re.sub(r'\{ t:"', '{ k:"Film", t:"', s)

# ── 2. the chapter rail: ticks, not numerals ──
sub("    b.textContent=String(i+1).padStart(2,'0');\n",
    "    b.appendChild(document.createElement('i'));\n"
    "    b.appendChild(document.createTextNode(f.t));\n",
    "rail -> tick + name")

# ── 3. the index line says what kind of film it is ──
sub("    idxW.textContent=String(i+1).padStart(2,'0')+' — Work';",
    "    idxW.textContent=f.k;",
    "index line -> discipline")

# ── 4. the filmstrip: titles only ──
sub("""    b.innerHTML='<span class="n">'+String(i+1).padStart(2,'0')+'</span><span class="t">'+f.t+'</span>';""",
    """    b.innerHTML='<span class="t">'+f.t+'</span><span class="c">'+f.c+'</span>';""",
    "strip -> title + client")

# ── 5. the static placeholder in the markup ──
sub('<div class="micro work__idx" id="w-idx">01 — Work</div>',
    '<div class="micro work__idx" id="w-idx">Heritage film</div>',
    "static index placeholder")

# ── 6. restyle: the strip now carries two lines of words, no numeral column ──
sub(".strip .n{display:block;font-size:9.5px;letter-spacing:.18em;color:var(--label);margin-bottom:.3rem}",
    ".strip .c{display:block;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;"
    "color:var(--label);margin-top:.34rem;opacity:.78}",
    "strip style: numeral -> client line")

sub("    .strip .n{margin:0;font-size:8.5px}",
    "    .strip .c{margin-top:.2rem;font-size:8px}",
    "strip style (mobile)")

# ── 7. the rail ticks need a look ──
sub(".work__idx{margin-bottom:1rem}",
    ".work__idx{margin-bottom:1rem}\n"
    "  .work__rail button{display:flex;align-items:center;gap:.6rem;background:none;border:0;padding:.34rem 0;"
    "cursor:pointer;font:inherit;font-size:10px;letter-spacing:.13em;text-transform:uppercase;"
    "color:var(--label);opacity:.52;transition:opacity .3s,color .3s}\n"
    "  .work__rail button i{display:block;width:16px;height:1px;background:currentColor;flex:none;"
    "transition:width .35s cubic-bezier(.22,1,.36,1)}\n"
    "  .work__rail button:hover{opacity:.9}\n"
    "  .work__rail button.is-live{opacity:1;color:var(--white)}\n"
    "  .work__rail button.is-live i{width:30px;background:var(--accent)}\n"
    "  @media(max-width:860px){.work__rail button{font-size:0;gap:0}"
    ".work__rail button i{width:10px}.work__rail button.is-live i{width:20px}}",
    "rail tick styling")

open(p, "w", encoding="utf-8").write(s)
print(f"\nv9 written: {len(before)} -> {len(s)} bytes")

# ── proof: no numerals left anywhere ──
leftovers = re.findall(r"padStart\(2|>0[1-8]\s*<|\(0[1-8]\)|\b0[1-8] —", s)
print("numeric-index leftovers:", leftovers or "none")
