# -*- coding: utf-8 -*-
"""
Reconstroi o material da apresentacao.

    python gerador/make.py     -> PetClean-API.pptx + index.html (+ previews em PNG)
    python gerador/roteiro.py  -> ROTEIRO.md

Requer: python-pptx, pillow, fonttools, brotli.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import build                        # noqa: E402
from engine import render_html, render_pptx   # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def main():
    slides = build()

    destino_pptx = os.path.join(RAIZ, "PetClean-API.pptx")
    destino_html = os.path.join(RAIZ, "index.html")
    render_pptx(slides, destino_pptx)
    render_html(slides, destino_html, "PetClean · API REST — Apresentação")
    print("gerado:", destino_pptx)
    print("gerado:", destino_html)

    try:
        import preview
    except Exception as erro:              # pillow ausente, por exemplo
        print("pre-visualizacao ignorada:", erro)
        return

    pasta = os.path.join(RAIZ, "preview")
    os.makedirs(pasta, exist_ok=True)
    problemas = 0
    for i, slide in enumerate(slides, start=1):
        preview.render(slide["canvas"], os.path.join(pasta, "slide-%02d.png" % i))
        for aviso in preview.avaliar(slide["canvas"]):
            problemas += 1
            print("  slide %02d: %s" % (i, aviso))
    print("preview: %d imagens em preview/ · %d aviso(s) de texto"
          % (len(slides), problemas))


if __name__ == "__main__":
    main()
