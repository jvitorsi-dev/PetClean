# -*- coding: utf-8 -*-
"""Gera o ROTEIRO.md a partir das notas do apresentador (mesma fonte dos slides)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deck import GABRIEL, HELEN, JOAO, build

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ROTEIRO.md")

BLOCOS = {
    HELEN: ("Bloco 01 — Modelos e Entidades", "0:00 — 5:00"),
    GABRIEL: ("Bloco 02 — Banco de Dados e Repositories", "5:00 — 10:00"),
    JOAO: ("Bloco 03 — Swagger, CRUD e Endpoints Especializados", "10:00 — 15:00"),
}


def main():
    slides = build()
    linhas = [
        "# Roteiro de fala — Apresentação da API PetClean",
        "",
        "**Duração:** 15 minutos · **3 blocos de 5 minutos**, um por integrante.",
        "Este arquivo é gerado a partir das notas do apresentador embutidas no `.pptx`",
        "(`gerador/deck.py`). Cada slide tem a fala sugerida e o tempo alvo.",
        "",
        "| Bloco | Quem | Slides | Janela |",
        "|---|---|---|---|",
        "| 01 · Modelos e Entidades | Helen Aclina | 1 a 6 | 0:00 — 5:00 |",
        "| 02 · Banco de Dados e Repositories | Gabriel Wagner | 7 a 10 | 5:00 — 10:00 |",
        "| 03 · Swagger, CRUD e Endpoints | João Vitor Silva | 11 a 15 | 10:00 — 15:00 |",
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
            titulo, janela = BLOCOS[quem]
            linhas += [f"## {titulo}", "", f"**{quem}** · janela de tempo: {janela}", ""]
        linhas.append(f"### Slide {i:02d} — {s['meta']['title']} · ⏱ {s['meta']['time']}")
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
        "- **Cronômetro:** os tempos por slide somam 14:00; os 60 segundos restantes",
        "  cobrem as duas trocas de apresentador.",
        "- **Passagem de bastão:** cada bloco termina com uma frase que entrega a palavra.",
        "- **Se atrasar:** os slides 3 (arquitetura) e 5 (relacionamentos) podem ser",
        "  resumidos em uma frase; os slides de código (06, 09, 12) devem ser mantidos.",
        "- **Demonstração ao vivo (opcional):** abrir `localhost:8080/swagger-ui.html`",
        "  depois do slide 12 é o momento de maior impacto — leva 40 segundos.",
        "",
    ]

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))
    print(OUT)


if __name__ == "__main__":
    main()
