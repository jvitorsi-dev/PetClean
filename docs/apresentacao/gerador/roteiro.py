# -*- coding: utf-8 -*-
"""Gera o ROTEIRO.md a partir das notas do apresentador (mesma fonte dos slides)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import GABRIEL, HELEN, JOAO, build

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ROTEIRO.md")

BLOCOS = {
    HELEN: ("Bloco 01 — Modelos e Entidades", "slides 1 a 6"),
    GABRIEL: ("Bloco 02 — Banco de Dados e Repositories", "slides 7 a 10"),
    JOAO: ("Bloco 03 — Swagger, CRUD e Endpoints Especializados", "slides 11 a 15"),
}


def main():
    slides = build()
    linhas = [
        "# Roteiro de fala — Apresentação da API PetClean",
        "",
        "**Três blocos**, um por integrante: Helen Aclina, Gabriel Wagner e João Vitor Silva.",
        "Este arquivo é gerado a partir das notas do apresentador embutidas no `.pptx`",
        "(`gerador/deck.py`). Cada slide tem a fala sugerida.",
        "",
        "| Bloco | Quem | Slides |",
        "|---|---|---|",
    ]
    for quem, (titulo, faixa) in BLOCOS.items():
        linhas.append(f"| {titulo.split(' — ')[0]} · {titulo.split(' — ')[1]} | {quem} | {faixa} |")
    linhas += [
        "",
        "> As notas também estão no arquivo do PowerPoint: em **Exibir › Anotações do",
        "> apresentador** (ou na tela do apresentador).",
        "",
        "---",
        "",
    ]

    atual = None
    for i, s in enumerate(slides, start=1):
        quem = s["meta"]["presenter"]
        if quem != atual:
            atual = quem
            titulo, faixa = BLOCOS[quem]
            linhas += [f"## {titulo}", "", f"**{quem}** · {faixa}", ""]
        linhas.append(f"### Slide {i:02d} — {s['meta']['title']}")
        linhas.append("")
        for par in s.get("notes", "").strip().split("\n"):
            if par.strip():
                linhas += [par.strip(), ""]
        linhas.append("")

    linhas += [
        "---",
        "",
        "## Dicas de condução",
        "",
        "- **Passagem de bastão:** cada bloco termina com uma frase que entrega a palavra.",
        "- **Se precisar encurtar:** os slides 3 (arquitetura) e 5 (relacionamentos) podem",
        "  ser resumidos em uma frase; os slides de código (06, 09, 12) devem ser mantidos.",
        "- **Demonstração ao vivo (opcional):** abrir `localhost:8080/swagger-ui.html`",
        "  depois do slide 12 é o momento de maior impacto.",
        "",
    ]

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))
    print(OUT)


if __name__ == "__main__":
    main()
