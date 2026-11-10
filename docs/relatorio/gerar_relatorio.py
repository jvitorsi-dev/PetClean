#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o relatorio academico do Projeto de Extensao Comunitaria (Curricularizacao)
da FATEC Mauá referente ao sistema PetClean.

Revisao integral segundo as normas da ABNT:
  NBR 14724 (trabalhos academicos), NBR 6023 (referencias), NBR 6024 (numeracao
  progressiva), NBR 6027 (sumario), NBR 6028 (resumo) e NBR 10520 (citacoes).

Estrutura: as sete secoes obrigatorias do modelo institucional Modelo_projeto.pdf,
acrescidas dos elementos pre-textuais exigidos pelas normas (resumo, palavras-chave
e sumario) e dos pos-textuais (referencias).

O conteudo das 23 tabelas e preservado em tabelas.json, extraido da versao anterior
deste gerador, de modo que a revisao textual nao altere os dados tecnicos.

Uso: python3 gerar_relatorio.py
"""
import json
import textwrap
import os

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = os.path.dirname(os.path.abspath(__file__))
FIGURAS = os.path.join(BASE, "figuras")
SAIDA = os.path.join(BASE, "Relatorio_PetClean_Projeto_Extensao.docx")

with open(os.path.join(BASE, "tabelas.json"), encoding="utf-8") as _f:
    TABELAS = json.load(_f)

FONTE = "Arial"
PRETO = RGBColor(0x00, 0x00, 0x00)
CINZA_FONTE = RGBColor(0x44, 0x44, 0x44)
CINZA_FAIXA = "D9D9D9"

NUM_TABELA = [0]
NUM_FIGURA = [0]

TRAVESSAO = "\u2013"  # travessao (en dash) exigido por NBR 14724 em titulos de tabelas/figuras


# ----------------------------------------------------------------------------
# Estilos
# ----------------------------------------------------------------------------
def configurar_estilos(doc):
    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(12)
    normal.font.color.rgb = PRETO
    pf = normal.paragraph_format
    pf.space_after = Pt(0)
    pf.line_spacing = 1.5
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1 = doc.styles["Heading 1"]
    h1.font.name = FONTE
    h1.font.size = Pt(12)
    h1.font.bold = True
    h1.font.color.rgb = PRETO
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.line_spacing = 1.0
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h2 = doc.styles["Heading 2"]
    h2.font.name = FONTE
    h2.font.size = Pt(12)
    h2.font.bold = True
    h2.font.color.rgb = PRETO
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.line_spacing = 1.0
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for sec in (doc.sections[0],):
        sec.left_margin = Cm(3.0)
        sec.right_margin = Cm(2.0)
        sec.top_margin = Cm(3.0)
        sec.bottom_margin = Cm(2.0)


# ----------------------------------------------------------------------------
# Paragrafos
# ----------------------------------------------------------------------------
def par(doc, texto="", tamanho=12, negrito=False, italico=False,
        alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, antes=0, depois=6,
        espacamento=1.5, cor=None, recuo=0.0, primeira_linha=1.25):
    p = doc.add_paragraph()
    p.alignment = alinhamento
    fmt = p.paragraph_format
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    fmt.line_spacing = espacamento
    fmt.first_line_indent = Cm(primeira_linha)
    if recuo:
        fmt.left_indent = Cm(recuo)
    if texto:
        r = p.add_run(texto)
        r.font.name = FONTE
        r.font.size = Pt(tamanho)
        r.bold = negrito
        r.italic = italico
        if cor is not None:
            r.font.color.rgb = cor
    return p


def marcadores(doc, itens, tamanho=12):
    for item in itens:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Cm(1.25)
        p.paragraph_format.first_line_indent = Cm(0.0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(item)
        r.font.name = FONTE
        r.font.size = Pt(tamanho)


def h1(doc, texto):
    return doc.add_heading(texto, level=1)


def h2(doc, texto):
    return doc.add_heading(texto, level=2)


def titulo_sem_numero(doc, texto, tamanho=12, depois=6):
    """Titulo de elemento pre ou pos-textual (sem numeracao)."""
    return par(doc, texto, tamanho=tamanho, negrito=True,
               alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=0, depois=depois,
               espacamento=1.0, primeira_linha=0.0)


# ----------------------------------------------------------------------------
# Tabelas (NBR 14724: titulo acima, fonte abaixo, apenas tracos horizontais)
# ----------------------------------------------------------------------------
def legenda_tabela(doc, titulo):
    NUM_TABELA[0] += 1
    return par(doc, f"Tabela {NUM_TABELA[0]} {TRAVESSAO} {titulo}", tamanho=11, negrito=True,
               alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=8, depois=4,
               espacamento=1.0, primeira_linha=0.0)


def fonte(doc, texto):
    return par(doc, f"Fonte: {texto}", tamanho=9, italico=False,
               alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=0, depois=10,
               espacamento=1.0, cor=CINZA_FONTE, primeira_linha=0.0)


def tabela(doc, cabecalho, linhas, larguras=None, tamanho=9.0, tamanho_cab=9.0,
           alinhamento_cab=WD_ALIGN_PARAGRAPH.CENTER):
    t = doc.add_table(rows=1, cols=len(cabecalho))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    hdr = t.rows[0].cells
    for i, texto in enumerate(cabecalho):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = alinhamento_cab
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run(texto)
        r.font.name = FONTE
        r.font.size = Pt(tamanho_cab)
        r.bold = True
        sombrear(hdr[i], CINZA_FAIXA)

    for linha in linhas:
        celulas = t.add_row().cells
        for i, texto in enumerate(linha):
            celulas[i].text = ""
            p = celulas[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(str(texto))
            r.font.name = FONTE
            r.font.size = Pt(tamanho)

    if larguras:
        for row in t.rows:
            for i, larg in enumerate(larguras):
                row.cells[i].width = Cm(larg)

    aplicar_bordas(t)
    return t


def sombrear(celula, hex_cor):
    tc_pr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_cor)
    tc_pr.append(shd)


def _limpar_bordas(tabela_doc):
    tbl_pr = tabela_doc._tbl.tbl_pr if hasattr(tabela_doc._tbl, "tbl_pr") \
        else tabela_doc._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    bordas = OxmlElement("w:tblBorders")
    for lado in ("top", "start", "bottom", "end", "insideH", "insideV"):
        el = OxmlElement(f"w:{lado}")
        el.set(qn("w:val"), "nil")
        bordas.append(el)
    tbl_pr.append(bordas)


def _borda_celula(celula, lados):
    tc_pr = celula._tc.get_or_add_tcPr()
    tc_b = tc_pr.find(qn("w:tcBorders"))
    if tc_b is None:
        tc_b = OxmlElement("w:tcBorders")
        tc_pr.append(tc_b)
    for lado in lados:
        el = tc_b.find(qn(f"w:{lado}"))
        if el is None:
            el = OxmlElement(f"w:{lado}")
            tc_b.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")


def aplicar_bordas(tabela_doc):
    """Tracos horizontais no topo, abaixo do cabecalho e na base (NBR 14724)."""
    _limpar_bordas(tabela_doc)
    linhas = tabela_doc.rows
    if not linhas:
        return
    for celula in linhas[0].cells:
        _borda_celula(celula, ["top", "bottom"])
    for celula in linhas[-1].cells:
        _borda_celula(celula, ["bottom"])


def emitir_tabela(doc, numero, texto_fonte):
    """Reinsere uma das 23 tabelas preservadas em tabelas.json."""
    bloco = TABELAS[numero - 1]
    legenda_tabela(doc, bloco["legenda"])
    codigo = bloco["codigo"]
    ini = codigo.index("    tabela(doc,")
    fim = codigo.index("\n    fonte(doc,")
    exec(textwrap.dedent(codigo[ini:fim]), globals(), {"doc": doc})
    fonte(doc, texto_fonte)


# ----------------------------------------------------------------------------
# Figuras (NBR 14724: identificacao abaixo da ilustracao, fonte depois)
# ----------------------------------------------------------------------------
def figura(doc, nome_arquivo, titulo, largura_cm=15.5, fonte_texto=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Cm(0)
    r = p.add_run()
    r.add_picture(os.path.join(FIGURAS, nome_arquivo), width=Cm(largura_cm))
    NUM_FIGURA[0] += 1
    par(doc, f"Figura {NUM_FIGURA[0]} {TRAVESSAO} {titulo}", tamanho=11, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, antes=0, depois=4,
        espacamento=1.0, primeira_linha=0.0)
    if fonte_texto:
        par(doc, f"Fonte: {fonte_texto}", tamanho=9,
            alinhamento=WD_ALIGN_PARAGRAPH.CENTER, antes=0, depois=10,
            espacamento=1.0, cor=CINZA_FONTE, primeira_linha=0.0)
    return p


# ----------------------------------------------------------------------------
# Campos automaticos (sumario e paginacao)
# ----------------------------------------------------------------------------
def campo_toc(paragrafo):
    run = paragrafo.add_run()
    ini = OxmlElement("w:fldChar")
    ini.set(qn("w:fldCharType"), "begin")
    ini.set(qn("w:dirty"), "true")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r'TOC \o "1-2" \h \z \u'
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    texto = OxmlElement("w:t")
    texto.text = ("Se o sumário aparecer vazio, selecione todo o documento (Ctrl+A) e pressione F9 "
                  "no Word, ou use Ferramentas > Atualizar > Índices no LibreOffice.")
    fim = OxmlElement("w:fldChar")
    fim.set(qn("w:fldCharType"), "end")
    for el in (ini, instr, sep, texto, fim):
        run._r.append(el)


def campo_pagina(paragrafo):
    run = paragrafo.add_run()
    ini = OxmlElement("w:fldChar")
    ini.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fim = OxmlElement("w:fldChar")
    fim.set(qn("w:fldCharType"), "end")
    for el in (ini, instr, fim):
        run._r.append(el)


def quebra_pagina(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# =============================================================================
# DOCUMENTO
# =============================================================================
def construir():
    doc = Document()
    configurar_estilos(doc)

    # ---------------------------------------------------------------- CAPA ---
    for _ in range(1):
        par(doc, depois=0, espacamento=1.0, primeira_linha=0.0)

    par(doc, "FACULDADE DE TECNOLOGIA DE MAUÁ - FATEC MAUÁ", tamanho=12, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=4, espacamento=1.0, primeira_linha=0.0)
    par(doc, "Curso Superior de Tecnologia em Desenvolvimento de Software Multiplataforma",
        tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=30, espacamento=1.0,
        primeira_linha=0.0)
    par(doc, "PETCLEAN", tamanho=20, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=8, espacamento=1.0, primeira_linha=0.0)
    par(doc, "Desenvolvimento de um MVP (Mínimo Produto Viável) de software para gestão de um pet shop",
        tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=40, espacamento=1.0,
        primeira_linha=0.0)
    par(doc, "Relatório do Projeto de Extensão Comunitária (Curricularização)",
        tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=60, espacamento=1.0,
        primeira_linha=0.0)

    par(doc, "Integrantes do Projeto:", tamanho=12, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=10, espacamento=1.0, primeira_linha=0.0)
    for nome in ("Helen Aclina", "Gabriel Wagner", "João Vitor"):
        par(doc, nome, tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
            depois=2, espacamento=1.0, primeira_linha=0.0)

    par(doc, depois=70, espacamento=1.0, primeira_linha=0.0)
    par(doc, "Mauá", tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=2,
        espacamento=1.0, primeira_linha=0.0)
    par(doc, "2026", tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=0,
        espacamento=1.0, primeira_linha=0.0)

    # --------------------------------------------------------------- RESUMO ---
    quebra_pagina(doc)
    titulo_sem_numero(doc, "RESUMO")
    par(doc,
        "Este relatório apresenta o PetClean, sistema web de gestão desenvolvido como Produto Mínimo "
        "Viável (MVP) para um pet shop de pequeno porte, no âmbito do Projeto de Extensão Comunitária "
        "(Curricularização) do curso superior de tecnologia em Desenvolvimento de Software "
        "Multiplataforma da Faculdade de Tecnologia de Mauá. O problema abordado é a dependência de "
        "pequenos estabelecimentos do setor em relação a planilhas e controles manuais para organizar o "
        "atendimento diário. O objetivo foi analisar as regras de negócio do estabelecimento, "
        "documentá-las segundo práticas de Engenharia de Software e entregar um MVP funcional com base "
        "de dados própria. A solução foi inicialmente construída em PHP e, posteriormente, migrada para "
        "Java com Spring Boot, preservando a interface original e substituindo o acesso direto ao banco "
        "por uma interface de programação de aplicações (API) REST documentada. O MVP abrange cadastro "
        "de tutores e animais de estimação, agenda de serviços com controle de conflito de horário, "
        "controle de estoque com alerta de reposição, painel de indicadores e autenticação por usuário "
        "e senha com hash bcrypt. Os resultados compreendem 48 rotas REST, seis entidades e sete "
        "enumerações na base de dados, 34 testes automatizados e documentação automática por meio da "
        "especificação OpenAPI. O sistema encontra-se verificado apenas em ambiente de testes pela "
        "própria equipe; a apresentação ao estabelecimento e a validação com usuários reais constituem "
        "atividades futuras.",
        espacamento=1.0, primeira_linha=0.0, depois=10)
    par(doc, "Palavras-chave: Gestão de pet shops; Engenharia de Software; Java; Spring Boot; "
             "Produto mínimo viável.", tamanho=12, espacamento=1.0, primeira_linha=0.0)

    # ------------------------------------------------------------- SUMÁRIO ---
    quebra_pagina(doc)
    titulo_sem_numero(doc, "SUMÁRIO", tamanho=12, depois=8)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    campo_toc(p)

    # ------------------------------------------------- SECAO DE CONTEUDO 1 ---
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(3.0)
    sec.bottom_margin = Cm(2.0)
    sect_pr = sec._sectPr
    pg_num = OxmlElement("w:pgNumType")
    pg_num.set(qn("w:start"), "1")
    sect_pr.insert_element_before(pg_num, "w:cols")

    rodape = sec.footer
    rodape.is_linked_to_previous = False
    pr = rodape.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pr.paragraph_format.space_before = Pt(0)
    pr.paragraph_format.space_after = Pt(0)
    campo_pagina(pr)
    for r in pr.runs:
        r.font.name = FONTE
        r.font.size = Pt(10)

    # =========================================================================
    h1(doc, "1 CARACTERÍSTICAS DO PROJETO DE EXTENSÃO")

    par(doc,
        "Pequenos estabelecimentos do setor de serviços costumam organizar o atendimento diário com "
        "planilhas, anotações manuais ou sistemas de operação complexa, o que dificulta o controle de "
        "clientes, da agenda e do estoque. No caso dos pet shops, essa fragilidade se agrava porque a "
        "informação encontra-se distribuída entre o cadastro dos tutores, o histórico de atendimento de "
        "cada animal e o consumo de produtos de higiene e alimentação. Foi a partir dessa constatação, "
        "registrada no próprio material de divulgação do sistema, que a equipe definiu o problema a ser "
        "enfrentado (JVITORSI-DEV, 2026).")

    par(doc,
        "O PetClean é o sistema web desenvolvido para responder a esse problema. Trata-se de um Produto "
        "Mínimo Viável de gestão, construído no âmbito do Projeto de Extensão Comunitária "
        "(Curricularização) do curso superior de tecnologia em Desenvolvimento de Software "
        "Multiplataforma da Faculdade de Tecnologia de Mauá. O trabalho foi conduzido nas quatro etapas "
        "previstas no modelo institucional (FATEC MAUÁ, [s.d.]) e resultou em uma aplicação com "
        "back-end em Java e Spring Boot, interface web migrada de uma versão anterior em PHP e base de "
        "dados relacional modelada pela própria equipe. O quadro a seguir reproduz a ficha do modelo "
        "institucional, preenchida com os dados deste projeto.")

    emitir_tabela(doc, 1, "Elaborada pelos autores (2026), com base no modelo institucional da FATEC "
                          "Mauá (FATEC MAUÁ, [s.d.]) e nos artefatos do repositório do projeto "
                          "(JVITORSI-DEV, 2026).")

    par(doc,
        "O objetivo geral do trabalho consistiu em desenvolver um MVP de software para apoiar a gestão "
        "de um pet shop de pequeno porte, abrangendo o cadastro de tutores e animais, a agenda de "
        "atendimentos, o controle de estoque e a visualização de indicadores. Os objetivos específicos "
        "decorrem das quatro etapas definidas no modelo institucional (FATEC MAUÁ, [s.d.]): "
        "analisar as regras de negócio do estabelecimento e produzir a documentação de Engenharia de "
        "Software correspondente; projetar, implementar e verificar o MVP em ambiente de testes; "
        "modelar, implementar e testar a base de dados da solução; e documentar as ações desempenhadas "
        "por cada integrante da equipe executora.")

    par(doc,
        "Sob o aspecto metodológico, o trabalho caracteriza-se como pesquisa aplicada, de abordagem "
        "descritiva, realizada sob a forma de estudo de caso único, com desenvolvimento iterativo e "
        "incremental apoiado em práticas de Scrum e Kanban. Os procedimentos adotados em cada etapa são "
        "descritos nas seções correspondentes, e os produtos gerados - código-fonte, documentos e "
        "roteiros de verificação - encontram-se publicados em repositório online (JVITORSI-DEV, 2026).")

    par(doc,
        "Cabe registrar, por fim, o estágio em que o projeto se encontra. O sistema foi desenvolvido e "
        "verificado internamente pela equipe em ambiente de testes, mas ainda não foi apresentado "
        "formalmente ao estabelecimento, não foi implantado em produção e não passou por validação nem "
        "coleta de retorno com os usuários do pet shop. A apresentação ao estabelecimento e a validação "
        "com usuários reais são atividades futuras, retomadas na Seção 7.")

    # =========================================================================
    h1(doc, "2 INFORMAÇÕES DA EQUIPE DE TRABALHO")

    par(doc,
        "A equipe executora é composta por três discentes do curso superior de tecnologia em "
        "Desenvolvimento de Software Multiplataforma. A divisão de funções declarada atribui a Helen "
        "Aclina o gerenciamento das demandas, a Gabriel Wagner o desenvolvimento do front-end e da "
        "interface, e a João Vitor o desenvolvimento do back-end e da base de dados. A Seção 6 descreve "
        "as ações efetivamente desempenhadas por cada integrante, com a respectiva evidência nos "
        "artefatos do repositório (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 2, "Dados informados pela equipe (2026).")

    par(doc, "Nome do Grupo: PetClean", tamanho=12, negrito=True, antes=6, depois=8,
        primeira_linha=0.0)

    # =========================================================================
    h1(doc, "3 ETAPA 1 - DESENVOLVIMENTO DE DOCUMENTAÇÃO DE ENGENHARIA DE SOFTWARE")

    par(doc, "Objetivo: analisar as regras de negócio e relatórios diagnósticos para produzir as "
             "documentações de Engenharia de Software (FATEC MAUÁ, [s.d.]).", italico=True, depois=10)

    h2(doc, "3.1 Levantamento das regras de negócio do pet shop")

    par(doc,
        "A primeira etapa consistiu em conhecer a rotina do estabelecimento e traduzi-la em requisitos "
        "verificáveis. O levantamento partiu da observação das atividades realizadas no atendimento e "
        "resultou na delimitação de seis domínios funcionais, adotados como escopo do MVP e "
        "correspondentes aos seis épicos descritos na Seção 3.2: tutores (clientes); animais de "
        "estimação; agenda de serviços; estoque de produtos; indicadores gerenciais; e controle de "
        "acesso ao sistema. A delimitação foi necessária para que o escopo coubesse no tempo disponível "
        "sem comprometer a utilidade do sistema, priorizando as tarefas realizadas diariamente no "
        "atendimento.")

    par(doc,
        "As regras levantadas não permaneceram apenas em documento: foram materializadas como validações "
        "e impedimentos no código, o que permitiu verificar cada uma delas por teste automatizado, "
        "conforme descrito na Seção 4.4. A Tabela 3 apresenta as principais regras de negócio, o "
        "comportamento esperado do sistema e o ponto do código-fonte em que cada regra se encontra "
        "implementada.")

    emitir_tabela(doc, 3, "Elaborada pelos autores (2026), com base em "
                          "src/main/java/br/com/fatecmaua/petclean/ (JVITORSI-DEV, 2026).")

    h2(doc, "3.2 Épicos e histórias de usuário com critérios de aceitação")

    par(doc,
        "A documentação de requisitos foi organizada em seis épicos, que reúnem 25 histórias de usuário "
        "numeradas de US-01 a US-25. Cada história recebeu critérios de aceitação na forma Dado / Quando "
        "/ Então, posteriormente convertidos em casos de teste automatizados, procedimento detalhado na "
        "Seção 4.4. A numeração original das histórias foi preservada e aparece nos comentários do "
        "código e na documentação da API, o que permite rastrear cada requisito até o trecho que o "
        "implementa (JVITORSI-DEV, 2026).")

    par(doc,
        "A Tabela 4 resume a distribuição das histórias pelos épicos e a quantidade de endpoints "
        "associada a cada um, enquanto a Tabela 5 apresenta o detalhamento história por história, com a "
        "regra implementada e o endpoint correspondente.")

    emitir_tabela(doc, 4, "Elaborada pelos autores (2026), com base em README.md e control/*.java, "
                          "conferidos contra a contagem de mapeamentos @GetMapping, @PostMapping, "
                          "@PutMapping, @PatchMapping e @DeleteMapping (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 5, "Elaborada pelos autores (2026), com base em README.md, control/*.java e "
                          "service/*.java (JVITORSI-DEV, 2026).")

    h2(doc, "3.3 Requisitos não funcionais e critérios de aceitação")

    par(doc,
        "Os requisitos não funcionais considerados relevantes para o MVP foram registrados como "
        "decisões concretas de implementação e podem ser conferidos no código. Dois deles aparecem "
        "nomeados nos comentários das classes - RNF-04, relativo ao armazenamento de senhas, e RNF-09, "
        "relativo à integridade referencial das exclusões -, e os demais correspondem a restrições "
        "técnicas adotadas pela equipe, igualmente verificáveis.")

    emitir_tabela(doc, 6, "Elaborada pelos autores (2026), com base no código-fonte e em "
                          "application.properties (JVITORSI-DEV, 2026).")

    h2(doc, "3.4 Gerenciamento da equipe com Scrum e Kanban")

    par(doc,
        "A coordenação do projeto ficou a cargo de Helen Aclina, responsável pelo gerenciamento das "
        "demandas, pelo acompanhamento das entregas e pela aplicação das práticas de Scrum e Kanban. O "
        "README do repositório registra a relação entre essas práticas e o que se observa no código "
        "(JVITORSI-DEV, 2026); a Tabela 7 reproduz essa correspondência, acrescentando a evidência "
        "verificável em cada caso.")

    emitir_tabela(doc, 7, "Elaborada pelos autores (2026), com base em README.md e nos documentos de "
                          "docs/, conferidos contra o código-fonte (JVITORSI-DEV, 2026).")

    # =========================================================================
    h1(doc, "4 ETAPA 2 - PROGRAMAÇÃO, TESTE E IMPLANTAÇÃO EM AMBIENTE DE TESTES PARA UM MVP "
            "DE SISTEMA/SOFTWARE")

    par(doc, "Objetivo: projetar, desenvolver, testar e entregar um MVP funcional (FATEC MAUÁ, [s.d.]).",
        italico=True, depois=10)

    h2(doc, "4.1 Arquitetura, tecnologias e evolução de PHP para Java")

    par(doc,
        "O PetClean começou a ser desenvolvido em PHP, com páginas que reuniam marcação HTML e consultas "
        "ao banco feitas diretamente por meio da extensão PDO, controle de acesso pela sessão nativa da "
        "linguagem (PHP DOCUMENTATION GROUP, 2026) e formulários enviados com fetch e FormData para "
        "scripts auxiliares. Ao longo do semestre, seguindo as orientações dos professores e o conteúdo "
        "trabalhado nas disciplinas, o projeto foi migrado para Java 17 com Spring Boot (ORACLE, 2026a; "
        "VMWARE, 2026a), preservando a interface visual original. A migração está documentada em "
        "docs/MIGRACAO-PHP-JAVA.md, com matriz de rastreabilidade página por página e o registro das "
        "incompatibilidades encontradas (JVITORSI-DEV, 2026).")

    par(doc,
        "Importa notar que o acervo da versão em PHP não está preservado no histórico do repositório - o "
        "controle de versão contém apenas a versão em Java - e que as informações sobre a etapa anterior "
        "provêm do documento de migração elaborado pela equipe. A Tabela 8 resume as diferenças "
        "entre as duas versões.")

    emitir_tabela(doc, 8, "Elaborada pelos autores (2026), com base em docs/MIGRACAO-PHP-JAVA.md, "
                          "pom.xml e application.properties (JVITORSI-DEV, 2026).")

    par(doc,
        "Do ponto de vista arquitetural, a aplicação organiza-se em camadas, com separação rigorosa de "
        "responsabilidades: a camada de controle trata apenas do protocolo HTTP, a camada de serviço "
        "concentra as regras de negócio e a camada de repositório isola o acesso à base de dados. A "
        "Figura 1 apresenta essa organização e os elementos transversais.")

    figura(doc, "fig01_arquitetura.png",
           "arquitetura em camadas do PetClean e pacotes transversais",
           largura_cm=15.5,
           fonte_texto="Elaborada pelos autores (2026), com base em pom.xml, application.properties e "
                       "nos pacotes control/, service/, repository/, model/, dto/, security/ e "
                       "exception/ (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 9, "Elaborada pelos autores (2026), com base em pom.xml (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 10, "Elaborada pelos autores (2026), com base na contagem de arquivos de "
                           "src/main/java/br/com/fatecmaua/petclean/ - 63 arquivos e 4.325 linhas "
                           "(JVITORSI-DEV, 2026).")

    h2(doc, "4.2 Implementação do MVP: controladores, serviços e endpoints")

    par(doc,
        "A API REST expõe 48 rotas, distribuídas em oito controladores anotados com @RestController. "
        "Outros dois controladores, anotados com @Controller, atendem as nove rotas de páginas: "
        "GET /login, que encaminha o navegador à tela de autenticação, e as oito telas do painel, "
        "servidas sob /paginas/. As rotas REST estão agrupadas por domínio, e cada grupo corresponde a "
        "uma tag da documentação gerada automaticamente (SPRINGDOC, 2026).")

    emitir_tabela(doc, 11, "Elaborada pelos autores (2026), com base em control/*.java - 48 mapeamentos "
                           "REST nos oito controladores @RestController (JVITORSI-DEV, 2026).")

    par(doc,
        "O comportamento da API em situações de sucesso e de erro é uniforme, o que simplifica tanto o "
        "consumo pelo front-end quanto a verificação por testes. A Tabela 12 descreve o significado de "
        "cada código de status e apresenta exemplos de regras que o provocam.")

    emitir_tabela(doc, 12, "Elaborada pelos autores (2026), com base em exception/ErroNegocioException."
                           "java, exception/GlobalExceptionHandler.java e control/*.java "
                           "(JVITORSI-DEV, 2026).")

    par(doc,
        "A padronização das respostas de erro é feita por um único componente, o GlobalExceptionHandler, "
        "que converte exceções em objetos ErroResposta com os campos status, erro, mensagem, detalhes, "
        "momento e rota. Com isso, a interface exibe a mensagem produzida pela regra de negócio - por "
        "exemplo, “CPF já cadastrado” ou “Não é possível agendar em data passada” -, em vez de "
        "mensagens genéricas da própria tela.")

    h2(doc, "4.3 Interface web, autenticação e segurança")

    par(doc,
        "A interface foi preservada na migração: a marcação HTML, as 12 folhas de estilo (3.072 linhas) "
        "e os 10 arquivos JavaScript da versão em PHP foram mantidos, e apenas a origem dos dados e o "
        "destino dos formulários foram alterados. As oito telas do painel - dashboard, clientes, pets, "
        "estoque, agendamentos, relatórios, perfil e configurações - são renderizadas no servidor por "
        "Thymeleaf (THYMELEAF, 2026) e alimentadas pelos mesmos serviços da API; as sete páginas "
        "públicas do site - início, sobre nós, funcionalidades, fale conosco, solicitar demonstração, "
        "login e recuperar senha - são estáticas. Um arquivo novo, static/js/api.js, centraliza as "
        "chamadas à API e converte as respostas para o formato esperado pelos scripts originais, de "
        "modo que os alertas, as confirmações e o recarregamento de página permaneceram idênticos aos "
        "do sistema em PHP.")

    par(doc,
        "Três ajustes de interface foram inevitáveis e estão registrados no documento de migração: os "
        "formulários de cliente e de animal receberam campos obrigatórios inexistentes no sistema "
        "original - CPF e endereço, no primeiro caso, espécie e porte, no segundo -, e o campo de "
        "categoria do estoque, que em PHP era de texto livre, passou a ser uma lista de seleção com os "
        "seis valores da enumeração da API. Fora isso, nenhuma regra de folha de estilo foi criada ou "
        "alterada.")

    par(doc,
        "O controle de acesso é feito por sessão HTTP, sem o emprego do Spring Security em sua "
        "totalidade - decisão registrada no README como forma de manter o projeto didático "
        "(JVITORSI-DEV, 2026); apenas o módulo de criptografia do Spring Security é utilizado, para a "
        "geração e a conferência do hash bcrypt das senhas (VMWARE, 2026c). Um interceptador registrado "
        "para todas as rotas verifica a existência do usuário na sessão e age de dois modos: as "
        "requisições de navegador, reconhecidas pelo cabeçalho Accept contendo text/html, são "
        "redirecionadas para /login com a rota original guardada na sessão, à qual retornam após a "
        "autenticação; as requisições de cliente de API recebem o código 401 com corpo JSON "
        "explicativo. A autenticação compara a senha informada com o hash bcrypt armazenado no banco. O "
        "fluxo completo está representado na Figura 2.")

    figura(doc, "fig03_autenticacao.png",
           "fluxo de autenticação (US-01, US-02 e US-14) e proteção de rotas",
           largura_cm=15.5,
           fonte_texto="Elaborada pelos autores (2026), com base em security/InterceptorSeguranca.java, "
                       "security/SessaoService.java, service/AutenticacaoService.java e "
                       "control/LoginController.java (JVITORSI-DEV, 2026).")

    par(doc,
        "Duas limitações de segurança merecem registro, pois decorrem de decisões de escopo e não de "
        "falhas de implementação. A primeira: o modelo de usuário prevê dois perfis, ATENDENTE e "
        "GESTOR, e o perfil é exibido na interface, mas o interceptador verifica apenas se o usuário "
        "está autenticado, de modo que não há restrição de acesso por perfil. A segunda: a aplicação não "
        "é multi-inquilino, isto é, não há separação dos dados por estabelecimento, e todos os usuários "
        "acessam a mesma base. A Tabela 13 registra essas e outras pendências, com o encaminhamento "
        "dado pela equipe.")

    emitir_tabela(doc, 13, "Elaborada pelos autores (2026), com base em docs/MIGRACAO-PHP-JAVA.md, em "
                           "security/ e em model/PerfilEnum.java (JVITORSI-DEV, 2026).")

    h2(doc, "4.4 Testes e implantação em ambiente de testes")

    par(doc,
        "A estratégia de verificação combinou três abordagens complementares. A primeira é a suíte de "
        "testes JUnit (JUNIT, 2026), executada pelo Maven e composta por 34 testes: 28 testes de "
        "integração que exercitam a API por meio do MockMvc, verificando contrato, códigos de status e "
        "sessão em casos distribuídos entre os seis épicos e a tela de perfil; 5 testes unitários da "
        "validação de CPF; e 1 teste destinado apenas a verificar se o contexto da aplicação é "
        "carregado sem erro. A segunda é o roteiro testes-api.sh, que executa 50 verificações de ponta a "
        "ponta contra a aplicação em execução, organizadas história por história e reutilizando um "
        "cookie de sessão. A terceira é o roteiro validar-estatico.sh, que dispensa servidor e confere "
        "resíduos de PHP, vínculos quebrados, chamadas mapeadas para a API, sintaxe dos arquivos "
        "JavaScript, balanceamento do HTML e a correspondência entre as variáveis usadas nos modelos de "
        "página e os atributos fornecidos pelo controlador.")

    emitir_tabela(doc, 14, "Elaborada pelos autores (2026), com base em src/test/java/ (396 linhas), "
                           "testes-api.sh e validar-estatico.sh (JVITORSI-DEV, 2026).")

    par(doc,
        "As verificações executadas e os respectivos resultados encontram-se organizados em cinco "
        "validações, com o resultado esperado de cada uma e o registro de evidências. A Tabela 15 "
        "reproduz esse registro, distinguindo o que foi efetivamente executado do que permanece "
        "pendente.")

    emitir_tabela(doc, 15, "Elaborada pelos autores (2026), com base em docs/VALIDACAO.md e em "
                           "docs/MIGRACAO-PHP-JAVA.md (JVITORSI-DEV, 2026).")

    par(doc,
        "Quanto à implantação, o modelo institucional solicita a implantação em ambiente de testes, e é "
        "esse o estágio alcançado. A aplicação é executada localmente pelo comando spring-boot:run, "
        "atende na porta 8080 e disponibiliza o painel, a documentação interativa da API e o console do "
        "banco H2. Não houve implantação em servidor de produção nem entrega do sistema ao "
        "estabelecimento. As datas registradas na Tabela 15 referem-se a execuções realizadas pela "
        "própria equipe em seu ambiente de desenvolvimento, e não a validações conduzidas com usuários "
        "do pet shop.")

    # =========================================================================
    h1(doc, "5 ETAPA 3 - MODELAGEM, IMPLEMENTAÇÃO E TESTE DE UMA BASE PERSISTENTE DE DADOS PARA "
            "ARMAZENAMENTO DOS DADOS DA SOLUÇÃO MVP DESENVOLVIDA")

    par(doc, "Objetivo: projetar, modelar e implementar a base de dados (FATEC MAUÁ, [s.d.]).",
        italico=True, depois=10)

    h2(doc, "5.1 Escolha e configuração do sistema gerenciador de banco de dados")

    par(doc,
        "Na versão em PHP, o acesso ao banco era feito por PDO sobre MySQL (PHP DOCUMENTATION GROUP, "
        "2026; ORACLE, 2026b). No ambiente de testes da versão atual, optou-se pelo H2 em memória (H2 "
        "DATABASE ENGINE, 2026), por permitir que o projeto seja executado em qualquer máquina, sem "
        "instalação de servidor de banco: a aplicação cria o esquema e carrega os dados de demonstração "
        "automaticamente ao subir. Essa escolha tem uma consequência que precisa ser explicitada: por "
        "ser em memória, todo o conteúdo é descartado ao encerrar a aplicação, o que atende à "
        "demonstração e aos testes, mas é incompatível com o uso definitivo do sistema. A migração para "
        "um sistema gerenciador persistente figura entre as atividades futuras indicadas na Seção 7.")

    par(doc,
        "O esquema físico não é escrito manualmente: é gerado pelo Hibernate a partir do mapeamento das "
        "entidades (VMWARE, 2026b), por meio da propriedade ddl-auto=create. O roteiro de carga é "
        "executado após a criação das tabelas, graças às propriedades defer-datasource-initialization e "
        "spring.sql.init.mode=always. A Tabela 16 apresenta as configurações relevantes.")

    emitir_tabela(doc, 16, "Elaborada pelos autores (2026), com base em "
                           "src/main/resources/application.properties (JVITORSI-DEV, 2026).")

    h2(doc, "5.2 Modelo de dados: entidades, atributos e relacionamentos")

    par(doc,
        "O modelo de dados é composto por seis entidades e sete enumerações. As entidades representam o "
        "tutor e seus animais, os atendimentos agendados, os produtos em estoque, o histórico de "
        "movimentações e os usuários do sistema. As enumerações foram adotadas em todos os campos de "
        "valores fechados - espécie, porte, serviço, situação do agendamento, categoria de produto, "
        "tipo de movimentação e perfil de acesso -, o que impede o registro de valores fora do catálogo "
        "e permite que a documentação da API liste as opções automaticamente. Todas são gravadas como "
        "texto, por meio de @Enumerated(EnumType.STRING), o que mantém a base legível no console do H2. "
        "A Figura 3 apresenta o modelo.")

    figura(doc, "fig02_der.png",
           "diagrama de entidades e relacionamentos do modelo de dados do MVP",
           largura_cm=15.5,
           fonte_texto="Elaborada pelos autores (2026), com base em "
                       "src/main/java/br/com/fatecmaua/petclean/model/ (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 17, "Elaborada pelos autores (2026), com base em model/*.java "
                           "(JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 18, "Elaborada pelos autores (2026), com base em model/*.java, "
                           "service/ClienteService.java, service/PetService.java e "
                           "service/ProdutoService.java (JVITORSI-DEV, 2026).")

    emitir_tabela(doc, 19, "Elaborada pelos autores (2026), com base em model/*Enum.java "
                           "(JVITORSI-DEV, 2026).")

    h2(doc, "5.3 Carga inicial e verificação de integridade")

    par(doc,
        "O arquivo data.sql reúne 71 registros de demonstração, usados para que o painel apresente dados "
        "em qualquer execução. As datas dos agendamentos são calculadas de forma relativa, com a função "
        "DATEADD, de modo que o histórico, o dia corrente e os próximos dias permaneçam coerentes "
        "independentemente de quando a aplicação for executada - cuidado necessário porque as séries "
        "temporais do painel dependem desse histórico. Ao final do roteiro, as sequências de "
        "identificadores são reiniciadas, para que os vínculos por chave estrangeira continuem válidos.")

    emitir_tabela(doc, 20, "Elaborada pelos autores (2026), com base em src/main/resources/data.sql - "
                           "contagem de instruções insert por tabela (JVITORSI-DEV, 2026).")

    par(doc,
        "A integridade referencial é assegurada por regras explícitas de negócio, e não apenas pelas "
        "restrições do esquema. Em todos os casos de violação, a API responde com o código 409 e uma "
        "mensagem que explica o motivo e, quando cabível, indica a alternativa disponível. A Tabela 21 "
        "resume as situações verificadas e o comportamento esperado do sistema.")

    emitir_tabela(doc, 21, "Elaborada pelos autores (2026), com base em testes-api.sh (50 verificações) "
                           "e em src/test/java/.../ApiPetCleanIntegrationTest.java "
                           "(JVITORSI-DEV, 2026).")

    h2(doc, "5.4 Consultas, repositórios e projeções")

    par(doc,
        "As seis interfaces de repositório estendem JpaRepository, o que fornece as operações básicas "
        "sem que a equipe precise escrever implementação - não há classe concreta de repositório no "
        "projeto (VMWARE, 2026b). A partir daí, três níveis de consulta são empregados: métodos "
        "derivados, em que o nome do método expressa a consulta; consultas declaradas com @Query em "
        "HQL, para filtros e contagens; e consultas nativas com projeções, destinadas às telas de "
        "listagem, que retornam apenas as colunas exibidas.")

    emitir_tabela(doc, 22, "Elaborada pelos autores (2026), com base em repository/*.java e "
                           "projection/*.java (JVITORSI-DEV, 2026).")

    par(doc,
        "Cabe destacar uma decisão que revela o cuidado dispensado à modelagem: a ordenação do estoque "
        "crítico, do item com maior falta para o de menor falta, é feita na consulta, e não no "
        "JavaScript da tela. Por se tratar de uma regra de negócio, ela foi mantida na camada de "
        "persistência, onde pode ser verificada independentemente da interface.")

    # =========================================================================
    h1(doc, "6 ETAPA 4 - DOCUMENTAÇÃO E RELATO DAS AÇÕES E FUNÇÕES DESEMPENHADAS POR CADA "
            "INTEGRANTE DA EQUIPE EXECUTORA DO PROJETO")

    par(doc, "Objetivo: aplicar técnicas de gerenciamento de equipes a partir de análises das "
             "habilidades técnicas e humanas dos integrantes (FATEC MAUÁ, [s.d.]).",
        italico=True, depois=10)

    par(doc,
        "Esta seção descreve as ações de cada integrante. A divisão adotada para a apresentação técnica "
        "do sistema é a registrada no material de apresentação da equipe (JVITORSI-DEV, 2026): Helen "
        "Aclina responde pelo bloco de modelos e entidades, Gabriel Wagner pelo bloco de banco de dados "
        "e repositórios, e João Vitor pelo bloco de documentação, operações de CRUD e endpoints. Essa "
        "divisão convive com a atribuição geral de funções declarada na Seção 2, na qual a coordenação "
        "das demandas cabe à Helen, o front-end e a interface ao Gabriel, e o back-end e a base de dados "
        "ao João Vitor.")

    h2(doc, "6.1 Helen Aclina")

    par(doc, "Função declarada: gerenciamento do projeto, coordenação das demandas e acompanhamento das "
             "entregas, com aplicação de práticas de Scrum e Kanban.")
    marcadores(doc, [
        "Conduziu o planejamento e o acompanhamento das 25 histórias de usuário distribuídas em seis "
        "épicos, mantendo o fluxo de trabalho e as políticas de cada etapa, conforme descrito na "
        "Seção 3.4.",
        "Respondeu pelo Bloco 01 do material de apresentação da API - Modelos e Entidades, composto "
        "pelos slides 1 a 6 -, no qual são descritos a arquitetura em camadas, as seis entidades, as "
        "sete enumerações, os relacionamentos e as regras de integridade referencial.",
        "Acompanhou o registro das decisões e das pendências do projeto, preservado nos documentos de "
        "docs/ e no README do repositório.",
    ])
    par(doc,
        "Habilidades aplicadas: organização e visão de conjunto do produto; comunicação entre os "
        "integrantes; capacidade de traduzir a rotina do estabelecimento em requisitos verificáveis; e "
        "leitura do modelo de dados suficiente para apresentá-lo publicamente.")

    h2(doc, "6.2 Gabriel Wagner")

    par(doc, "Função declarada: desenvolvimento do front-end e da interface do sistema.")
    marcadores(doc, [
        "Atuou na camada de apresentação, composta por 12 folhas de estilo (3.072 linhas), 11 arquivos "
        "JavaScript (1.010 linhas, incluindo o novo api.js), 8 modelos de página Thymeleaf (1.940 "
        "linhas) e 7 páginas públicas, preservando o visual da versão em PHP.",
        "Participou da adaptação dos formulários às exigências da API: inclusão dos campos CPF e "
        "endereço no formulário de cliente, de espécie e porte no formulário de animal, e conversão da "
        "categoria do estoque de texto livre para lista de seleção.",
        "Respondeu pelo Bloco 02 do material de apresentação da API - Banco de Dados e Repositórios, "
        "composto pelos slides 7 a 10 -, no qual são descritos o banco H2, a carga inicial, as "
        "interfaces de repositório e as consultas em HQL, SQL nativo e projeções.",
    ])
    par(doc,
        "Habilidades aplicadas: construção de interfaces com HTML, CSS e JavaScript; atenção à "
        "fidelidade visual na migração; compreensão da camada de persistência a ponto de apresentá-la; "
        "e trabalho colaborativo na integração entre tela e API.")

    h2(doc, "6.3 João Vitor")

    par(doc, "Função declarada: desenvolvimento do back-end e do banco de dados.")
    marcadores(doc, [
        "Implementou a API REST em Java com Spring Boot (VMWARE, 2026a): oito controladores com 48 "
        "rotas, sete serviços de negócio, seis repositórios, cinco projeções, 13 objetos de "
        "transferência de dados e o tratamento centralizado de erros, totalizando 63 arquivos Java e "
        "4.325 linhas de código na aplicação.",
        "Modelou e implementou a base persistente: seis entidades, sete enumerações, o esquema gerado "
        "pelo Hibernate e o roteiro de carga com 71 registros de demonstração, conforme a Seção 5.",
        "Estruturou a verificação automatizada: 28 testes de integração com MockMvc, cinco testes "
        "unitários de CPF, o roteiro de verificação de ponta a ponta com 50 checagens e o validador "
        "estático da interface.",
        "Respondeu pelo Bloco 03 do material de apresentação da API - Documentação, operações de CRUD e "
        "endpoints especializados, composto pelos slides 11 a 15 -, no qual são apresentados a "
        "documentação automática, os códigos de status e os endpoints que concentram regras de "
        "negócio.",
    ])
    par(doc,
        "Habilidades aplicadas: programação em Java e no ecossistema Spring; modelagem relacional e "
        "escrita de consultas; automação de testes; e documentação técnica de API.")

    h2(doc, "6.4 Síntese da divisão do trabalho, habilidades e dificuldades")

    emitir_tabela(doc, 23, "Elaborada pelos autores (2026), com base na declaração da equipe e em "
                           "docs/apresentacao/README.md (JVITORSI-DEV, 2026).")

    par(doc,
        "As principais dificuldades enfrentadas pela equipe constam dos próprios documentos do projeto "
        "e merecem ser relacionadas. A migração de PHP para Java exigiu reescrever a origem dos dados "
        "de todas as telas sem alterar o visual, o que gerou onze incompatibilidades catalogadas e "
        "tratadas caso a caso: cinco foram integralmente resolvidas - campos obrigatórios ausentes nos "
        "formulários de cliente e de animal, categoria de estoque como texto livre, ausência de "
        "endpoints de perfil e bloqueio indevido de arquivos estáticos pelo interceptador - e as demais "
        "foram contornadas com ajuste de interface ou registradas como pendência de escopo. A página de "
        "relatórios chegou a apresentar erro de resposta truncada, causado pela injeção de valores do "
        "servidor em scripts no meio do documento; a correção consistiu em transportar os dados em "
        "atributos data-* e lê-los com JSON.parse. Os testes de agendamento falharam quando as datas "
        "literais usadas nos casos de teste se tornaram passadas, o que levou à substituição por datas "
        "calculadas a partir do dia corrente. Por fim, a ausência de JDK e de Maven em um dos ambientes "
        "de trabalho bloqueou parte das verificações, que permanecem como atividades futuras.")

    # =========================================================================
    h1(doc, "7 CONCLUSÃO")

    par(doc,
        "O PetClean alcançou o objetivo de entregar um MVP funcional para a gestão de um pet shop de "
        "pequeno porte. O sistema cobre, de ponta a ponta, o percurso que vai do cadastro do tutor e de "
        "seus animais até a realização do atendimento, passando pelo controle de estoque, pelos alertas "
        "de reposição e pelo painel de indicadores, com acesso protegido por usuário e senha. As 25 "
        "histórias de usuário levantadas na etapa de documentação encontram correspondência em "
        "endpoints, regras de negócio e testes automatizados, o que permitiu demonstrar a "
        "rastreabilidade entre o solicitado e o construído.")

    par(doc,
        "Quanto aos aspectos técnicos, as três entregas centrais do modelo institucional foram cumpridas. A "
        "base de dados foi modelada em seis entidades e sete enumerações, com relacionamentos e regras "
        "de integridade aplicados tanto no esquema quanto na camada de negócio. A aplicação foi "
        "organizada em camadas, com separação entre controle, regras de negócio e persistência, o que "
        "tornou possível verificar as regras sem a necessidade de executar servidor. A documentação "
        "ficou em grande parte automatizada, por meio da especificação OpenAPI, e complementada pelos "
        "documentos de migração, de validação e de verificação mantidos no repositório.")

    par(doc,
        "A contribuição esperada para a comunidade é oferecer a um pequeno estabelecimento uma "
        "alternativa organizada de gestão, em substituição às planilhas e aos controles manuais, ao "
        "mesmo tempo em que os integrantes aplicaram, diante de uma demanda real, os conteúdos de "
        "Engenharia de Software, Banco de Dados, Linguagens de Programação e Gestão de Equipes. Essa "
        "contribuição, contudo, permanece potencial: o sistema foi desenvolvido e verificado "
        "internamente pela equipe em ambiente de testes, mas não foi apresentado formalmente ao "
        "estabelecimento, não foi implantado em produção e não contou com a participação dos usuários "
        "do pet shop em validações ou na coleta de retorno. Não há, portanto, resultado medido junto ao "
        "beneficiário.")

    par(doc,
        "As dificuldades enfrentadas foram registradas ao longo deste relatório e na própria "
        "documentação do projeto: a migração tecnológica de PHP para Java com preservação da interface, "
        "o tratamento das onze incompatibilidades entre as duas versões, a correção da página de "
        "relatórios, o ajuste dos testes que dependiam de datas literais e a limitação de "
        "infraestrutura em um dos ambientes de desenvolvimento. Em cada caso, causa e solução foram "
        "documentadas, o que constitui, em si, resultado de aprendizagem para a equipe.")

    par(doc,
        "Como encaminhamentos, a equipe identifica as seguintes atividades futuras, relacionadas por "
        "ordem de prioridade para a continuidade do projeto:")
    marcadores(doc, [
        "Apresentar formalmente o sistema ao pet shop e conduzir uma sessão de validação com os "
        "usuários reais, registrando o retorno recebido - etapa prevista no próprio modelo "
        "institucional e ainda não realizada.",
        "Executar e registrar as verificações pendentes: o teste de ponta a ponta dos endpoints e a "
        "validação visual comparada às capturas da versão original.",
        "Migrar a base de dados do H2 em memória para um sistema gerenciador persistente, condição "
        "necessária para qualquer uso definitivo do sistema.",
        "Implementar as funcionalidades previstas e não contempladas no MVP: recuperação de senha, "
        "envio da solicitação de demonstração, persistência das notificações lidas e alimentação por "
        "dados reais dos gráficos que hoje exibem valores fixos.",
        "Aplicar a autorização por perfil, hoje apenas modelada, e avaliar a separação dos dados por "
        "estabelecimento, caso o sistema venha a atender mais de um pet shop.",
    ])

    par(doc,
        "O saldo do trabalho é um MVP coerente com o escopo definido, sustentado por código organizado, "
        "verificações automatizadas e documentação verificável, e com um conjunto de pendências "
        "explicitado com honestidade. A etapa que falta - apresentar o resultado ao estabelecimento e "
        "ouvir quem efetivamente utilizará o sistema - é justamente a que devolve ao projeto o seu "
        "sentido de extensão comunitária.")

    # =========================================================================
    # REFERENCIAS (NBR 6023)
    # =========================================================================
    quebra_pagina(doc)
    titulo_sem_numero(doc, "REFERÊNCIAS", tamanho=12, depois=12)

    referencias = [
        "FATEC MAUÁ. Projeto de Extensão Comunitária (Curricularização): modelo de relatório de "
        "atividade de extensão. Mauá, [s.d.]. 1 arquivo PDF (10 p.).",

        "H2 DATABASE ENGINE. H2 database engine. [S.l.], 2026. Disponível em: "
        "https://www.h2database.com/. Acesso em: 10 nov. 2026.",

        "JUNIT. JUnit 5: user guide. [S.l.], 2026. Disponível em: "
        "https://junit.org/junit5/docs/current/user-guide/. Acesso em: 10 nov. 2026.",

        "JVITORSI-DEV. PetClean: sistema de gestão para pet shops. 2026. Repositório de código-fonte. "
        "Disponível em: https://github.com/jvitorsi-dev/PetClean. Acesso em: 10 nov. 2026.",

        "ORACLE. Java 17: documentation. [S.l.], 2026a. Disponível em: "
        "https://docs.oracle.com/en/java/javase/17/. Acesso em: 10 nov. 2026.",

        "ORACLE. MySQL 8.0: reference manual. [S.l.], 2026b. Disponível em: "
        "https://dev.mysql.com/doc/refman/8.0/en/. Acesso em: 10 nov. 2026.",

        "PHP DOCUMENTATION GROUP. PHP: data objects (PDO). [S.l.], 2026. Disponível em: "
        "https://www.php.net/manual/en/book.pdo.php. Acesso em: 10 nov. 2026.",

        "SPRINGDOC. springdoc-openapi: library for OpenAPI 3 with Spring Boot. [S.l.], 2026. "
        "Disponível em: https://springdoc.org/. Acesso em: 10 nov. 2026.",

        "THYMELEAF. Thymeleaf: documentation. [S.l.], 2026. Disponível em: "
        "https://www.thymeleaf.org/documentation.html. Acesso em: 10 nov. 2026.",

        "VMWARE. Spring Boot: reference documentation. [S.l.]: Broadcom, 2026a. Disponível em: "
        "https://docs.spring.io/spring-boot/docs/current/reference/html/. Acesso em: 10 nov. 2026.",

        "VMWARE. Spring Data JPA: reference guide. [S.l.]: Broadcom, 2026b. Disponível em: "
        "https://docs.spring.io/spring-data/jpa/reference/. Acesso em: 10 nov. 2026.",

        "VMWARE. Spring Security: reference documentation. [S.l.]: Broadcom, 2026c. Disponível em: "
        "https://docs.spring.io/spring-security/reference/. Acesso em: 10 nov. 2026.",
    ]
    for ref in referencias:
        par(doc, ref, tamanho=11, alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=0, depois=6,
            espacamento=1.0, primeira_linha=0.0)

    doc.save(SAIDA)
    return SAIDA


if __name__ == "__main__":
    print("gerado:", construir())
