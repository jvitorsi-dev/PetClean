"""
Pre-visualizacao em PNG usando as metricas reais da fonte Poppins.

Serve para duas coisas:
  1. conferir visualmente os slides sem abrir o PowerPoint;
  2. detectar texto que vaza do cartao (a funcao `avaliar` devolve avisos).

Nao e o arquivo final: o entregavel e o .pptx / index.html.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import IN_H, IN_W  # noqa: E402

PX = 144.0  # pixels por polegada

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fontes")
FONT_FILES = {400: "poppins-latin-400-normal.woff2",
              500: "poppins-latin-500-normal.woff2",
              600: "poppins-latin-600-normal.woff2",
              700: "poppins-latin-700-normal.woff2"}
MONO_FILES = {False: "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              True: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              700: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"}

# woff2 do fontsource -> TTF (convertido no primeiro uso, pois o Pillow nao le woff2)
TTF_DIR = os.path.join(FONT_DIR, "ttf")


def garantir_ttf():
    if not os.path.isdir(TTF_DIR):
        os.makedirs(TTF_DIR, exist_ok=True)
    from fontTools.ttLib import TTFont
    for nome in FONT_FILES.values():
        destino = os.path.join(TTF_DIR, nome)
        if not os.path.exists(destino):
            fonte = TTFont(os.path.join(FONT_DIR, nome))
            fonte.flavor = None
            fonte.save(destino)


garantir_ttf()

_cache = {}
_CMAP = {}


def _has(font_path, ch):
    if font_path not in _CMAP:
        from fontTools.ttLib import TTFont
        _CMAP[font_path] = set(TTFont(font_path).getBestCmap())
    return ord(ch) in _CMAP[font_path]


def _main_font_path(mono=False):
    if mono:
        return MONO_FILES[True]
    return os.path.join(TTF_DIR, FONT_FILES[400])


def _font(size_px, weight, mono=False, fallback=False):
    key = (round(size_px, 1), weight, mono, fallback)
    if key in _cache:
        return _cache[key]
    if fallback:
        f = ImageFont.truetype(MONO_FILES[mono], max(1, int(round(size_px))))
    else:
        path = (MONO_FILES[700 if weight >= 600 else False] if mono
                else os.path.join(TTF_DIR, FONT_FILES[weight if weight in FONT_FILES else 400]))
        f = ImageFont.truetype(path, max(1, int(round(size_px))))
    _cache[key] = f
    return f


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def text_width(text, size_pt, weight=400, mono=False):
    return _font(size_pt / 72.0 * PX, weight, mono).getlength(text)


def wrap(text, size_pt, width_in, weight=400, mono=False):
    """Quebra o texto em linhas respeitando a largura (em polegadas)."""
    limit = width_in * PX
    f = _font(size_pt / 72.0 * PX, weight, mono)
    words, lines, cur = text.split(" "), [], ""
    for word in words:
        cand = word if not cur else cur + " " + word
        if f.getlength(cand) > limit and cur:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    lines.append(cur)
    return lines


def render(canvas, dest):
    W, H = int(IN_W * PX), int(IN_H * PX)
    img = Image.new("RGB", (W, H), _hex(canvas.bg))
    draw = ImageDraw.Draw(img)

    for it in canvas.items:
        x, y = it["x"] * PX, it["y"] * PX
        w, h = it["w"] * PX, it["h"] * PX

        if it["k"] == "rect":
            fill = _hex(it["fill"]) if it["fill"] else None
            outline = _hex(it["line"]) if it["line"] else None
            r = max(0, it["radius"] * PX)
            largura = max(1, int(it["lw"] / 72.0 * PX)) if outline else 0
            if r > 0:
                draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill,
                                       outline=outline, width=largura)
            else:
                draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline,
                               width=largura)
            continue

        if it["k"] == "img":
            if not os.path.exists(it["path"]):
                continue
            try:
                tile = Image.open(it["path"]).convert("RGBA")
            except Exception:
                continue
            tw, th = max(1, int(w)), max(1, int(h if it["h"] else w))
            tile = tile.resize((tw, th), Image.LANCZOS)
            img.paste(tile, (int(x), int(y)), tile)
            continue

        if it["k"] == "arrow":
            draw.polygon([(x, y + h * 0.3), (x + w * 0.55, y + h * 0.3),
                          (x + w * 0.55, y), (x + w, y + h / 2),
                          (x + w * 0.55, y + h), (x + w * 0.55, y + h * 0.7),
                          (x, y + h * 0.7)], fill=_hex("CBD5D3"))
            continue

        # ---- texto (quebra caractere a caractere, como o PowerPoint)
        glyphs = []
        for run in it["runs"]:
            mono = run.get("font", it["font"]) == "m"
            weight = 700 if run.get("bold", it["bold"]) else 400
            size = run.get("size", it["size"])
            color = run.get("color", it["color"])
            base = _main_font_path(mono)
            for ch in run["t"]:
                if ch == "\n":
                    glyphs.append(("\n", None, color, size))
                    continue
                fnt = _font(size / 72.0 * PX, weight, mono,
                            fallback=not _has(base, ch))
                glyphs.append((ch, fnt, color, size))

        lines, cur, cur_w, last_space = [], [], 0.0, -1
        limit = it["w"] * PX
        for g in glyphs:
            if g[0] == "\n":
                lines.append(cur)
                cur, cur_w, last_space = [], 0.0, -1
                continue
            ch, fnt, color, size = g
            wch = fnt.getlength(ch)
            if ch == " ":
                last_space = len(cur)
            if cur_w + wch > limit and cur and ch != " ":
                if last_space > 0:
                    lines.append(cur[:last_space])
                    cur = cur[last_space + 1:]
                    cur_w = sum(x[1].getlength(x[0]) for x in cur)
                else:
                    lines.append(cur)
                    cur, cur_w = [], 0.0
                last_space = -1
            if ch != " " or cur:
                cur.append((ch, fnt, color, size))
                cur_w += wch
        if cur:
            lines.append(cur)

        max_size = max([r.get("size", it["size"]) for r in it["runs"]] or [it["size"]])
        line_h = max_size / 72.0 * PX * it["spacing"]
        total = line_h * len(lines)
        ty = y
        if it["valign"] == "m":
            ty = y + (h - total) / 2
        elif it["valign"] == "b":
            ty = y + h - total

        for line in lines:
            if not line:
                ty += line_h
                continue
            lw = sum(f.getlength(c) for c, f, _, _ in line)
            tx = x
            if it["align"] == "c":
                tx = x + (w - lw) / 2
            elif it["align"] == "r":
                tx = x + w - lw
            for c, f, color, _ in line:
                draw.text((tx, ty + line_h * 0.06), c, font=f, fill=_hex(color))
                tx += f.getlength(c)
            ty += line_h

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)
    return dest


def avaliar(canvas, largura_segura=0.985):
    """Aponta textos que estouram a caixa em que foram colocados."""
    avisos = []
    for it in canvas.items:
        if it["k"] != "text":
            continue
        linhas, max_pt = 0, it["size"]
        for run in it["runs"]:
            mono = run.get("font", it["font"]) == "m"
            weight = 700 if run.get("bold", it["bold"]) else 400
            size = run.get("size", it["size"])
            max_pt = max(max_pt, size)
            n = 0
            for seg in run["t"].split("\n"):
                n += max(1, len(wrap(seg, size, it["w"] * largura_segura, weight, mono)))
            linhas = max(linhas, n)
        altura = linhas * max_pt / 72.0 * it["spacing"]
        if altura > it["h"] + 0.045:
            avisos.append("altura: %.2f in > %.2f in  %r" % (altura, it["h"],
                                                             it["runs"][0]["t"][:70]))
        for run in it["runs"]:
            mono = run.get("font", it["font"]) == "m"
            weight = 700 if run.get("bold", it["bold"]) else 400
            size = run.get("size", it["size"])
            for seg in run["t"].split("\n"):
                wpx = text_width(seg, size, weight, mono) / PX
                if wpx > it["w"] * 1.02 and len(seg.split()) == 1:
                    avisos.append("largura: %.2f in > %.2f in  %r" % (wpx, it["w"],
                                                                      seg[:60]))
    return avisos
