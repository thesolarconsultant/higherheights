"""Text -> SVG path data with custom tracking. Y-down output, baseline at y=0."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen


class Face:
    def __init__(self, path):
        self.font = TTFont(path)
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.space_glyph = self.cmap.get(32) or self.cmap.get(0xA0) or "space"
        self.gs = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self.kern = {}
        try:
            gpos = self.font["GPOS"]
            # crude: rely on kern feature via kerning subtable lookup
            from fontTools.ttLib.tables import otTables
            lookups = gpos.table.LookupList.Lookup
            for lk in lookups:
                if lk.LookupType != 2:
                    continue
                for st in lk.SubTable:
                    if st.Format == 1:
                        for i, g1 in enumerate(st.Coverage.glyphs):
                            for ps in st.PairSet[i].PairValueRecord:
                                v = ps.Value1.XAdvance if ps.Value1 else 0
                                key = (g1, ps.SecondGlyph)
                                self.kern[key] = v
        except Exception:
            pass

    def layout(self, text, size, tracking_em=0.0, word_space_extra=0.0):
        """Returns list of (glyphname, x_offset, d_path) and total advance (px)."""
        scale = size / self.upm
        x = 0.0
        out = []
        prev = None
        tracking_px = tracking_em * size
        for ch in text:
            if ch == " ":
                x += self.hmtx[self.space_glyph][0] * scale + tracking_px + word_space_extra * size
                prev = None
                continue
            gname = self.cmap.get(ord(ch))
            if gname is None:
                continue
            pen = SVGPathPen(self.gs)
            tp = TransformPen(pen, (scale, 0, 0, -scale, x, 0))
            self.gs[gname].draw(tp)
            d = pen.getCommands()
            if prev is not None:
                x += self.kern.get((prev, gname), 0) * scale
            out.append((gname, x, d))
            x += self.hmtx[gname][0] * scale + tracking_px
            prev = gname
        return out, x - tracking_px if text else 0

    def measure(self, text, size, tracking_em=0.0, word_space_extra=0.0):
        glyphs, width = self.layout(text, size, tracking_em, word_space_extra)
        return width

    def cap_height(self, size):
        return self.font["OS/2"].sCapHeight * size / self.upm

    def x_height(self, size):
        return self.font["OS/2"].sxHeight * size / self.upm

    def ascender(self, size):
        return self.font["hhea"].ascent * size / self.upm

    def descender(self, size):
        return self.font["hhea"].descent * size / self.upm


def paths(face, text, size, tracking_em=0.0, word_space_extra=0.0, dx=0.0, dy=0.0):
    """Concatenate glyph outlines into one path string, offset by (dx,dy)."""
    scale = size / face.upm
    tracking_px = tracking_em * size
    x = 0.0
    parts = []
    prev = None
    for ch in text:
        if ch == " ":
            x += face.hmtx[face.space_glyph][0] * scale + tracking_px + word_space_extra * size
            prev = None
            continue
        gname = face.cmap.get(ord(ch))
        if gname is None:
            continue
        pen = SVGPathPen(face.gs)
        tp = TransformPen(pen, (scale, 0, 0, -scale, dx + x, dy))
        face.gs[gname].draw(tp)
        d = pen.getCommands()
        if prev is not None:
            x += face.kern.get((prev, gname), 0) * scale
        if d:
            parts.append(d)
        x += face.hmtx[gname][0] * scale + tracking_px
        prev = gname
    width = x - tracking_px if text else 0.0
    return " ".join(parts), width


import re
_CMD = re.compile(r"[MLCQZmlcqzHVhvSsTtAa]")


def _translate(d, dx, dy):
    """Translate an absolute-coordinate SVG path (M/L/C/Q/Z + relative variants) by dx,dy."""
    if dx == 0 and dy == 0:
        return d
    out = []
    tokens = re.findall(r"[A-Za-z]|-?\d*\.?\d+(?:e[-+]?\d+)?", d)
    i = 0
    cx = cy = 0.0
    sx = sy = 0.0
    cmd = None
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            out.append(t)
            i += 1
            if cmd in "Zz":
                cx, cy = sx, sy
            continue
        rel = cmd.islower()
        up = cmd.upper()
        if up in ("M", "L", "T"):
            px, py = float(tokens[i]), float(tokens[i + 1])
            i += 2
            if rel:
                px += cx; py += cy
            cx, cy = px, py
            out.append(f"{px+dx:.2f},{py+dy:.2f}")
            if up == "M":
                sx, sy = cx, cy
        elif up == "H":
            px = float(tokens[i]); i += 1
            if rel: px += cx
            cx = px
            out.append(f"{cx+dx:.2f}")
        elif up == "V":
            py = float(tokens[i]); i += 1
            if rel: py += cy
            cy = py
            out.append(f"{cy+dy:.2f}")
        elif up in ("C",):
            pts = [float(tokens[i + k]) for k in range(6)]
            i += 6
            if rel:
                pts = [pts[0] + cx, pts[1] + cy, pts[2] + cx, pts[3] + cy, pts[4] + cx, pts[5] + cy]
            cx, cy = pts[4], pts[5]
            out.append(" ".join(f"{pts[k]+ (dx if k%2==0 else dy):.2f}" for k in range(6)))
        elif up in ("Q",):
            pts = [float(tokens[i + k]) for k in range(4)]
            i += 4
            if rel:
                pts = [pts[0] + cx, pts[1] + cy, pts[2] + cx, pts[3] + cy]
            cx, cy = pts[2], pts[3]
            out.append(" ".join(f"{pts[k]+ (dx if k%2==0 else dy):.2f}" for k in range(4)))
        elif up == "S":
            pts = [float(tokens[i + k]) for k in range(4)]
            i += 4
            if rel:
                pts = [pts[0] + cx, pts[1] + cy, pts[2] + cx, pts[3] + cy]
            cx, cy = pts[2], pts[3]
            out.append(" ".join(f"{pts[k]+ (dx if k%2==0 else dy):.2f}" for k in range(4)))
        else:
            raise ValueError("unsupported cmd " + str(cmd))
    return " ".join(out)
