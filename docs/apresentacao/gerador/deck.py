# -*- coding: utf-8 -*-
"""
Conteudo da apresentacao "PetClean API".

15 slides divididos igualmente entre os tres blocos:
  Bloco 01 - Helen Aclina   (slides 1-6)   Modelos e Entidades
  Bloco 02 - Gabriel Wagner (slides 7-10)  Banco de Dados e Repositories
  Bloco 03 - Joao Vitor     (slides 11-15) Swagger, CRUD e endpoints
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import (ASSETS, CREAM, GREEN_PALE, INK, LINE, MINT, MINT_SOFT,
                    MINT_TEXT, MUTED, MUTED_2, PEACH, PEACH_SOFT, PEACH_TEXT, PINK,
                    PINK_SOFT, PINK_TEXT, SOFT, WHITE, Canvas, blend, estimate_width)

M = 0.55                 # margem lateral
CW = 13.333 - 2 * M      # largura util (12.233)
RIGHT = 13.333 - M       # 12.783

KW = "C0555F"            # palavra-chave (rosa escuro)
ANN = "AE6A1B"           # anotacao (ambar)
STR = "2E7D5B"           # string (verde)
CMT = "99A1AF"           # comentario
PLN = "4A5565"           # texto de codigo
TYP = "3B5C8A"           # tipo
FN = "8A6D3B"            # nome de metodo

HELEN = "Helen Aclina"
GABRIEL = "Gabriel Wagner"
JOAO = "Joao Vitor Silva"

SLIDES = []


# ============================================================ utilidades =====
def add(canvas, title, presenter, notes=""):
    SLIDES.append(dict(canvas=canvas, meta=dict(title=title, presenter=presenter),
                       notes=notes))


def shell(cv, section, presenter, page, total=15):
    """Barra superior + rodape iguais em todos os slides internos."""
    cv.rect(0, 0, 13.333, 0.78, WHITE, None, radius=0)
    cv.line(0, 0.775, 13.333, 0.012, LINE)
    cv.img(0.55, 0.215, 1.03, 0.33, os.path.join(ASSETS, "logotipo.png"))
    cv.line(1.82, 0.2, 0.012, 0.39, LINE)
    cv.text(2.0, 0.30, 5.2, 0.24, section.upper(), size=8.6, bold=True,
            color=MUTED_2, spacing=1.0)

    chip_label = f"{page:02d}/{total}"
    chip_w = estimate_width(chip_label, 8.4, False, "p") / 72.0 + 0.26
    cv.text(RIGHT - chip_w - 0.24 - 1.85, 0.285, 1.85, 0.25, presenter, size=9,
            bold=True, color=INK, align="r", spacing=1.0)
    cv.chip(RIGHT - chip_w, 0.255, chip_label, size=8.4, fill=SOFT, color=MUTED,
            h=0.27)

    cv.line(0.55, 7.10, CW, 0.010, LINE)
    cv.text(0.55, 7.17, 8.2, 0.22,
            "PetClean · API REST de gestão para pet shops · Projeto Interdisciplinar — Fatec Mauá",
            size=7.8, color=MUTED_2, spacing=1.0)
    cv.text(9.2, 7.17, 3.58, 0.22, "Helen · Gabriel · João Vitor", size=7.8,
            color=MUTED_2, align="r", spacing=1.0)


def head(cv, kicker, title, sub=None, y=1.10):
    cv.text(M, y, CW, 0.24, kicker.upper(), size=8.8, bold=True, color=PINK_TEXT,
            spacing=1.0)
    cv.text(M, y + 0.24, CW, 0.52, title, size=25, bold=True, color=INK, spacing=1.12)
    if sub:
        cv.text(M, y + 0.80, 11.9, 0.26, sub, size=11, color=MUTED, spacing=1.3)


def _code_rows(cv, x, top, w, rows, size, step, pad):
    for i, row in enumerate(rows):
        if isinstance(row, str):
            row = [(row, PLN)]
        runs = [dict(t=t, color=c, font="m", size=size) for t, c in row]
        cv.text(x + pad, top + i * step, w - 2 * pad, step, runs=runs, size=size,
                spacing=1.05, font="m")
    return cv


def code_card(cv, x, y, w, h, rows, size=8.3, step=0.158, pad=0.2, label=None,
              bg=SOFT, border=LINE, head=None):
    """Cartao de codigo. `head` = (titulo, subtitulo) exibido no topo."""
    cv.rect(x, y, w, h, bg, border, radius=0.14)
    if head:
        cv.text(x + pad, y + 0.16, w - 2 * pad - 1.75, 0.24,
                runs=[dict(t=head[0], color=INK, bold=True, size=9.4),
                      dict(t=head[1], color=MUTED, size=8.4)],
                size=8.4, spacing=1.0)
        if label:
            cv.text(x + w - pad - 1.75, y + 0.19, 1.75, 0.2,
                    runs=[dict(t=label, color=MUTED_2, font="m", size=7)],
                    align="r", spacing=1.0)
        cv.line(x + pad, y + 0.46, w - 2 * pad, 0.010, LINE)
        return _code_rows(cv, x, y + 0.58, w, rows, size, step, pad)

    top = y + pad
    if label:
        cv.text(x + pad, y + 0.14, w - 2 * pad, 0.2, label.upper(), size=7.4,
                bold=True, color=MUTED_2, spacing=1.0)
        cv.line(x + pad, y + 0.40, w - 2 * pad, 0.010, LINE)
        top = y + 0.50
    return _code_rows(cv, x, top, w, rows, size, step, pad)


def bullets(cv, x, y, w, lines, color=MUTED, size=10.2, gap=0.30, dot=PINK):
    for i, line in enumerate(lines):
        yy = y + i * gap
        cv.circle(x, yy + 0.085, 0.075, 0.075, dot, None)
        cv.text(x + 0.19, yy, w - 0.19, gap, line, size=size, color=color, spacing=1.2)
    return y + len(lines) * gap


def field_lines(cv, x, y, w, lines, size=8.3, step=0.155):
    for i, (text, color) in enumerate(lines):
        cv.text(x, y + i * step, w, step,
                runs=[dict(t=text, color=color, font="m", size=size)],
                size=size, spacing=1.05, font="m")


def avatar(cv, x, y, size, img, ring=MINT_SOFT):
    cv.circle(x, y, size, size, ring, None)
    cv.img(x + size * 0.06, y + size * 0.06, size * 0.88, size * 0.88,
           os.path.join(ASSETS, img))


# ============================================================== slide 01 =====
def s01_capa():
    cv = Canvas(bg=CREAM)
    cv.circle(9.05, -1.15, 6.2, 6.2, fill="FDEBE0", line=None)
    cv.circle(11.35, 4.55, 2.85, 2.85, fill=GREEN_PALE, line=None)
    cv.circle(0.15, 5.35, 1.5, 1.5, fill=PINK_SOFT, line=None)

    cv.img(M, 0.52, 2.24, 0.72, os.path.join(ASSETS, "logotipo.png"))

    cv.chip(M, 1.52, "PROJETO INTERDISCIPLINAR · FATEC MAUÁ · 2026", size=8.4,
            fill=WHITE, color=MUTED, line=LINE, h=0.32)
    cv.text(M, 2.0, 6.5, 1.35,
            runs=[dict(t="A API do "), dict(t="PetClean", color=PINK_TEXT)],
            size=40, bold=True, color=INK, spacing=1.06)
    cv.text(M, 2.74, 6.5, 0.42, "gestão de pet shops, do banco ao endpoint",
            size=15.5, color=INK, spacing=1.2)
    cv.text(M, 3.3, 5.75, 1.0,
            "Como o back-end do PetClean foi construído: entidades JPA, banco H2, "
            "repositories, documentação Swagger/OpenAPI e endpoints com regras de negócio.",
            size=10.6, color=MUTED, spacing=1.5)
    cv.line(M, 4.42, 5.75, 0.010, LINE)

    for i, (nome, img, papel) in enumerate([
            (HELEN, "IvesHelen.png", "Modelos e Entidades"),
            (GABRIEL, "CachorroGab.png", "Banco e Repositories"),
            (JOAO, "Hamster Lu.png", "Swagger e CRUD")]):
        x = M + i * 1.97
        avatar(cv, x, 4.66, 0.62, img)
        cv.text(x + 0.76, 4.68, 1.25, 0.22, nome, size=9, bold=True, color=INK,
                spacing=1.0)
        cv.text(x + 0.76, 4.92, 1.3, 0.24, papel, size=7.8, color=MUTED, spacing=1.2)

    # Amostra real de resposta: GET /api/pets?termo=thor (dados do data.sql)
    rows_json = [
        [("{", CMT)],
        [('  "id": ', PLN), ("1", TYP), (",", PLN)],
        [('  "nome": ', PLN), ('"Thor"', STR), (",", PLN)],
        [('  "especie": ', PLN), ('"CACHORRO"', STR), (",", PLN)],
        [('  "raca": ', PLN), ('"Golden Retriever"', STR), (",", PLN)],
        [('  "porte": ', PLN), ('"GRANDE"', STR), (",", PLN)],
        [('  "idade": ', PLN), ("4", TYP), (",", PLN)],
        [('  "cliente": {', PLN)],
        [('    "nome": ', PLN), ('"Maria da Silva"', STR)],
        [("  }", PLN)],
        [("}", PLN)],
    ]
    code_card(cv, 7.22, 1.26, 5.72, 3.92, rows_json, size=9.2, step=0.26,
              pad=0.26, label="json",
              head=("Resposta da API  ", "GET /api/pets?termo=thor"))
    cv.line(7.48, 4.72, 5.2, 0.010, LINE)
    cv.text(7.48, 4.84, 5.2, 0.24,
            runs=[dict(t="200 ", color=MINT_TEXT, bold=True, size=8.4),
                  dict(t="OK", color=MUTED, size=8.4),
                  dict(t="   ·   application/json   ·   1 objeto", color=MUTED_2,
                       size=8.4)],
            size=8.4, spacing=1.0)

    cv.rect(M, 5.9, CW, 0.92, WHITE, LINE, radius=0.2)
    itens = [("6 requisitos", "do projeto atendidos"), ("6 entidades", "e 7 enums no domínio"),
             ("48 endpoints", "REST documentados")]
    for i, (big, small) in enumerate(itens):
        x = M + 0.34 + i * 3.05
        cv.text(x, 6.08, 2.4, 0.28, big, size=12.5, bold=True, color=INK, spacing=1.0)
        cv.text(x, 6.38, 2.6, 0.24, small, size=8.8, color=MUTED, spacing=1.0)
    cv.line(M + 2.7, 6.06, 0.010, 0.58, LINE)
    cv.line(M + 5.75, 6.06, 0.010, 0.58, LINE)
    cv.text(9.35, 6.16, 3.2, 0.4,
            runs=[dict(t="Swagger UI  ", color=MUTED, size=8.4),
                  dict(t="localhost:8080/swagger-ui.html", color=PINK_TEXT, size=8.4,
                       font="m")],
            align="r", spacing=1.1)

    add(cv, "Capa", HELEN, notes=(
        "Boa noite! Somos o grupo do PetClean — eu sou a Helen, e junto comigo estão o "
        "Gabriel e o João Vitor. Vamos apresentar a API do PetClean, o back-end Java "
        "do nosso Projeto Interdisciplinar.\n"
        "A ideia é simples: o painel que vocês já conhecem só funciona porque existe uma "
        "API por trás. É ela que guarda os clientes, os pets, os agendamentos e o estoque. "
        "Hoje mostramos como essa API foi construída — os modelos, o banco H2, os "
        "repositories, a documentação no Swagger e os endpoints com as regras de negócio.\n"
        "Dividimos a apresentação em três blocos: eu começo pelos modelos e entidades, "
        "o Gabriel segue com banco de dados e repositories e o João Vitor fecha com "
        "Swagger, CRUD e endpoints especializados."))


# ============================================================== slide 02 =====
def s02_roteiro():
    cv = Canvas()
    shell(cv, "Roteiro", HELEN, 2)
    head(cv, "Roteiro",
         "Três blocos, cada um com um responsável",
         "A ordem acompanha o caminho de uma requisição: do modelo de dados até o endpoint documentado.")

    cards = [
        dict(nome=HELEN, img="IvesHelen.png", tema="Modelos e Entidades",
             tag="BLOCO 01", cor=MINT_SOFT, cor2=MINT_TEXT, faixa=MINT,
             itens=["Arquitetura em camadas do projeto",
                    "As 6 entidades JPA e os 7 enums",
                    "Relacionamentos e integridade referencial",
                    "Anotações JPA e @Schema no código"],
             tempo="slides 1 a 6"),
        dict(nome=GABRIEL, img="CachorroGab.png", tema="Banco de Dados e Repositories",
             tag="BLOCO 02", cor=PINK_SOFT, cor2=PINK_TEXT, faixa=PINK,
             itens=["H2 em memória, console e ddl-auto",
                    "data.sql: 71 registros de demonstração",
                    "Spring Data JPA: o CRUD vem pronto",
                    "HQL, SQL nativo e projections"],
             tempo="slides 7 a 10"),
        dict(nome=JOAO, img="Hamster Lu.png", tema="Swagger, CRUD e regras",
             tag="BLOCO 03", cor=PEACH_SOFT, cor2=PEACH_TEXT, faixa=PEACH,
             itens=["springdoc: Swagger UI e OpenAPI JSON",
                    "CRUD completo com status HTTP corretos",
                    "Filtros e buscas parametrizadas",
                    "Conflito de horário e estoque crítico"],
             tempo="slides 11 a 15"),
    ]

    w, gap = 3.85, 0.34
    for i, c in enumerate(cards):
        x = M + i * (w + gap)
        cv.rect(x, 2.32, w, 3.86, WHITE, LINE, radius=0.2)
        cv.rect(x, 2.32, w, 0.10, c["faixa"], None, radius=0.05)
        cv.chip(x + 0.26, 2.55, c["tag"], size=7.6, fill=c["cor"], color=c["cor2"],
                line=c["cor"], h=0.26)
        avatar(cv, x + 0.26, 2.95, 0.72, c["img"], c["cor"])
        cv.text(x + 1.1, 2.98, w - 1.3, 0.26, c["nome"], size=12, bold=True,
                color=INK, spacing=1.0)
        cv.text(x + 1.1, 3.26, w - 1.25, 0.44, c["tema"], size=9.2, bold=True,
                color=c["cor2"], spacing=1.2)
        cv.line(x + 0.26, 3.86, w - 0.52, 0.010, LINE)
        bullets(cv, x + 0.26, 4.02, w - 0.5, c["itens"], size=9.1, gap=0.40,
                dot=c["faixa"])
        cv.line(x + 0.26, 5.74, w - 0.52, 0.010, LINE)
        cv.text(x + 0.26, 5.84, w - 0.52, 0.24, c["tempo"], size=8.4, color=MUTED,
                spacing=1.0)

    add(cv, "Roteiro", HELEN, notes=(
        "Antes de começar, só para vocês saberem onde estamos indo.\n"
        "A apresentação tem três blocos, um para cada integrante. Eu "
        "começo pelo modelo de dados: como o PetClean representa clientes, pets, "
        "agendamentos e estoque no código Java. O Gabriel continua com a camada de "
        "persistência — o banco H2 e os repositories. E o João Vitor fecha com a parte "
        "que todo mundo vê: a documentação no Swagger, o CRUD e os endpoints que carregam "
        "as regras de negócio.\n"
        "A ordem não é por acaso: ela é exatamente o caminho que uma requisição faz dentro "
        "do projeto."))


# ============================================================== slide 03 =====
def s03_arquitetura():
    cv = Canvas()
    shell(cv, "Visão geral", HELEN, 3)
    head(cv, "Arquitetura do projeto",
         "Cada classe tem um papel: do HTTP ao banco",
         "Organização em camadas no pacote br.com.fatecmaua.petclean, o mesmo padrão do projeto de referência da disciplina.")

    cams = [
        ("Painel ou Swagger", "HTML + JS, Postman", "relatorios.png", MINT_SOFT, MINT_TEXT),
        ("control/", "Recebe HTTP e valida", "dash.png", PINK_SOFT, PINK_TEXT),
        ("service/", "Regras de negócio", "clientes.png", PEACH_SOFT, PEACH_TEXT),
        ("repository/", "Spring Data JPA", "estoque.png", "EEF3FB", "3B5C8A"),
        ("H2", "jdbc:h2:mem:petcleandb", "agendamentos.png", "F2F0FB", "5B4B9A"),
    ]
    w, gap, y = 2.15, 0.30, 2.60
    for i, (titulo, sub, icone, tint, cor) in enumerate(cams):
        x = M + 0.14 + i * (w + gap)
        cv.rect(x, y, w, 1.82, WHITE, LINE, radius=0.18)
        cv.icon_box(x + 0.22, y + 0.2, 0.44, icone, tint, radius=0.11)
        cv.text(x + 0.22, y + 0.78, w - 0.44, 0.26, titulo, size=10.6, bold=True,
                color=INK, spacing=1.0)
        cv.text(x + 0.22, y + 1.06, w - 0.4, 0.55, sub, size=8.4, color=MUTED,
                spacing=1.25)
        if i < len(cams) - 1:
            cv.arrow(x + w + 0.045, y + 0.79, 0.21, 0.22)

    cv.text(M, 2.30, 5.0, 0.22,
            runs=[dict(t="Java 17", color=INK, bold=True),
                  dict(t="  ·  Spring Boot 3.5.16  ·  Maven", color=MUTED)],
            size=8.6, spacing=1.0)
    cv.text(6.6, 2.30, (RIGHT - 6.6), 0.22,
            runs=[dict(t="web · data-jpa · validation · thymeleaf · springdoc",
                       color=MUTED, font="m", size=7.6)],
            align="r", spacing=1.0)

    cards = [
        ("Validação de entrada", MINT_TEXT, MINT_SOFT,
         "O controller recebe um DTO com @Valid. Campos obrigatórios, CPF com dígito "
         "verificador e idade entre 0 e 40 são barrados antes de chegar ao service."),
        ("Erros padronizados", PINK_TEXT, PINK_SOFT,
         "GlobalExceptionHandler transforma exceções em JSON: 400 para dados inválidos, "
         "409 para conflito de negócio e 422 para regra não atendida."),
        ("Consultas otimizadas", PEACH_TEXT, PEACH_SOFT,
         "Projections trazem só as colunas usadas nas listagens — sem carregar a entidade "
         "inteira quando a tela precisa de três campos."),
    ]
    w2 = 3.95
    for i, (titulo, cor, tint, texto) in enumerate(cards):
        x = M + i * (w2 + 0.19)
        cv.rect(x, 4.68, w2, 1.32, tint, None, radius=0.16)
        cv.text(x + 0.24, 4.82, w2 - 0.48, 0.24, titulo, size=10, bold=True,
                color=cor, spacing=1.0)
        cv.text(x + 0.24, 5.10, w2 - 0.46, 0.82, texto, size=8.5, color=PLN,
                spacing=1.35)

    cv.rect(M, 6.14, CW, 0.84, WHITE, LINE, radius=0.16)
    cv.text(M + 0.24, 6.24, 2.6, 0.2, "UMA REQUISIÇÃO NA PRÁTICA", size=7.4,
            bold=True, color=MUTED_2, spacing=1.0)
    cv.text(M + 0.24, 6.52, CW - 0.5, 0.3,
            runs=[dict(t="POST /api/agendamentos", color=PINK_TEXT, bold=True),
                  dict(t="   →   AgendamentoController   →   AgendamentoService "),
                  dict(t="  (checa conflito) ", color=KW),
                  dict(t="  →   AgendamentoRepository   →   H2")],
            size=9.2, color=PLN, font="m", spacing=1.0)

    add(cv, "Arquitetura", HELEN, notes=(
        "Antes de entrar nas entidades, vale entender onde elas vivem.\n"
        "O projeto está dividido em camadas, igual ao padrão que a gente viu na "
        "disciplina. A requisição entra pelo control, que só cuida de HTTP: recebe o JSON, "
        "valida com Bean Validation e devolve o status certo. Ele chama o service, que é "
        "onde ficam as regras de negócio — por exemplo, checar conflito de horário. O "
        "service fala com o repository, e o repository com o banco H2.\n"
        "Essa separação é o que permite testar as regras sem subir servidor: a maioria dos "
        "nossos testes ataca o service direto. E o GlobalExceptionHandler garante que "
        "qualquer erro saia no mesmo formato JSON, o que o painel consegue mostrar em "
        "qualquer tela."))


# ============================================================== slide 04 =====
def s04_entidades():
    cv = Canvas()
    shell(cv, "Modelos e entidades", HELEN, 4)
    head(cv, "Modelos e Entidades",
         "Seis entidades, um domínio só",
         "Pacote model/ — cada classe é uma tabela (@Entity + @Table) e cada campo é uma coluna documentada com @Schema.")

    entidades = [
        ("Cliente", "cliente", "clientes.png", MINT_SOFT, [
            ("id : Long", INK), ("nome : String", PLN), ("cpf : String  unique", PLN),
            ("telefone · email · endereco", PLN), ("@OneToMany  pets, agendamentos", ANN)]),
        ("Pet", "pet", "pets.png", PINK_SOFT, [
            ("id : Long", INK), ("cliente : Cliente  @ManyToOne", ANN),
            ("nome · raca : String", PLN), ("especie · porte : enums", PLN),
            ("idade : Integer  (0 a 40)", PLN)]),
        ("Agendamento", "agendamento", "agendamentos.png", PEACH_SOFT, [
            ("cliente · pet : @ManyToOne", ANN), ("servico : ServicoEnum", PLN),
            ("data · hora · valor", PLN), ("status : StatusAgendamentoEnum", PLN),
            ("atualizadoEm · motivoCancelamento", PLN)]),
        ("Produto", "produto", "estoque.png", "EEF3FB", [
            ("id : Long", INK), ("nome · categoria : enum", PLN),
            ("quantidade · estoqueMinimo", PLN), ("preco : BigDecimal", PLN),
            ("ativo : Boolean", PLN)]),
        ("MovimentacaoEstoque", "movimentacao_estoque", "relatorios.png", "F2F0FB", [
            ("id : Long", INK), ("produto : Produto  @ManyToOne", ANN),
            ("tipo : TipoMovimentacaoEnum", PLN), ("quantidade : Integer", PLN),
            ("observacao · registradoEm", PLN)]),
        ("Usuario", "usuario", "dash.png", MINT_SOFT, [
            ("nome · email  unique", PLN), ("senhaHash : String  bcrypt", PLN),
            ("perfil : PerfilEnum", PLN), ("nomePetshop · telefone · endereco", PLN),
            ("foto : byte[] · dataAlteracaoSenha", PLN)]),
    ]

    w, h, gx, gy = 3.85, 2.02, 0.34, 0.26
    for i, (nome, tabela, icone, tint, campos) in enumerate(entidades):
        x = M + (i % 3) * (w + gx)
        y = 2.28 + (i // 3) * (h + gy)
        cv.rect(x, y, w, h, WHITE, LINE, radius=0.18)
        cv.icon_box(x + 0.22, y + 0.2, 0.4, icone, tint, radius=0.1)
        cv.text(x + 0.72, y + 0.24, w - 0.9, 0.24, nome, size=11, bold=True,
                color=INK, spacing=1.0)
        cv.text(x + 0.72, y + 0.46, w - 0.9, 0.22,
                runs=[dict(t="@Table ", color=MUTED_2),
                      dict(t=tabela, color=MUTED, bold=True)],
                size=7.4, font="m", spacing=1.0)
        cv.line(x + 0.22, y + 0.74, w - 0.44, 0.010, LINE)
        field_lines(cv, x + 0.22, y + 0.88, w - 0.4, campos, size=8.6, step=0.215)

    cv.rect(M, 6.60, CW, 0.4, SOFT, LINE, radius=0.14)
    cv.text(M + 0.2, 6.60, CW - 0.4, 0.4,
            runs=[dict(t="7 enums do domínio  ", color=INK, bold=True, size=8),
                  dict(t="EspecieEnum · PorteEnum · ServicoEnum · StatusAgendamentoEnum · "
                         "CategoriaProdutoEnum · TipoMovimentacaoEnum · PerfilEnum",
                       color=MUTED, size=7.8)],
            valign="m", spacing=1.0)

    add(cv, "Entidades", HELEN, notes=(
        "Este é o coração do projeto: seis entidades que cobrem todo o domínio de um pet shop.\n"
        "Cliente é o tutor. Pet está sempre vinculado a um cliente — a chave estrangeira é "
        "obrigatória. Agendamento amarra cliente, pet, serviço, data e hora, e guarda o valor "
        "e a duração calculados a partir do serviço, não digitados pelo usuário.\n"
        "Produto controla o estoque com quantidade e estoque mínimo, e MovimentacaoEstoque "
        "guarda o histórico de cada entrada e saída. Por último, Usuario, que cuida do acesso "
        "ao painel com senha em bcrypt.\n"
        "Repare que os campos que só podem ter alguns valores viraram enums — espécie, porte, "
        "serviço, status, categoria, tipo de movimentação e perfil. Isso evita status escrito "
        "errado no banco e faz o Swagger listar as opções automaticamente."))


# ============================================================== slide 05 =====
def s05_relacionamentos():
    cv = Canvas()
    shell(cv, "Modelos e entidades", HELEN, 5)
    head(cv, "Relacionamentos",
         "As ligações e as regras que elas protegem",
         "Um relacionamento bem mapeado é o que permite bloquear exclusões indevidas e impedir dois banhos no mesmo horário.")

    cv.rect(M, 2.28, 7.7, 3.72, WHITE, LINE, radius=0.2)
    cv.text(M + 0.26, 2.44, 5.0, 0.22, "MAPA DE RELACIONAMENTOS", size=7.6, bold=True,
            color=MUTED_2, spacing=1.0)

    ligacoes = [
        ("Cliente", "Pet", "1:N", MINT_SOFT,
         "Todo pet pertence a um tutor. Excluir cliente com pet vinculado devolve 409."),
        ("Pet · Cliente", "Agendamento", "1:N", PINK_SOFT,
         "O agendamento guarda tutor e pet; o serviço define valor e duração."),
        ("Produto", "MovimentacaoEstoque", "1:N", PEACH_SOFT,
         "Cada entrada ou saída gera um registro histórico com data e observação."),
    ]
    for i, (a, b, card, tint, texto) in enumerate(ligacoes):
        y = 2.80 + i * 1.02
        cv.rect(M + 0.26, y, 1.42, 0.5, tint, None, radius=0.1)
        cv.text(M + 0.26, y, 1.42, 0.5, a, size=8.6, bold=True, color=INK,
                align="c", valign="m", spacing=1.0)
        cv.arrow(M + 1.76, y + 0.14, 0.5, 0.22)
        cv.text(M + 1.74, y - 0.19, 0.55, 0.18, card, size=7.2, bold=True,
                color=PINK_TEXT, align="c", spacing=1.0)
        cv.rect(M + 2.34, y, 1.72, 0.5, tint, None, radius=0.1)
        cv.text(M + 2.34, y, 1.72, 0.5, b, size=8.2, bold=True, color=INK,
                align="c", valign="m", spacing=1.0)
        cv.text(M + 4.20, y - 0.02, 3.18, 0.64, texto, size=8.6, color=MUTED,
                spacing=1.35)

    x2 = 8.42
    cv.rect(x2, 2.28, 4.36, 2.22, WHITE, LINE, radius=0.2)
    cv.text(x2 + 0.24, 2.44, 3.9, 0.22, "ENUMS: TEXTO LEGÍVEL NO BANCO", size=7.6,
            bold=True, color=MUTED_2, spacing=1.0)
    enums = [("EspecieEnum", "CACHORRO · GATO · AVE · ROEDOR"),
             ("ServicoEnum", "BANHO · TOSA · CONSULTA…"),
             ("StatusAgendamentoEnum", "AGENDADO · CONFIRMADO · REALIZADO"),
             ("Outros enums", "categoria · perfil · tipo mov.")]
    for i, (nome, vals) in enumerate(enums):
        y = 2.74 + i * 0.34
        cv.text(x2 + 0.24, y, 1.72, 0.2, nome, size=7.8, bold=True, color=INK,
                font="m", spacing=1.0)
        cv.text(x2 + 1.96, y, 2.2, 0.2, vals, size=7.4, color=MUTED, spacing=1.0)
    cv.text(x2 + 0.24, 4.06, 3.95, 0.2,
            runs=[dict(t="@Enumerated(EnumType.STRING)", color=ANN, font="m", size=7.4),
                  dict(t="  grava o nome", color=MUTED, size=7.4)],
            spacing=1.0)

    cv.rect(x2, 4.66, 4.36, 1.32, MINT_SOFT, None, radius=0.18)
    cv.text(x2 + 0.24, 4.78, 3.9, 0.24, "Integridade referencial (RNF-09)", size=9.6,
            bold=True, color=MINT_TEXT, spacing=1.0)
    bullets(cv, x2 + 0.24, 5.06, 3.85,
            ["ClienteService bloqueia exclusão com pets",
             "PetService bloqueia com agendamento futuro",
             "Produto com histórico sugere inativar"],
            size=8.2, gap=0.3, dot=MINT)

    cv.rect(x2, 6.10, 4.36, 0.52, PINK_SOFT, None, radius=0.16)
    cv.text(x2 + 0.24, 6.10, 3.9, 0.52,
            runs=[dict(t="Status novo? ", color=PINK_TEXT, bold=True, size=8.2),
                  dict(t="vira valor de enum, não texto solto.", color=PLN, size=8.2)],
            valign="m", spacing=1.0)

    add(cv, "Relacionamentos", HELEN, notes=(
        "Aqui estão as três ligações principais. Cliente para pet é um para muitos: um tutor "
        "pode ter vários pets, mas cada pet tem um tutor. Agendamento aponta para o cliente e "
        "para o pet ao mesmo tempo, porque na tela a gente precisa mostrar os dois.\n"
        "Esses vínculos não são só desenho: eles viraram regra. O ClienteService consulta se "
        "o cliente tem pets antes de excluir; o PetService checa se existe agendamento "
        "futuro. Se existir, a API devolve 409 com uma mensagem explicando o motivo, em vez "
        "de quebrar o banco.\n"
        "E os enums são gravados como texto — @Enumerated STRING. Isso deixa o banco legível "
        "quando abrimos o console do H2, e qualquer valor inválido nem compila."))


# ============================================================== slide 06 =====
def s06_codigo():
    cv = Canvas()
    shell(cv, "Modelos e entidades", HELEN, 6)
    head(cv, "No código", "A entidade Pet, linha por linha", None)

    rows = [
        [("@Schema(", ANN), ("description = \"Pet vinculado a um cliente\"", STR), (")", ANN)],
        [("@Entity", ANN)],
        [("@Table(", ANN), ("name = \"pet\"", STR), (")", ANN)],
        [("public class ", KW), ("Pet", TYP), (" {", PLN)],
        [],
        [("    @Id", ANN)],
        [("    @GeneratedValue", ANN), ("(strategy = IDENTITY)", PLN)],
        [("    private ", KW), ("Long", TYP), (" id;", PLN)],
        [],
        [("    @ManyToOne", ANN), ("(optional = false)", PLN)],
        [("    @JoinColumn", ANN), ("(name = \"fk_cliente\")", STR)],
        [("    private ", KW), ("Cliente", TYP), (" cliente;      ", PLN),
         ("// tutor obrigatório", CMT)],
        [],
        [("    @Enumerated", ANN), ("(EnumType.STRING)", PLN)],
        [("    @Column", ANN), ("(nullable = false, length = 20)", PLN)],
        [("    private ", KW), ("EspecieEnum", TYP), (" especie;", PLN)],
        [],
        [("    @Column", ANN), ("(nullable = false)", PLN)],
        [("    private ", KW), ("Integer", TYP), (" idade;        ", PLN),
         ("// 0 a 40 no DTO", CMT)],
        [("}", PLN)],
    ]
    code_card(cv, M, 2.05, 7.35, 4.70, rows, size=8.2, step=0.19,
              label="model/Pet.java",
              head=("Uma entidade, três decisões: ",
                    "tabela, chave estrangeira e enum como texto."))

    x2 = 8.08
    notas = [
        ("@Entity + @Table", MINT_TEXT,
         "A classe vira tabela e o nome é fixado — o console do H2 mostra exatamente `pet`."),
        ("@ManyToOne + @JoinColumn", PINK_TEXT,
         "optional = false cria a FK `fk_cliente` NOT NULL: pet sem tutor não é salvo."),
        ("@Enumerated(EnumType.STRING)", PEACH_TEXT,
         "Grava o nome do enum, não o número. Banco legível e seguro contra reordenação."),
        ("@Schema", MUTED,
         "Descrição e exemplo de cada campo aparecem na documentação do Swagger."),
    ]
    for i, (titulo, cor, texto) in enumerate(notas):
        y = 2.05 + i * 1.20
        cv.rect(x2, y, 4.7, 1.14, WHITE, LINE, radius=0.16)
        cv.rect(x2, y + 0.14, 0.075, 0.86, cor, None, radius=0.03)
        cv.text(x2 + 0.26, y + 0.16, 4.2, 0.22, titulo, size=9, bold=True,
                color=cor, font="m", spacing=1.0)
        cv.text(x2 + 0.26, y + 0.44, 4.24, 0.62, texto, size=8.4, color=MUTED,
                spacing=1.3)

    add(cv, "Código da entidade", HELEN, notes=(
        "Para fechar meu bloco, um pedaço real do código, sem simplificação.\n"
        "Em quatro linhas a gente tem o essencial: a classe vira tabela, o cliente vira chave "
        "estrangeira obrigatória, a espécie é um enum gravado como texto e cada campo tem uma "
        "descrição que aparece no Swagger.\n"
        "Uma decisão importante: a validação de faixa, tipo idade entre 0 e 40, fica no DTO, "
        "não na entidade. A entidade representa o dado; o DTO representa o que o usuário pode "
        "enviar. Com isso eu passo a palavra para o Gabriel falar do banco."))


# ============================================================== divisor ======
def divisor(numero, nome, img, tema, itens, cor_fundo, cor_principal, cor_suave,
            proximo):
    cv = Canvas(bg=cor_fundo)
    cv.circle(9.6, 1.1, 5.4, 5.4, fill=cor_suave, line=None)
    cv.circle(11.9, 5.6, 1.9, 1.9, fill=WHITE, line=None)

    cv.rect(M, 0.62, 3.4, 0.10, blend(cor_principal, 0.35), None, radius=0.05)
    cv.rect(M, 0.62, 3.4 * numero / 3, 0.10, cor_principal, None, radius=0.05)

    cv.text(M, 1.06, 6.0, 0.26, f"BLOCO {numero:02d}", size=9, bold=True,
            color=blend(cor_principal, 0.6), spacing=1.0)
    cv.text(M, 1.36, 2.6, 1.5, f"{numero:02d}", size=104, bold=True,
            color=blend(cor_principal, 0.32), spacing=0.95)
    cv.text(M + 2.5, 2.06, 6.2, 0.75, nome, size=30, bold=True, color=INK, spacing=1.05)
    cv.text(M + 2.52, 2.86, 5.6, 0.34, tema, size=13, bold=True,
            color=blend(cor_principal, 0.62), spacing=1.1)
    cv.line(M, 3.42, 6.9, 0.014, blend(cor_principal, 0.3))

    y = 3.62
    for item in itens:
        cv.circle(M + 0.02, y + 0.1, 0.08, 0.08, cor_principal, None)
        cv.text(M + 0.28, y, 6.5, 0.3, item, size=10.6, color=PLN, spacing=1.0)
        y += 0.44

    avatar(cv, 9.35, 2.36, 2.5, img, WHITE)
    cv.text(9.1, 5.16, 3.0, 0.26, "apresenta agora", size=8.4, color=MUTED,
            align="c", spacing=1.0)
    cv.text(8.5, 5.42, 4.2, 0.3, nome, size=12.5, bold=True, color=INK, align="c",
            spacing=1.0)
    cv.text(M, 6.36, 8.2, 0.26, proximo, size=9, color=MUTED, spacing=1.0)
    add(cv, f"Bloco {numero:02d}", nome, notes="")


def s07_divisor_gabriel():
    divisor(2, GABRIEL, "CachorroGab.png", "Banco de dados e Repositories",
            ["Por que H2 em memória — e o que ele resolve",
             "Console do banco e carga inicial com data.sql",
             "Repositories: o CRUD pronto do Spring Data",
             "HQL, SQL nativo e projections"],
            MINT_SOFT, MINT, blend(MINT, 0.45),
            "Em seguida: Banco de Dados  →  Repositories  →  Consultas")
    SLIDES[-1]["notes"] = (
        "Obrigado, Helen. Meu bloco é o que fica embaixo da API: onde os dados realmente "
        "moram. Vou mostrar o banco H2, como ele é configurado, a carga inicial de dados e "
        "depois os repositories — incluindo as consultas que escrevemos na mão.")


def s08_divisor_joao():
    divisor(3, JOAO, "Hamster Lu.png", "Swagger, CRUD e endpoints especializados",
            ["Documentação gerada a partir do código",
             "Testar a API pelo navegador, com sessão",
             "As quatro operações CRUD e seus status",
             "Filtros, conflitos e consultas de negócio"],
            PINK_SOFT, PINK, blend(PINK, 0.4),
            "Em seguida: Swagger/OpenAPI  →  CRUD  →  Endpoints especializados")
    SLIDES[-1]["notes"] = (
        "Boa, Gabriel. Eu fecho mostrando a parte que dá para ver funcionando: a "
        "documentação no Swagger, o CRUD completo e os endpoints que carregam as regras de "
        "negócio do PetClean.")


# ============================================================== slide 08 =====
def s09_h2():
    cv = Canvas()
    shell(cv, "Banco de dados", GABRIEL, 8)
    head(cv, "Banco de Dados", "H2 em memória: leve, rápido e descartável")

    rows = [
        [("# H2 em memoria — sobe junto com a aplicacao", CMT)],
        [("spring.datasource.url", PLN), ("=jdbc:h2:mem:petcleandb", STR)],
        [("spring.datasource.username", PLN), ("=sa", STR)],
        [("spring.datasource.password", PLN), ("=", STR)],
        [],
        [("# Console web: localhost:8080/h2-console", CMT)],
        [("spring.h2.console.enabled", PLN), ("=true", KW)],
        [],
        [("# Hibernate cria as tabelas a cada subida", CMT)],
        [("spring.jpa.hibernate.ddl-auto", PLN), ("=create", KW)],
        [("spring.jpa.defer-datasource-initialization", PLN), ("=true", KW)],
        [("spring.sql.init.mode", PLN), ("=always", KW)],
        [("spring.sql.init.encoding", PLN), ("=UTF-8", STR)],
    ]
    code_card(cv, M, 1.92, 6.15, 2.66, rows, size=7.8, step=0.16,
              label="application.properties",
              head=("Tudo em um arquivo: ", "URL, console, schema e carga inicial."))

    stats = [("6", "tabelas criadas"), ("71", "INSERTs no data.sql"),
             ("/h2-console", "console web liberado"), ("create", "schema a cada start")]
    w = 2.9
    for i, (big, small) in enumerate(stats):
        x = 6.94 + (i % 2) * (w + 0.18)
        y = 1.92 + (i // 2) * 1.32
        cv.rect(x, y, w, 1.2, WHITE, LINE, radius=0.16)
        cv.text(x + 0.24, y + 0.22, w - 0.4, 0.36, big, size=17, bold=True,
                color=PINK_TEXT if i == 3 else INK, spacing=1.0)
        cv.text(x + 0.24, y + 0.68, w - 0.4, 0.24, small, size=8.2, color=MUTED,
                spacing=1.0)

    cv.rect(M, 4.74, CW, 2.12, WHITE, LINE, radius=0.2)
    cv.text(M + 0.28, 4.88, 6.0, 0.24, "Registros da carga inicial, por tabela", size=9.6,
            bold=True, color=INK, spacing=1.0)
    cv.text(RIGHT - 3.0, 4.90, 2.7, 0.22, "data.sql", size=7.6, color=MUTED_2,
            align="r", font="m", spacing=1.0)

    dados = [("cliente", 8), ("pet", 10), ("agendamento", 24), ("produto", 10),
             ("movimentacao", 15), ("usuario", 4)]
    base, topo, escala = 6.52, 1.02, 24.0
    cv.line(M + 0.3, base, CW - 0.6, 0.010, LINE)
    for i, (nome, valor) in enumerate(dados):
        bw = 0.86
        x = M + 0.55 + i * 1.95
        hh = max(0.1, valor / escala * topo)
        cv.rect(x, base - hh, bw, hh, MINT if i % 2 == 0 else blend(MINT, 0.72),
                None, radius=0.1)
        cv.text(x - 0.2, base - hh - 0.26, bw + 0.4, 0.22, str(valor), size=8.6,
                bold=True, color=INK, align="c", spacing=1.0)
        cv.text(x - 0.35, base + 0.08, bw + 0.7, 0.22, nome, size=7.6, color=MUTED,
                align="c", spacing=1.0)
    cv.text(RIGHT - 2.4, 5.94, 2.1, 0.22,
            runs=[dict(t="6 tabelas · 71 registros", color=MUTED_2, size=7.6)],
            align="r", spacing=1.0)

    add(cv, "Banco H2", GABRIEL, notes=(
        "O enunciado permitia usar o H2, e a gente escolheu justamente por ser em memória: "
        "o projeto sobe, cria as tabelas e carrega os dados de demonstração sozinho. Ninguém "
        "precisa instalar MySQL para rodar na sua máquina.\n"
        "São quatro linhas de configuração que importam: a URL jdbc:h2:mem:petcleandb, o "
        "console habilitado em /h2-console, o ddl-auto create — que recria o schema a cada "
        "subida — e o defer-datasource-initialization com sql.init.mode always, que garante "
        "que o data.sql rode depois do Hibernate criar as tabelas.\n"
        "O data.sql tem 71 inserts: 8 clientes, 10 pets, 24 agendamentos, 10 produtos, 15 "
        "movimentações e 4 usuários. As datas dos agendamentos são relativas, com DATEADD, "
        "para o dashboard nunca aparecer vazio, independentemente do dia da apresentação.\n"
        "E como é em memória, ao parar a aplicação tudo é descartado — o que é ótimo para "
        "demonstração: cada ./mvnw spring-boot:run começa de um estado conhecido."))


# ============================================================== slide 09 =====
def s10_repositories():
    cv = Canvas()
    shell(cv, "Repositories", GABRIEL, 9)
    head(cv, "Repositories",
         "Spring Data JPA: o CRUD vem de graça",
         "Basta estender JpaRepository<Entidade, Long> — findAll, findById, save e deleteById já existem, sem uma linha de implementação.")

    rows = [
        [("public interface ", KW), ("PetRepository", TYP),
         (" extends ", KW), ("JpaRepository", TYP), ("<", PLN), ("Pet", TYP),
         (", ", PLN), ("Long", TYP), ("> {", PLN)],
        [],
        [("    // consulted by name: o Spring monta o SQL", CMT)],
        [("    List<Pet> ", PLN), ("findByClienteIdOrderByNome", FN),
         ("(Long idCliente);", PLN)],
        [],
        [("    long ", PLN), ("countByClienteId", FN), ("(Long idCliente);", PLN)],
        [],
        [("    // HQL: filtro por nome do pet ou do tutor", CMT)],
        [("    @Query", ANN), ("(\"from Pet p where lower(p.nome) like ...\")", STR)],
        [("    List<Pet> ", PLN), ("filtrarPorNomePetOuTutor", FN),
         ("(@Param(\"termo\") String termo);", PLN)],
        [],
        [("    // SQL nativo + projection (US-08)", CMT)],
        [("    @Query", ANN), ("(nativeQuery = true, value = \"select ...\")", STR)],
        [("    List<PetResumoProjection> ", PLN), ("filtrarResumo", FN),
         ("(@Param(\"termo\") String termo);", PLN)],
        [("}", PLN)],
    ]
    code_card(cv, M, 2.26, 7.1, 4.42, rows, size=7.9, step=0.255,
              label="repository/PetRepository.java",
              head=("Nome do método = consulta. ", "E quando não basta, @Query."))

    x2 = 7.9
    cv.rect(x2, 2.26, 4.88, 1.94, WHITE, LINE, radius=0.18)
    cv.text(x2 + 0.24, 2.38, 4.4, 0.22, "6 INTERFACES, ZERO IMPLEMENTAÇÃO", size=7.4,
            bold=True, color=MUTED_2, spacing=1.0)
    repos = ["ClienteRepository", "PetRepository", "AgendamentoRepository",
             "ProdutoRepository", "MovimentacaoEstoqueRepository", "UsuarioRepository"]
    for i, r in enumerate(repos):
        y = 2.66 + i * 0.235
        cv.circle(x2 + 0.28, y + 0.055, 0.07, 0.07, PINK, None)
        cv.text(x2 + 0.44, y, 4.2, 0.2, r, size=7.8, color=PLN, font="m", spacing=1.0)
        cv.text(x2 + 3.5, y, 1.2, 0.2, "JpaRepository", size=7, color=MUTED_2,
                align="r", font="m", spacing=1.0)

    cv.rect(x2, 4.36, 4.88, 1.20, MINT_SOFT, None, radius=0.16)
    cv.text(x2 + 0.24, 4.48, 4.4, 0.22, "Query methods: o nome é a consulta", size=9,
            bold=True, color=MINT_TEXT, spacing=1.0)
    cv.text(x2 + 0.24, 4.74, 4.4, 0.72,
            runs=[dict(t="existsByCpf", color=ANN, font="m", size=7.6),
                  dict(t="  →  gera o SELECT de duplicidade\n", color=PLN, size=7.6),
                  dict(t="contarPendentesDoDia", color=ANN, font="m", size=7.6),
                  dict(t="  →  agendamentos do dia", color=PLN, size=7.6)],
            spacing=1.35)

    cv.rect(x2, 5.70, 4.88, 0.98, PINK_SOFT, None, radius=0.16)
    cv.text(x2 + 0.24, 5.80, 4.4, 0.22, "Quando o nome não basta: @Query", size=9,
            bold=True, color=PINK_TEXT, spacing=1.0)
    cv.text(x2 + 0.24, 6.06, 4.4, 0.56,
            "Filtros com like, conflito de horário e agregações do dashboard são "
            "escritos em HQL ou SQL nativo dentro do repository.",
            size=7.8, color=PLN, spacing=1.3)

    add(cv, "Repositories", GABRIEL, notes=(
        "O Spring Data JPA resolve a maior parte do trabalho pesado. As seis interfaces "
        "estendem JpaRepository e, só com isso, cada entidade já tem findAll, findById, "
        "save, deleteById e paginação. Não existe classe de implementação no projeto — o "
        "Spring gera o proxy em tempo de execução.\n"
        "Quando o método padrão não serve, a gente desce um nível. Primeiro os query "
        "methods: o nome do método é a consulta. findByClienteIdOrderByNome quer dizer "
        "'busque por id do cliente, ordenado por nome'. existsByCpf resolve a duplicidade "
        "de CPF, countByClienteId conta os pets do tutor.\n"
        "E quando a consulta é mais complexa — filtro com like, contagem de conflito de "
        "horário, agregação por mês — a gente escreve com @Query, em HQL ou SQL nativo. "
        "Isso me leva ao próximo slide."))


# ============================================================== slide 10 =====
def s11_queries():
    cv = Canvas()
    shell(cv, "Repositories", GABRIEL, 10)
    head(cv, "Consultas especializadas",
         "HQL, SQL nativo e projections",
         "A mesma busca tem duas versões: a que devolve a entidade completa e a que devolve apenas três colunas.")

    rows_hql = [
        [("// HQL: filtra por nome do pet ou do tutor (US-08)", CMT)],
        [("@Query", ANN), ("(\"from Pet p where \"", STR)],
        [("       + \"lower(p.nome) like lower(concat('%', :termo, '%')) \"", STR)],
        [("       + \"or lower(p.cliente.nome) like lower(concat('%', :termo, '%')) \"", STR)],
        [("       + \"order by p.nome\")", STR)],
        [("List<Pet> ", PLN), ("filtrarPorNomePetOuTutor", FN),
         ("(@Param(\"termo\") String termo);", PLN)],
    ]
    code_card(cv, M, 2.22, 5.98, 2.5, rows_hql, size=7.6, step=0.3,
              label="HQL — entidade completa")

    rows_sql = [
        [("// SQL nativo + projection = 3 colunas (US-08)", CMT)],
        [("@Query", ANN), ("(nativeQuery = true, value =", STR)],
        [("   \"select p.nome pet, cast(p.especie as varchar) especie, \"", STR)],
        [(" + \"c.nome tutor from pet p inner join cliente c \"", STR)],
        [(" + \"on (p.fk_cliente = c.id) where lower(p.nome) like ...\")", STR)],
        [("List<PetResumoProjection> ", PLN), ("filtrarResumo", FN),
         ("(@Param(\"termo\") String termo);", PLN)],
    ]
    code_card(cv, M + 6.25, 2.22, 5.98, 2.5, rows_sql, size=7.6, step=0.3,
              label="SQL nativo — projection")

    cv.rect(M, 4.92, 7.15, 1.92, WHITE, LINE, radius=0.18)
    cv.text(M + 0.24, 5.02, 5.0, 0.22, "Resposta de GET /api/pets/resumo?termo=thor",
            size=8.6, bold=True, color=INK, spacing=1.0)
    cols = [("pet", 0.24, 1.5), ("especie", 2.0, 1.6), ("tutor", 3.7, 2.6)]
    for nome, dx, ww in cols:
        cv.text(M + 0.24 + dx, 5.34, ww, 0.2, nome, size=7.4, bold=True,
                color=MUTED_2, spacing=1.0)
    cv.line(M + 0.24, 5.56, 6.7, 0.010, LINE)
    for i, (pet, esp, tutor) in enumerate([("Thor", "CACHORRO", "Maria da Silva"),
                                           ("Pipoca", "AVE", "Fernando Lima"),
                                           ("Bidu", "CACHORRO", "Patricia Nogueira")]):
        y = 5.62 + i * 0.24
        cv.text(M + 0.24, y, 1.5, 0.2, pet, size=7.8, bold=True, color=INK, spacing=1.0)
        cv.text(M + 2.0, y, 1.6, 0.2, esp, size=7.6, color=MINT_TEXT, font="m",
                spacing=1.0)
        cv.text(M + 3.7, y, 2.9, 0.2, tutor, size=7.6, color=MUTED, spacing=1.0)

    x2 = M + 7.42
    cv.rect(x2, 4.92, 4.81, 1.92, MINT_SOFT, None, radius=0.18)
    cv.text(x2 + 0.24, 5.04, 4.3, 0.24, "Por que projection vale a pena", size=9.2,
            bold=True, color=MINT_TEXT, spacing=1.0)
    bullets(cv, x2 + 0.24, 5.34, 4.3,
            ["Traz 3 colunas em vez de ~20",
             "Não hidrata entidade nem abre transação",
             "A listagem do painel fica mais leve"],
            size=8.2, gap=0.3, dot=MINT)

    cv.rect(M, 6.30, 5.72, 0.62, SOFT, LINE, radius=0.15)
    cv.text(M + 0.22, 6.30, 5.4, 0.62,
            runs=[dict(t="5 projections", color=INK, bold=True, size=8),
                  dict(t="  ·  Cliente, Pet, Agendamento, Dia, Produto",
                       color=MUTED, size=8)],
            valign="m", spacing=1.1)

    cv.rect(M + 7.42, 6.30, 4.81, 0.62, PEACH_SOFT, None, radius=0.15)
    cv.text(M + 7.64, 6.30, 4.4, 0.62,
            runs=[dict(t="ORDER BY na consulta", color=PEACH_TEXT, bold=True, size=7.6),
                  dict(t="  — o estoque já vem ordenado pelo banco", color=PLN, size=7.6)],
            valign="m", spacing=1.1)

    add(cv, "Consultas", GABRIEL, notes=(
        "Essa dupla de métodos mostra bem a evolução. A primeira consulta é HQL e devolve a "
        "entidade Pet inteira, com todos os relacionamentos. É o que a tela de edição "
        "precisa.\n"
        "A segunda é SQL nativo com projection: um select que traz só nome, espécie e nome "
        "do tutor. A interface PetResumoProjection é uma interface com três getters, e o "
        "Spring preenche direto — não existe classe, não existe mapeamento manual.\n"
        "Isso importa porque a listagem de pets aparece no dashboard e precisa ser leve. "
        "Volume de dados baixo aqui, mas o hábito é o que vale: busque só o que a tela "
        "mostra.\n"
        "Tem ainda um detalhe de regra: o estoque crítico já vem ordenado pelo banco, do "
        "maior déficit para o menor. A ordenação é decisão de negócio, então mora na "
        "consulta, não no JavaScript."))


# ============================================================== slide 12 =====
def s12_swagger():
    cv = Canvas()
    shell(cv, "Swagger / OpenAPI", JOAO, 12)
    head(cv, "Swagger / OpenAPI",
         "Documentação que também é ferramenta de teste",
         "O springdoc lê os controllers e gera a especificação OpenAPI em /api-docs.")

    rows = [
        [("@Configuration", ANN)],
        [("public class ", KW), ("SwaggerConfig", TYP), (" {", PLN)],
        [],
        [("  @Bean OpenAPI configurarSwagger() {", PLN)],
        [("    final String esquema = \"sessaoPetClean\";", PLN)],
        [],
        [("    return new ", KW), ("OpenAPI", TYP), ("()", PLN)],
        [("      .info(", PLN), ("new ", KW), ("Info", TYP), ("()", PLN)],
        [("        .title(\"PetClean — API de Gestao para Pet Shops\")", STR)],
        [("        .version(\"1.0\"))", PLN)],
        [("      .addSecurityItem(", PLN), ("new ", KW), ("SecurityRequirement", TYP)],
        [("        .addList(esquema))", PLN)],
        [("      .components(", PLN), ("new ", KW), ("Components", TYP)],
        [("        .addSecuritySchemes(esquema,", PLN)],
        [("          new ", KW), ("SecurityScheme", TYP), ("()", PLN)],
        [("            .name(\"PETCLEANSESSION\")", STR)],
        [("            .type(APIKEY).in(COOKIE))));", PLN)],
        [("  }", PLN)],
        [("}", PLN)],
    ]
    code_card(cv, M, 2.26, 6.55, 4.32, rows, size=7.6, step=0.185,
              label="swagger/SwaggerConfig.java",
              head=("Uma classe só: ", "título, versão e o cookie de sessão."))

    x2 = 7.4
    cv.rect(x2, 2.26, 5.38, 3.32, WHITE, LINE, radius=0.18)
    cv.rect(x2, 2.26, 5.38, 0.4, SOFT, None, radius=0.18)
    for i, cor in enumerate([PINK, PEACH, MINT]):
        cv.circle(x2 + 0.22 + i * 0.17, 2.4, 0.09, 0.09, cor, None)
    cv.text(x2 + 0.82, 2.34, 3.0, 0.24,
            runs=[dict(t="localhost:8080", color=MUTED, font="m", size=7.6),
                  dict(t="/swagger-ui.html", color=PINK_TEXT, font="m", size=7.6)],
            spacing=1.0)

    tags = [("01 - Clientes", "6 endpoints", MINT_SOFT, MINT_TEXT),
            ("02 - Pets", "7 endpoints", MINT_SOFT, MINT_TEXT),
            ("03 - Agendamentos", "8 endpoints", PINK_SOFT, PINK_TEXT),
            ("04 - Estoque", "10 endpoints", PEACH_SOFT, PEACH_TEXT),
            ("05 - Dashboard", "2 endpoints", "EEF3FB", "3B5C8A"),
            ("06 - Autenticação", "4 endpoints", "F2F0FB", "5B4B9A"),
            ("07 - Catálogos", "6 endpoints", SOFT, MUTED)]
    for i, (tag, qtd, tint, cor) in enumerate(tags):
        y = 2.78 + i * 0.385
        cv.rect(x2 + 0.2, y, 4.98, 0.33, tint, None, radius=0.09)
        cv.text(x2 + 0.34, y, 3.3, 0.33, tag, size=7.8, bold=True, color=cor,
                valign="m", spacing=1.0)
        cv.text(x2 + 3.0, y, 2.05, 0.33, qtd, size=7.4, color=cor, align="r",
                valign="m", spacing=1.0)

    cv.rect(x2, 5.68, 5.38, 0.98, MINT_SOFT, None, radius=0.16)
    cv.text(x2 + 0.24, 5.77, 4.9, 0.22, "Testar rota protegida no próprio Swagger",
            size=9, bold=True, color=MINT_TEXT, spacing=1.0)
    for k, passo in enumerate(["POST /login com e-mail e senha",
                               "O cookie PETCLEANSESSION fica no navegador",
                               "Authorize e as rotas protegidas respondem"]):
        yy = 6.02 + k * 0.20
        cv.circle(x2 + 0.26, yy + 0.02, 0.155, 0.155, WHITE, None)
        cv.text(x2 + 0.26, yy + 0.02, 0.155, 0.155, str(k + 1), size=6.4, bold=True,
                color=MINT_TEXT, align="c", valign="m", spacing=1.0)
        cv.text(x2 + 0.52, yy, 4.6, 0.2, passo, size=7.5, color=PLN, spacing=1.0)

    add(cv, "Swagger", JOAO, notes=(
        "Boa noite. Fecho o grupo mostrando o que o Swagger faz por nós.\n"
        "A configuração é uma classe só. O springdoc lê os controllers e gera a "
        "especificação OpenAPI automaticamente — quem escreve a documentação é o próprio "
        "código. É por isso que os @Operation e @Schema que a Helen mostrou fazem diferença: "
        "eles viram o texto que aparece aqui.\n"
        "A parte que a gente adicionou de propósito foi o esquema de segurança: a nossa "
        "autenticação é sessão por cookie, então o Swagger precisa saber que existe um "
        "cookie chamado PETCLEANSESSION. Sem isso, toda rota protegida responde 401 e não dá "
        "para testar nada.\n"
        "Na prática: abre /swagger-ui.html, executa o POST /login, o navegador guarda o "
        "cookie e a partir daí os endpoints de clientes, pets, agendamentos e estoque "
        "funcionam direto na tela, sem Postman. As tags numeradas organizam os endpoints "
        "por épico do projeto."))


# ============================================================== slide 13 =====
def s13_crud():
    cv = Canvas()
    shell(cv, "Operações CRUD", JOAO, 13)
    head(cv, "Operações CRUD",
         "As quatro operações, com os status certos",
         "Cada verbo HTTP devolve o código que o painel espera — e cada falha tem um código próprio.")

    ops = [
        ("POST", "/api/clientes", "201", "Created", MINT, MINT_TEXT,
         "Cria o cliente e devolve o Location do recurso."),
        ("GET", "/api/clientes?termo=maria", "200", "OK", "EEF3FB", "3B5C8A",
         "Lista, busca por id ou filtra por nome/CPF."),
        ("PUT", "/api/clientes/{id}", "200", "OK", PEACH_SOFT, PEACH_TEXT,
         "Atualiza o registro inteiro; CPF continua único."),
        ("DELETE", "/api/clientes/{id}", "204", "No Content", PINK_SOFT, PINK_TEXT,
         "Exclui sem corpo; com vínculo devolve 409."),
    ]
    for i, (verbo, rota, code, nome, tint, cor, texto) in enumerate(ops):
        y = 2.34 + i * 1.13
        cv.rect(M, y, 7.55, 1.0, WHITE, LINE, radius=0.16)
        cv.chip(M + 0.22, y + 0.3, verbo, size=7.6, fill=tint, color=cor,
                line=tint, h=0.34, bold=True)
        cv.text(M + 1.28, y + 0.18, 3.7, 0.24, rota, size=8.2, color=INK,
                font="m", spacing=1.0)
        cv.text(M + 1.28, y + 0.5, 4.3, 0.24, texto, size=7.9, color=MUTED,
                spacing=1.0)
        cv.text(M + 5.6, y + 0.16, 1.75, 0.3, code, size=14, bold=True, color=cor,
                align="r", spacing=1.0)
        cv.text(M + 5.6, y + 0.52, 1.75, 0.22, nome, size=7.2, color=MUTED,
                align="r", spacing=1.0)

    rows = [
        [("# criar", CMT)],
        [("curl -X POST localhost:8080/api/clientes \\", PLN)],
        [("  -H \"Content-Type: application/json\" \\", PLN)],
        [("  -d '{\"nome\":\"Maria da Silva\",", STR)],
        [("       \"cpf\":\"123.456.789-09\"}'", STR)],
        [],
        [("# movimentar estoque (PATCH especializado)", CMT)],
        [("curl -X PATCH localhost:8080/api/produtos/1/movimentar \\", PLN)],
        [("  -d '{\"tipo\":\"SAIDA\",\"quantidade\":2}'", STR)],
    ]
    code_card(cv, M + 7.82, 2.34, 4.41, 2.66, rows, size=7.2, step=0.225,
              label="curl", head=("Testando por linha de comando", ""))

    cv.rect(M + 7.82, 5.12, 4.41, 1.56, SOFT, LINE, radius=0.16)
    cv.text(M + 8.04, 5.24, 3.9, 0.22, "CÓDIGOS DE ERRO PADRONIZADOS", size=7.4,
            bold=True, color=MUTED_2, spacing=1.0)
    erros = [("400", "dados inválidos"), ("401", "sem sessão"),
             ("404", "não encontrado"), ("409", "conflito de negócio"),
             ("422", "arquivo grande")]
    for i, (code, desc) in enumerate(erros[:3]):
        y = 5.52 + i * 0.34
        cv.chip(M + 8.04, y, code, size=7.2, fill=WHITE, color=PINK_TEXT, h=0.28)
        cv.text(M + 8.72, y, 3.3, 0.28, desc, size=7.6, color=PLN, valign="m",
                spacing=1.0)
    for i, (code, desc) in enumerate(erros[3:]):
        y = 5.52 + i * 0.34
        cv.chip(M + 10.35, y, code, size=7.2, fill=WHITE, color=PINK_TEXT, h=0.28)
        cv.text(M + 11.03, y, 1.3, 0.28, desc, size=7.6, color=PLN, valign="m",
                spacing=1.0)

    add(cv, "CRUD", JOAO, notes=(
        "Sobre o CRUD: as quatro operações existem para todas as entidades principais, "
        "então são 48 endpoints no total. O que importa aqui é que cada uma "
        "devolve o status correto.\n"
        "POST devolve 201 com o Location do recurso criado — não 200. DELETE devolve 204, "
        "sem corpo. E o DELETE do cliente é o exemplo perfeito de regra de negócio no CRUD: "
        "se o cliente tem pet ou agendamento, ele não apaga, devolve 409 e explica o motivo. "
        "Produto é parecido: com histórico de movimentação, o certo é inativar em vez de "
        "excluir, e existe um PATCH específico para isso.\n"
        "Os erros também são padronizados pelo GlobalExceptionHandler: 400 para corpo "
        "inválido, 401 quando não tem sessão, 404 quando o id não existe, 409 para conflito "
        "e 422 para regra não atendida, como a foto acima de 2 MB."))


# ============================================================== slide 14 =====
def s14_especializados():
    cv = Canvas()
    shell(cv, "Endpoints especializados", JOAO, 14)
    head(cv, "Endpoints especializados",
         "Onde a regra de negócio aparece na URL")

    cards = [
        ("Busca parametrizada", "GET", "/api/clientes?termo=", MINT_SOFT, MINT_TEXT,
         "Filtra por nome ou CPF sem diferenciar maiúsculas. A tela de clientes usa em tempo real."),
        ("Filtros combinados", "GET", "/api/produtos?termo=&categoria=", MINT_SOFT,
         MINT_TEXT, "Nome e categoria na mesma consulta — é a busca do estoque."),
        ("Agenda do dia", "GET", "/api/agendamentos/agenda?data=", "EEF3FB", "3B5C8A",
         "Volta em projection com tutor, pet, serviço e horário, já ordenado."),
        ("Conflito de horário", "POST", "/api/agendamentos", PINK_SOFT, PINK_TEXT,
         "Mesmo dia e horário ativos → 409 e nada é gravado. É a regra mais testada."),
        ("Estoque crítico", "GET", "/api/produtos/estoque-critico", PEACH_SOFT,
         PEACH_TEXT, "quantidade ≤ mínimo, do maior déficit para o menor."),
        ("Dashboard analítico", "GET", "/api/dashboard?periodo=semanal", "F2F0FB",
         "5B4B9A", "KPIs + gráfico de 8 semanas ou 6 meses, com períodos vazios zerados."),
    ]
    w, h, gx, gy = 3.85, 1.94, 0.34, 0.24
    for i, (titulo, verbo, rota, tint, cor, texto) in enumerate(cards):
        x = M + (i % 3) * (w + gx)
        y = 1.92 + (i // 3) * (h + gy)
        cv.rect(x, y, w, h, WHITE, LINE, radius=0.18)
        cv.rect(x, y, w, 0.08, cor, None, radius=0.04)
        cv.text(x + 0.24, y + 0.22, w - 0.5, 0.24, titulo, size=10.4, bold=True,
                color=INK, spacing=1.0)
        cv.chip(x + 0.24, y + 0.56, verbo, size=6.8, fill=tint, color=cor, line=tint,
                h=0.26, bold=True)
        cv.text(x + 1.02, y + 0.56, w - 1.22, 0.26, rota, size=6.9, color=PLN,
                font="m", valign="m", spacing=1.0)
        cv.text(x + 0.24, y + 0.96, w - 0.48, 0.8, texto, size=9.2, color=PLN,
                spacing=1.4)

    cv.rect(M, 6.06, CW, 0.68, MINT_SOFT, None, radius=0.16)
    cv.text(M + 0.26, 6.06, CW - 0.5, 0.68,
            runs=[dict(t="48 endpoints  ", color=MINT_TEXT, bold=True, size=9),
                  dict(t="43 nas 7 tags de domínio + 5 do perfil  ·  "
                         "US-04, US-08, US-12, US-17, US-20, US-23, US-24, US-25",
                       color=PLN, size=9)],
            valign="m", spacing=1.0)

    add(cv, "Especializados", JOAO, notes=(
        "O último requisito era o que mais gostei de fazer: endpoints que não são CRUD, "
        "que existem por causa de uma regra do PetClean.\n"
        "Alguns são consultas: busca por termo em clientes, filtro combinado de nome e "
        "categoria no estoque, agenda do dia. Outros são operações que só fazem sentido no "
        "nosso domínio: o conflito de horário, que impede dois banhos no mesmo horário e "
        "devolve 409 sem gravar nada; o estoque crítico já ordenado pelo déficit; e o "
        "dashboard, que devolve os KPIs e o gráfico de oito semanas ou seis meses.\n"
        "Cada um desses endpoints corresponde a uma história de usuário do relatório. Dá "
        "para rastrear: a US-17 é o conflito, a US-20 é o alerta de estoque crítico, a "
        "US-23 é o gráfico por período."))


# ============================================================== slide 15 =====
def s15_fechamento():
    cv = Canvas(bg=CREAM)
    cv.circle(10.4, -0.9, 4.4, 4.4, fill="FDEBE0", line=None)
    cv.circle(-0.7, 5.5, 2.4, 2.4, fill=GREEN_PALE, line=None)

    cv.img(M, 0.5, 2.1, 0.68, os.path.join(ASSETS, "logotipo.png"))
    cv.text(M, 1.28, 8.0, 0.26, "FECHAMENTO", size=9, bold=True,
            color=PINK_TEXT, spacing=1.0)
    cv.text(M, 1.58, 8.2, 0.62, "Os seis requisitos, entregues", size=31, bold=True,
            color=INK, spacing=1.05)
    cv.text(M, 2.34, 7.4, 0.5,
            "E tudo isso rodando em uma aplicação só: ./mvnw spring-boot:run e a API "
            "sobe com banco, dados e documentação.",
            size=10.4, color=MUTED, spacing=1.4)

    requisitos = [
        ("Modelos e entidades", "6 entidades JPA + 7 enums"),
        ("Banco de dados", "H2 em memória + data.sql"),
        ("Repositories", "6 interfaces Spring Data JPA"),
        ("Swagger / OpenAPI", "springdoc + 7 tags"),
        ("Operações CRUD", "POST · GET · PUT · DELETE"),
        ("Endpoints especializados", "filtros, conflitos, dashboard"),
    ]
    w = 3.85
    for i, (titulo, desc) in enumerate(requisitos):
        x = M + (i % 3) * (w + 0.34)
        y = 3.06 + (i // 3) * 0.98
        cv.rect(x, y, w, 0.84, WHITE, LINE, radius=0.16)
        cv.circle(x + 0.2, y + 0.24, 0.34, 0.34, MINT_SOFT, None)
        cv.text(x + 0.2, y + 0.24, 0.34, 0.34, "✓", size=10, bold=True,
                color=MINT_TEXT, align="c", valign="m", spacing=1.0)
        cv.text(x + 0.66, y + 0.16, w - 0.85, 0.24, titulo, size=9.4, bold=True,
                color=INK, spacing=1.0)
        cv.text(x + 0.66, y + 0.43, w - 0.85, 0.24, desc, size=7.8, color=MUTED,
                spacing=1.0)

    cv.rect(M, 5.26, 7.75, 1.5, WHITE, LINE, radius=0.18)
    cv.text(M + 0.26, 5.38, 6.0, 0.22, "PARA TESTAR AGORA", size=7.4, bold=True,
            color=MUTED_2, spacing=1.0)
    links = [("Swagger UI", "localhost:8080/swagger-ui.html"),
             ("OpenAPI JSON", "localhost:8080/api-docs"),
             ("Console H2", "localhost:8080/h2-console")]
    for i, (nome, url) in enumerate(links):
        y = 5.66 + i * 0.34
        cv.text(M + 0.26, y, 1.5, 0.24, nome, size=8, bold=True, color=INK,
                spacing=1.0)
        cv.text(M + 1.72, y, 5.8, 0.24, url, size=8, color=PINK_TEXT, font="m",
                spacing=1.0)

    cv.rect(8.55, 5.26, 4.23, 1.5, MINT, None, radius=0.18)
    cv.text(8.79, 5.42, 3.8, 0.34, "Perguntas?", size=15, bold=True, color=INK,
            spacing=1.0)
    cv.text(8.79, 5.86, 3.7, 0.7,
            "Obrigado! O projeto completo está no repositório, com README, testes e o "
            "roteiro de validação.", size=8.4, color="1F4A3A", spacing=1.4)

    cv.text(M, 6.86, CW, 0.24,
            "Helen Aclina  ·  Gabriel Wagner  ·  João Vitor Silva   —   Projeto "
            "Interdisciplinar · Fatec Mauá · 2026",
            size=8, color=MUTED, spacing=1.0)

    add(cv, "Fechamento", JOAO, notes=(
        "Fechando: os seis requisitos do trabalho estão entregues. Modelos e entidades com "
        "as seis classes JPA, banco H2 em memória com carga inicial, repositories com Spring "
        "Data, Swagger configurado e documentado, CRUD completo e os endpoints "
        "especializados com as regras do PetClean.\n"
        "Tudo isso roda com um comando, e os links para testar estão aqui. Obrigado — "
        "ficamos à disposição para perguntas."))


# ================================================================ montagem ===
def build():
    SLIDES.clear()
    s01_capa()
    s02_roteiro()
    s03_arquitetura()
    s04_entidades()
    s05_relacionamentos()
    s06_codigo()
    s07_divisor_gabriel()
    s09_h2()
    s10_repositories()
    s11_queries()
    s08_divisor_joao()
    s12_swagger()
    s13_crud()
    s14_especializados()
    s15_fechamento()
    return SLIDES


if __name__ == "__main__":
    for s in build():
        print(s["meta"]["title"], "|", s["meta"]["presenter"], "|", s["meta"]["time"],
              "|", len(s["canvas"].items), "elementos")
