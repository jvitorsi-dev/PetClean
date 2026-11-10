"""
Motor de renderizacao da apresentacao PetClean.

Um unico modelo de elementos (retangulos, textos, imagens, setas) e desenhado
em dois destinos:
  * PowerPoint (.pptx) -> arquivo editavel para a banca;
  * HTML 16:9           -> visualizacao fiel no navegador (mesmo padrao visual
                           do painel do PetClean: cartoes brancos, cantos
                           arredondados, rosa #FF8C94, menta #A8E6CE).

Todas as medidas sao em polegadas sobre um palco de 13.333 x 7.5 pol (16:9).
"""

import html as htmlmod
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Emu, Pt

EMU = 914400
IN_W, IN_H = 13.333, 7.5

# ---------------------------------------------------------------- paleta ----
# Temperada a partir das telas do projeto (menus-globais.css / dashboard.css)
INK = "2C3E50"
MUTED = "6A7282"
MUTED_2 = "99A1AF"
LINE = "E5E7EB"
BG = "FAFAFA"
WHITE = "FFFFFF"

MINT = "A8E6CE"
MINT_SOFT = "EAF8F2"
MINT_TEXT = "2E7D5B"

PINK = "FF8C94"
PINK_SOFT = "FFF0F1"
PINK_TEXT = "C0555F"

PEACH = "FFD3B5"
PEACH_SOFT = "FFF4EA"
PEACH_TEXT = "AE6A1B"

CREAM = "FFF5EF"
GREEN_PALE = "DCEDC2"
SOFT = "F9FAFB"

FONT = "Poppins"
MONO = "Consolas"

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def rgb(value):
    return RGBColor.from_string(value)


def blend(color, alpha, over="FFFFFF"):
    """Mistura `color` sobre `over` (simula transparencia em solid fill)."""
    c = [int(color[i:i + 2], 16) for i in (0, 2, 4)]
    o = [int(over[i:i + 2], 16) for i in (0, 2, 4)]
    mixed = [round(c[i] * alpha + o[i] * (1 - alpha)) for i in range(3)]
    return "".join(f"{v:02X}" for v in mixed)


# ------------------------------------------------------------- elementos ----
class Canvas:
    """Lista plana de elementos graficos de um slide."""

    def __init__(self, bg=BG):
        self.bg = bg
        self.items = []

    # -- primitivas ---------------------------------------------------------
    def rect(self, x, y, w, h, fill=WHITE, line=LINE, radius=0.14, lw=0.8, dash=None):
        self.items.append(dict(k="rect", x=x, y=y, w=w, h=h, fill=fill, line=line,
                               radius=radius, lw=lw, dash=dash))
        return self

    def circle(self, x, y, w, h, fill=WHITE, line=None, lw=0.8):
        self.items.append(dict(k="rect", x=x, y=y, w=w, h=h, fill=fill, line=line,
                               radius=min(w, h) / 2, lw=lw))
        return self

    def text(self, x, y, w, h, text="", runs=None, size=12, bold=False, color=INK,
             align="l", valign="t", spacing=1.28, font="p", italic=False, alpha=None):
        if runs is None:
            runs = [dict(t=text)]
        else:
            runs = [dict(r) for r in runs]
        if alpha is not None:
            for r in runs:
                r.setdefault("color", color)
                r["color"] = blend(r["color"], alpha, self.bg)
        self.items.append(dict(k="text", x=x, y=y, w=w, h=h, runs=runs, size=size,
                               bold=bold, color=color, align=align, valign=valign,
                               spacing=spacing, font=font, italic=italic))
        return self

    def img(self, x, y, w, h=None, path=""):
        self.items.append(dict(k="img", x=x, y=y, w=w, h=h, path=path))
        return self

    def arrow(self, x, y, w, h):
        self.items.append(dict(k="arrow", x=x, y=y, w=w, h=h))
        return self

    def line(self, x, y, w, h=0.014, color=LINE):
        self.items.append(dict(k="rect", x=x, y=y, w=w, h=h, fill=color, line=None,
                               radius=0, lw=0))
        return self

    # -- componentes --------------------------------------------------------
    def chip(self, x, y, text, size=9.5, fill=SOFT, color=INK, line=LINE, h=None,
             pad=0.13, bold=False, font="p"):
        """Etiqueta com largura calculada pelo texto."""
        width = estimate_width(text, size, bold, font) / 72.0 + pad * 2
        hh = h if h else size / 72.0 * 2.1
        self.rect(x, y, width, hh, fill=fill, line=line, radius=hh / 2, lw=0.8)
        self.text(x, y, width, hh, text, size=size, bold=bold, color=color,
                  align="c", valign="m", font=font, spacing=1.0)
        return width

    def card(self, x, y, w, h, fill=WHITE, line=LINE, radius=0.14, lw=0.8):
        return self.rect(x, y, w, h, fill=fill, line=line, radius=radius, lw=lw)

    def icon_box(self, x, y, size, icon, tint=MINT_SOFT, radius=0.09, pad=0.11):
        self.rect(x, y, size, size, fill=tint, line=None, radius=radius, lw=0)
        self.img(x + pad, y + pad, size - 2 * pad, size - 2 * pad,
                 os.path.join(ASSETS, "icones", icon))
        return self


# ------------------------------------------------------------- utilidades ---
def estimate_width(text, size_pt, bold=False, font="p"):
    """Largura aproximada do texto em pontos (Poppins ~0.54em de media)."""
    factor = 0.58 if font == "m" else 0.545
    if bold:
        factor *= 1.045
    return len(text) * size_pt * factor


# =============================================================== PPTX =======
def render_pptx(slides, dest):
    prs = Presentation()
    prs.slide_width = Emu(int(IN_W * EMU))
    prs.slide_height = Emu(int(IN_H * EMU))
    blank = prs.slide_layouts[6]

    for data in slides:
        cv = data["canvas"]
        slide = prs.slides.add_slide(blank)

        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = rgb(cv.bg)

        for it in cv.items:
            _pptx_item(slide, it)

        if data.get("notes"):
            slide.notes_slide.notes_text_frame.text = data["notes"]

    prs.save(dest)
    return dest


def _pptx_item(slide, it):
    box = (Emu(int(it["x"] * EMU)), Emu(int(it["y"] * EMU)),
           Emu(int(it["w"] * EMU)), Emu(int(it["h"] * EMU)))

    if it["k"] == "rect":
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, *box)
        shape.shadow.inherit = False
        if it["radius"] <= 0.001:
            shape.adjustments[0] = 0.0
        else:
            shape.adjustments[0] = min(0.5, it["radius"] / min(it["w"], it["h"]))
        if it["fill"]:
            shape.fill.solid()
            shape.fill.fore_color.rgb = rgb(it["fill"])
        else:
            shape.fill.background()
        if it["line"]:
            shape.line.color.rgb = rgb(it["line"])
            shape.line.width = Pt(it["lw"] or 0.8)
        else:
            shape.line.fill.background()
        shape.text_frame.word_wrap = False
        return

    if it["k"] == "img":
        slide.shapes.add_picture(it["path"], *box)
        return

    if it["k"] == "arrow":
        shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, *box)
        shape.shadow.inherit = False
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb("CBD5D3")
        shape.line.fill.background()
        return

    # texto
    tb = slide.shapes.add_textbox(*box)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE,
                          "b": MSO_ANCHOR.BOTTOM}[it["valign"]]

    p = tf.paragraphs[0]
    p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER,
                   "r": PP_ALIGN.RIGHT, "j": PP_ALIGN.JUSTIFY}[it["align"]]
    # espacamento absoluto: garante no PowerPoint a mesma altura de linha do
    # HTML e da pre-visualizacao (a Poppins tem line-height natural ~1.4em,
    # o que estouraria as caixas se fosse usado o multiplicador)
    maior = max(r.get("size", it["size"]) for r in it["runs"]) if it["runs"] else it["size"]
    p.line_spacing = Pt(round(maior * it["spacing"], 1))
    p.space_before = Pt(0)
    p.space_after = Pt(0)

    for r in it["runs"]:
        run = p.add_run()
        run.text = r["t"]
        f = run.font
        f.size = Pt(r.get("size", it["size"]))
        f.bold = r.get("bold", it["bold"])
        f.italic = r.get("italic", it["italic"])
        f.name = {"p": FONT, "m": MONO}[r.get("font", it["font"])]
        f.color.rgb = rgb(r.get("color", it["color"]))


# =============================================================== HTML =======
HTML_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def rel(path):
    """Caminho relativo ao index.html (a pasta do HTML e a raiz de assets/fontes)."""
    return os.path.relpath(path, HTML_ROOT).replace(os.sep, "/")


def render_html(slides, dest, title="PetClean - API"):
    parts = []
    for i, data in enumerate(slides, start=1):
        meta = data["meta"]
        body = "".join(_html_item(it) for it in data["canvas"].items)
        notes = htmlmod.escape(data.get("notes", "")).replace("\n", "<br>")
        parts.append(f"""
    <section class="slide" id="s{i}" data-title="{htmlmod.escape(meta['title'])}"
             data-presenter="{htmlmod.escape(meta['presenter'])}"
             style="background:#{data['canvas'].bg}">
      {body}
      <div class="notes"><div class="notes-inner"><b>Fala de {htmlmod.escape(meta['presenter'])}</b><br>{notes}</div></div>
    </section>""")

    doc = HTML_TEMPLATE.replace("__SLIDES__", "".join(parts)).replace("__TITLE__", title)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return dest


def _px(v):
    return round(v * 96, 2)


def esc(text):
    return htmlmod.escape(text).replace("  ", " &nbsp;")


def _html_item(it):
    x, y, w, h = _px(it["x"]), _px(it["y"]), _px(it["w"]), _px(it["h"])

    if it["k"] == "rect":
        radius = _px(it["radius"])
        border = (f"border:{it['lw']}pt solid #{it['line']}"
                  if it["line"] else "border:none")
        bg = f"#{it['fill']}" if it["fill"] else "transparent"
        return (f'<div class="e" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'background:{bg};{border};border-radius:{radius}px"></div>')

    if it["k"] == "img":
        return (f'<img class="e" src="{rel(it["path"])}" style="left:{x}px;top:{y}px;'
                f'width:{w}px;height:{h}px">')

    if it["k"] == "arrow":
        return (f'<div class="e" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'background:#CBD5D3;clip-path:polygon(0 30%,55% 30%,55% 0,100% 50%,'
                f'55% 100%,55% 70%,0 70%)"></div>')

    align = {"l": "left", "c": "center", "r": "right", "j": "justify"}[it["align"]]
    items = {"t": "flex-start", "m": "center", "b": "flex-end"}[it["valign"]]
    inner = "".join(_span(r, it) for r in it["runs"])
    return (f'<div class="e txt" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'align-items:{items};text-align:{align};'
            f'line-height:{it["spacing"]}"><div class="tin">{inner}</div></div>')


def _span(run, it):
    size = run.get("size", it["size"])
    family = ("'Consolas','Courier New',monospace" if run.get("font", it["font"]) == "m"
              else "'Poppins',system-ui,sans-serif")
    weight = 700 if run.get("bold", it["bold"]) else 400
    color = run.get("color", it["color"])
    style = (f"font-size:{size * 4 / 3:.2f}px;font-family:{family};font-weight:{weight};"
             f"color:#{color};white-space:pre-wrap;"
             f"font-style:{'italic' if run.get('italic', it['italic']) else 'normal'}")
    return f'<span style="{style}">{esc(run["t"])}</span>'


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="icon" href="assets/logo.png">
<style>
@font-face{font-family:'Poppins';src:url('fontes/poppins-latin-400-normal.woff2') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:'Poppins';src:url('fontes/poppins-latin-500-normal.woff2') format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:'Poppins';src:url('fontes/poppins-latin-600-normal.woff2') format('woff2');font-weight:600;font-display:swap}
@font-face{font-family:'Poppins';src:url('fontes/poppins-latin-700-normal.woff2') format('woff2');font-weight:700;font-display:swap}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#EDEAE6;font-family:'Poppins',system-ui,sans-serif;
     display:flex;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}
#stage{position:relative;width:1280px;height:720px;transform-origin:center center;
       box-shadow:0 24px 70px rgba(44,62,80,.28);border-radius:10px;overflow:hidden;background:#fff}
.slide{position:absolute;inset:0;display:none}
.slide.active{display:block}
.e{position:absolute}
.txt{display:flex;overflow:visible}
.tin{width:100%;display:block}
.txt span{display:inline}
.notes{display:none}
#hud{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);display:flex;
     align-items:center;gap:14px;background:rgba(255,255,255,.96);border:1px solid #E5E7EB;
     border-radius:999px;padding:8px 18px;font-size:13px;color:#2C3E50;
     box-shadow:0 8px 24px rgba(44,62,80,.14);z-index:50}
#hud b{font-weight:600}
#hud .dot{width:6px;height:6px;border-radius:50%;background:#FF8C94}
#hud button{border:none;background:#FFF0F1;color:#C0555F;font-family:inherit;font-size:12px;
     padding:5px 12px;border-radius:999px;cursor:pointer}
#hud button:hover{background:#FF8C94;color:#fff}
#bar{position:fixed;left:0;top:0;height:4px;background:#FF8C94;width:0;z-index:60;transition:width .25s}
#panel{position:fixed;right:22px;bottom:78px;width:340px;max-height:60vh;overflow:auto;
     background:#fff;border:1px solid #E5E7EB;border-radius:16px;padding:18px;font-size:13px;
     line-height:1.55;color:#4A5565;display:none;z-index:55;box-shadow:0 12px 30px rgba(44,62,80,.16)}
#panel b{color:#2C3E50}
@media print{
  @page{size:1280px 720px;margin:0}
  body{background:#fff;display:block;overflow:visible}
  #hud,#bar,#panel{display:none}
  #stage{box-shadow:none;border-radius:0;width:1280px;height:auto}
  .slide{display:block;position:relative;page-break-after:always;width:1280px;height:720px}
}
</style>
</head>
<body>
<div id="bar"></div>
<div id="stage">
__SLIDES__
</div>
<div id="panel"></div>
<div id="hud">
  <span><b id="pname">Helen Aclina</b></span>
  <span class="dot"></span>
  <span id="pcount">1 / 15</span>
  <button id="btn-notes">Roteiro</button>
  <button id="btn-full">Tela cheia</button>
</div>
<script>
const slides=[...document.querySelectorAll('.slide')];
let i=0;
function fit(){
  const s=Math.min(window.innerWidth/1360, window.innerHeight/840);
  document.getElementById('stage').style.transform='scale('+s+')';
}
function show(n){
  i=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((s,k)=>s.classList.toggle('active',k===i));
  document.getElementById('pname').textContent=slides[i].dataset.presenter;
  document.getElementById('pcount').textContent=(i+1)+' / '+slides.length;
  document.getElementById('bar').style.width=((i+1)/slides.length*100)+'%';
  document.getElementById('panel').innerHTML='<div class="notes">'+slides[i].querySelector('.notes').innerHTML+'</div>';
}
document.addEventListener('keydown',e=>{
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(i+1)}
  if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(i-1)}
  if(e.key==='Home')show(0);
  if(e.key==='End')show(slides.length-1);
  if(e.key==='n'||e.key==='N')toggleNotes();
  if(e.key==='f'||e.key==='F')document.documentElement.requestFullscreen();
});
function toggleNotes(){
  const p=document.getElementById('panel');
  p.style.display=p.style.display==='block'?'none':'block';
}
document.getElementById('btn-notes').onclick=toggleNotes;
document.getElementById('btn-full').onclick=()=>document.documentElement.requestFullscreen();
document.addEventListener('click',e=>{if(e.target.closest('#stage'))show(i+1)});
window.addEventListener('resize',fit);
fit();show(0);
</script>
</body>
</html>
"""
