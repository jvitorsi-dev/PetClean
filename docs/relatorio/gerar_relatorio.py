#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera o relatorio academico do Projeto de Extensao Comunitaria (Curricularizacao)
da FATEC Mauá referente ao sistema PetClean.

Estrutura: as 7 secoes obrigatorias do arquivo Modelo_projeto.pdf, com capa,
sumario, tabelas, figuras, paginacao e conclusao.

Todo dado tecnico citado foi conferido no codigo-fonte do repositorio
(branch arena/d25a6ca1-petclean) e nos documentos de docs/.

Uso: python3 gerar_relatorio.py
"""
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

FONTE = "Arial"
AZUL = RGBColor(0x1F, 0x4E, 0x79)
CINZA = RGBColor(0x44, 0x44, 0x44)
PRETO = RGBColor(0x00, 0x00, 0x00)

# ----------------------------------------------------------------------------
# Contadores
# ----------------------------------------------------------------------------
NUM_TABELA = [0]
NUM_FIGURA = [0]


# ----------------------------------------------------------------------------
# Helpers de formatacao
# ----------------------------------------------------------------------------
def configurar_estilos(doc):
    normal = doc.styles["Normal"]
    normal.font.name = FONTE
    normal.font.size = Pt(12)
    normal.font.color.rgb = PRETO
    pf = normal.paragraph_format
    pf.space_after = Pt(6)
    pf.line_spacing = 1.5
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1 = doc.styles["Heading 1"]
    h1.font.name = FONTE
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.font.color.rgb = AZUL
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(8)
    h1.paragraph_format.line_spacing = 1.15
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    h2 = doc.styles["Heading 2"]
    h2.font.name = FONTE
    h2.font.size = Pt(12)
    h2.font.bold = True
    h2.font.color.rgb = AZUL
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.line_spacing = 1.15
    h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    sec = doc.sections[0]
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(3.0)
    sec.bottom_margin = Cm(2.0)


def par(doc, texto="", tamanho=12, negrito=False, italico=False,
        alinhamento=WD_ALIGN_PARAGRAPH.JUSTIFY, antes=0, depois=6,
        espacamento=1.5, cor=None, recuo=0.0):
    p = doc.add_paragraph()
    p.alignment = alinhamento
    fmt = p.paragraph_format
    fmt.space_before = Pt(antes)
    fmt.space_after = Pt(depois)
    fmt.line_spacing = espacamento
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


def marcadores(doc, itens, tamanho=11.5, recuo=0.75):
    for item in itens:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.left_indent = Cm(recuo)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.4
        r = p.add_run(item)
        r.font.name = FONTE
        r.font.size = Pt(tamanho)


def h1(doc, texto):
    return doc.add_heading(texto, level=1)


def h2(doc, texto):
    return doc.add_heading(texto, level=2)


def legenda_tabela(doc, titulo):
    NUM_TABELA[0] += 1
    p = par(doc, f"Tabela {NUM_TABELA[0]} - {titulo}", tamanho=10, negrito=True,
            alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=8, depois=3, espacamento=1.15, cor=AZUL)
    return p


def fonte(doc, texto):
    par(doc, f"Fonte: {texto}", tamanho=8.5, italico=True,
        alinhamento=WD_ALIGN_PARAGRAPH.LEFT, antes=0, depois=10, espacamento=1.05, cor=CINZA)


def tabela(doc, cabecalho, linhas, larguras=None, tamanho=9.0, tamanho_cab=9.0,
           alinhamento_cab=WD_ALIGN_PARAGRAPH.CENTER):
    t = doc.add_table(rows=1, cols=len(cabecalho))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False

    # cabecalho
    hdr = t.rows[0].cells
    for i, texto in enumerate(cabecalho):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = alinhamento_cab
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(texto)
        r.font.name = FONTE
        r.font.size = Pt(tamanho_cab)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        sombrear(hdr[i], "1F4E79")

    for linha in linhas:
        celulas = t.add_row().cells
        for i, texto in enumerate(linha):
            celulas[i].text = ""
            p = celulas[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(str(texto))
            r.font.name = FONTE
            r.font.size = Pt(tamanho)

    if larguras:
        for row in t.rows:
            for i, larg in enumerate(larguras):
                row.cells[i].width = Cm(larg)
    return t


def sombrear(celula, hex_cor):
    tc_pr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_cor)
    tc_pr.append(shd)


def figura(doc, nome_arquivo, titulo, largura_cm=16.0, fonte_texto=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run()
    r.add_picture(os.path.join(FIGURAS, nome_arquivo), width=Cm(largura_cm))
    NUM_FIGURA[0] += 1
    par(doc, f"Figura {NUM_FIGURA[0]} - {titulo}", tamanho=10, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, antes=2, depois=2, espacamento=1.1, cor=AZUL)
    if fonte_texto:
        par(doc, f"Fonte: {fonte_texto}", tamanho=8.5, italico=True,
            alinhamento=WD_ALIGN_PARAGRAPH.CENTER, antes=0, depois=10, espacamento=1.05, cor=CINZA)
    return p


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
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


# =============================================================================
# DOCUMENTO
# =============================================================================
def construir():
    doc = Document()
    configurar_estilos(doc)

    # ---------------------------------------------------------------- CAPA ---
    for _ in range(2):
        par(doc, depois=0, espacamento=1.0)

    par(doc, "FACULDADE DE TECNOLOGIA DE MAUÁ - FATEC MAUÁ", tamanho=13, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=4, espacamento=1.15, cor=AZUL)
    par(doc, "Curso Superior de Tecnologia em Desenvolvimento de Software Multiplataforma",
        tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=28, espacamento=1.15)
    par(doc, "PROJETO DE EXTENSÃO COMUNITÁRIA", tamanho=15, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=2, espacamento=1.15, cor=AZUL)
    par(doc, "(Curricularização)", tamanho=13, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=40, espacamento=1.15, cor=AZUL)

    par(doc, "PETCLEAN", tamanho=26, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=6, espacamento=1.05, cor=AZUL)
    par(doc, "Desenvolvimento de um MVP (Mínimo Produto Viável) de software para gestão de um pet shop",
        tamanho=13, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=60, espacamento=1.3)

    par(doc, "Integrantes do Projeto:", tamanho=12, negrito=True,
        alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=8, espacamento=1.15)
    for nome in ("Helen Aclina", "Gabriel Wagner", "João Vitor"):
        par(doc, nome, tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
            depois=2, espacamento=1.15)

    par(doc, depois=60, espacamento=1.0)
    par(doc, "Mauá", tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=2, espacamento=1.15)
    par(doc, "2026", tamanho=12, alinhamento=WD_ALIGN_PARAGRAPH.CENTER, depois=0, espacamento=1.15)

    # ------------------------------------------------------------- SUMÁRIO ---
    quebra_pagina(doc)
    par(doc, "SUMÁRIO", tamanho=14, negrito=True, alinhamento=WD_ALIGN_PARAGRAPH.LEFT,
        antes=0, depois=8, espacamento=1.15, cor=AZUL)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    campo_toc(p)
    par(doc, "Nota: este sumário é gerado automaticamente pelo editor de texto a partir dos títulos "
             "numerados do documento.", tamanho=9, italico=True, cor=CINZA, depois=4, espacamento=1.1)

    # ------------------------------------------------- SECAO DE CONTEUDO 1 ---
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(3.0)
    sec.bottom_margin = Cm(2.0)
    # reinicia a numeracao em 1 nesta secao
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
    # 1. CARACTERÍSTICAS DO PROJETO DE EXTENSÃO
    # =========================================================================
    h1(doc, "1. CARACTERÍSTICAS DO PROJETO DE EXTENSÃO")

    par(doc,
        "O PetClean é um sistema web de gestão desenvolvido para atender às necessidades de um pet shop "
        "de pequeno porte. O trabalho foi conduzido pela equipe ao longo das quatro etapas previstas no "
        "modelo institucional do Projeto de Extensão Comunitária (Curricularização) da FATEC Mauá, "
        "resultando em um MVP composto por back-end em Java com Spring Boot, interface web migrada de uma "
        "versão anterior em PHP e uma base de dados relacional modelada e implementada no próprio projeto. "
        "O quadro a seguir reproduz a ficha do modelo institucional, preenchida com os dados deste projeto.")

    legenda_tabela(doc, "Características do Projeto de Extensão Comunitária - PetClean")
    tabela(doc,
           ["Campo", "Registro do projeto PetClean"],
           [
               ["Título",
                "Desenvolvimento de um MVP (Mínimo Produto Viável) de software para gestão de uma organização "
                "(3º Semestre): sistema PetClean de gestão para pet shops de pequeno porte."],
               ["Temática",
                "[ ] Programas   [X] Projetos   [ ] Cursos e Oficinas   [ ] Eventos   [ ] Prestação de Serviços"],
               ["Descrição",
                "A partir do levantamento das regras de negócio de um pet shop real, o projeto consistiu no "
                "desenvolvimento de um MVP de software para gestão de uma parte delimitada das rotinas do "
                "estabelecimento: cadastro de tutores e pets, agenda de serviços (banho, tosa, hidratação e "
                "consulta veterinária), controle de estoque com alerta de reposição, painel de indicadores e "
                "controle de acesso por usuário e senha."],
               ["Objetivos",
                "1) Analisar as regras de negócio e relatórios diagnósticos para produzir as documentações de "
                "Engenharia de Software; 2) Projetar, desenvolver, testar e entregar um MVP funcional; "
                "3) Projetar, modelar e implementar a base de dados; 4) Aplicar técnicas de gerenciamento de "
                "equipes a partir de análises das habilidades técnicas e humanas dos integrantes."],
               ["Carga horária",
                "Total: 130 horas/aula."],
               ["Público-alvo",
                "Empresas, ONGs, órgãos públicos e entidades sociais. Nesta edição, o público-alvo "
                "específico foi um pet shop de pequeno porte da região atendida pela unidade."],
               ["Ações / Etapas de execução",
                "1) Desenvolver documentação de Engenharia de Software; 2) Programar, testar e efetuar "
                "implantação em ambiente de testes para um MVP de sistema/software; 3) Modelar, implementar e "
                "testar uma base persistente de dados; 4) Documentar e relatar as ações e funções desempenhadas "
                "por cada integrante da equipe executora do projeto."],
               ["Entregas",
                "1) Projeto de banco de dados do MVP (modelo JPA com 6 entidades e 7 enumerações, Seção 5); "
                "2) Documentações de software do MVP (épicos e 25 histórias de usuário com critérios de "
                "aceitação, Seção 3; documentação automática da API via Swagger/OpenAPI, Seção 4); "
                "3) Código-fonte do MVP em repositório online na internet "
                "(https://github.com/jvitorsi-dev/PetClean); 4) Relatório de composição de equipe, funções e "
                "suas descrições de responsabilidades, relato de execução de tarefas e descrição das personas "
                "envolvidas (Seções 2 e 6)."],
               ["Instrumentos e procedimentos de avaliação",
                "Aluno: trabalho em grupo, eficácia na realização das tarefas, entrega digital do resultado "
                "das tarefas em relatório padronizado de atividade de extensão. Projeto: resultados obtidos, "
                "publicação dos resultados em repositório online, envio de resultados para a entidade "
                "beneficiada na comunidade ou execução de evento para apresentação dos resultados e integração "
                "com representantes da comunidade externa beneficiada."],
               ["Componente(s) curricular(es) envolvidos",
                "Banco de Dados (30 horas/aula) - Etapa 3; Linguagens de Programação I (40 horas/aula) - "
                "Etapa 2; Engenharia de Software (40 horas/aula) - Etapa 1; Gestão de Equipes "
                "(20 horas/aula) - Etapa 4."],
               ["Formas de evidência",
                "Entrega de relatório de atividade de extensão com os resultados em cada disciplina."],
           ],
           larguras=[4.2, 12.3], tamanho=9.0)
    fonte(doc, "Modelo institucional Modelo_projeto.pdf, preenchido com dados do repositório PetClean.")

    par(doc,
        "Cabe registrar o estágio em que o projeto se encontra. O sistema foi desenvolvido e validado "
        "internamente pela equipe em ambiente de testes, mas ainda não foi apresentado formalmente ao "
        "estabelecimento, não foi implantado em produção e não passou por validação ou coleta de feedback "
        "com os usuários do pet shop. A apresentação ao estabelecimento e a validação com usuários reais "
        "são atividades futuras, relacionadas na Seção 7.")

    # =========================================================================
    # 2. INFORMAÇÕES DA EQUIPE DE TRABALHO
    # =========================================================================
    h1(doc, "2. INFORMAÇÕES DA EQUIPE DE TRABALHO")

    par(doc,
        "A equipe executora é composta por três alunos do curso de Desenvolvimento de Software "
        "Multiplataforma. A divisão de funções declarada pela equipe atribui a coordenação das demandas à "
        "Helen, o desenvolvimento do front-end e da interface ao Gabriel e o desenvolvimento do back-end e "
        "do banco de dados ao João Vitor. A Seção 6 detalha as ações efetivamente desempenhadas por cada "
        "integrante, com a respectiva evidência nos artefatos do repositório.")

    legenda_tabela(doc, "Composição da equipe executora")
    tabela(doc,
           ["Nr.", "Nome completo do aluno", "E-mail", "WhatsApp"],
           [
               ["01", "Helen Aclina", "aclinahelen@gmail.com", "-"],
               ["02", "Gabriel Wagner", "wagninhodos@gmail.com", "-"],
               ["03", "João Vitor", "jvitorsi.dev@gmail.com", "-"],
           ],
           larguras=[1.2, 6.0, 6.3, 3.0], tamanho=10.0,
           alinhamento_cab=WD_ALIGN_PARAGRAPH.LEFT)
    fonte(doc, "Dados informados pela equipe. Os números de WhatsApp não foram fornecidos.")

    par(doc, "Nome do Grupo: PetClean", tamanho=12, negrito=True, antes=6, depois=8)

    # =========================================================================
    # 3. ETAPA 1
    # =========================================================================
    h1(doc, "3. ETAPA 1 - DESENVOLVIMENTO DE DOCUMENTAÇÃO DE ENGENHARIA DE SOFTWARE")

    par(doc, "Objetivo: Analisar as regras de negócio e relatórios diagnósticos para produzir as "
             "documentações de Engenharia de Software.", italico=True, depois=8)

    h2(doc, "3.1 Levantamento das regras de negócio do pet shop")

    par(doc,
        "O levantamento partiu da observação das rotinas do estabelecimento e resultou na delimitação de "
        "seis domínios funcionais, adotados como escopo do MVP e correspondentes aos seis épicos descritos "
        "na Seção 3.2: tutores (clientes); pets; agenda de serviços; estoque de produtos; indicadores "
        "gerenciais; e controle de acesso ao sistema. A delimitação foi necessária para que o "
        "MVP coubesse no tempo disponível sem comprometer a utilidade do sistema: o recorte abrange o que "
        "é usado diariamente no balcão do pet shop.")

    par(doc,
        "As regras levantadas não ficaram apenas em documento: foram materializadas como validações e "
        "impedimentos no código, o que permitiu à equipe verificar cada uma por teste automatizado. A "
        "Tabela 3 consolida as principais regras de negócio, o comportamento esperado e o ponto do "
        "código-fonte onde a regra está implementada.")

    legenda_tabela(doc, "Regras de negócio levantadas e sua localização no código-fonte")
    tabela(doc,
           ["Domínio", "Regra de negócio", "Comportamento", "Evidência no código"],
           [
               ["Clientes",
                "CPF é obrigatório, único e precisa ser válido",
                "CPF com dígito verificador inválido ou sequência repetida é recusado (422); CPF já "
                "cadastrado é recusado (409)",
                "service/ValidacaoCpf.java; service/ClienteService.java (validarCpf)"],
               ["Clientes",
                "Um tutor não pode ser apagado se possuir pets ou agendamentos",
                "Exclusão recusada (409) com mensagem que informa a quantidade de vínculos",
                "service/ClienteService.java (excluir)"],
               ["Pets",
                "Todo pet pertence a um tutor",
                "Chave estrangeira obrigatória (@ManyToOne optional = false)",
                "model/Pet.java"],
               ["Pets",
                "Pet com agendamento futuro ou histórico não pode ser excluído",
                "Exclusão recusada (409) preservando o histórico de atendimentos",
                "service/PetService.java (excluir)"],
               ["Agenda",
                "Não é possível agendar em data passada",
                "Recusa com 422 e a mensagem \"Não é possível agendar em data passada\"",
                "service/AgendamentoService.java (cadastrar)"],
               ["Agenda",
                "Não é possível agendar pet que não pertença ao tutor selecionado",
                "Recusa com 422, informando Tutor e pet",
                "service/AgendamentoService.java (cadastrar, atualizar)"],
               ["Agenda",
                "Dois atendimentos não podem ocupar o mesmo dia e horário",
                "Recusa com 409; cancelados não contam como ocupação, portanto o horário volta a ficar livre",
                "repository/AgendamentoRepository.java (contarConflitosNoHorario)"],
               ["Agenda",
                "Cancelamento exigem confirmação e não vale para atendimentos realizados",
                "Somente AGENDADO e CONFIRMADO podem ser cancelados (409 nos demais casos)",
                "model/StatusAgendamentoEnum.java (permiteCancelamento)"],
               ["Agenda",
                "Valor e duração do atendimento vêm do serviço escolhido",
                "O usuário não digita preço nem duração; ambos são copiados do catálogo",
                "model/ServicoEnum.java; service/AgendamentoService.java"],
               ["Estoque",
                "Quantidade e preço não podem ser negativos",
                "Recusa com 422 já na validação do corpo da requisição",
                "dto/ProdutoRequest.java; service/ProdutoService.java (validarValores)"],
               ["Estoque",
                "Saída não pode exceder a quantidade disponível",
                "Recusa com 409 informando o saldo disponível",
                "service/ProdutoService.java (movimentar)"],
               ["Estoque",
                "Produto com histórico de movimentação não pode ser excluído",
                "Recusa com 409, sugerindo a inativação do item",
                "service/ProdutoService.java (excluir)"],
               ["Estoque",
                "Estoque crítico quando a quantidade é igual ou inferior ao mínimo",
                "Campo calculado destacado na interface e usado nos alertas",
                "model/Produto.java (isEstoqueCritico)"],
               ["Indicadores",
                "Períodos sem movimentação devem aparecer zerados, sem erro",
                "Séries semanal (8 semanas) e mensal (6 meses) são pré-preenchidas com zero",
                "service/DashboardService.java (montarGraficoSemanal/Mensal)"],
               ["Acesso",
                "Toda tela interna exige usuário autenticado",
                "Navegador é redirecionado ao login (302) e cliente de API recebe 401",
                "security/InterceptorSeguranca.java"],
               ["Acesso",
                "Cada usuário altera somente o próprio perfil",
                "Tentativa de alterar perfil de terceiro é recusada com 403",
                "control/UsuarioController.java (exigirProprio)"],
           ],
           larguras=[2.0, 5.0, 5.5, 4.0], tamanho=8.3)
    fonte(doc, "Elaborada pelos autores a partir de src/main/java/br/com/fatecmaua/petclean/.")

    h2(doc, "3.2 Épicos e histórias de usuário com critérios de aceitação")

    par(doc,
        "A documentação de requisitos foi organizada em seis épicos, que reúnem 25 histórias de usuário "
        "numeradas de US-01 a US-25. Cada história recebeu critérios de aceitação no formato "
        "Dado / Quando / Então, posteriormente convertidos em testes automatizados - procedimento descrito "
        "na Seção 4.4. A numeração original das histórias foi preservada e é citada nos comentários do "
        "próprio código e na documentação da API, o que permite rastrear cada requisito até o trecho que o "
        "implementa.")

    legenda_tabela(doc, "Épicos, histórias de usuário e cobertura por endpoints")
    tabela(doc,
           ["Épico", "Histórias", "Qtd.", "Endpoints"],
           [
               ["EP-01 - Gerenciamento de Clientes", "US-03, US-04, US-05, US-06, US-15", "5", "6"],
               ["EP-02 - Gerenciamento de Pets", "US-07, US-08, US-09, US-10", "4", "7"],
               ["EP-03 - Controle de Agendamentos", "US-11, US-12, US-13, US-16, US-17", "5", "8"],
               ["EP-04 - Controle de Estoque", "US-18, US-19, US-20, US-21, US-25", "5", "10"],
               ["EP-05 - Dashboards Analíticos", "US-22, US-23, US-24", "3", "2"],
               ["EP-06 - Autenticação e Acesso", "US-01, US-02, US-14", "3", "4"],
               ["Perfil do usuário (tela agregada)", "-", "-", "5"],
               ["Catálogos e domínios de apoio", "-", "-", "6"],
               ["Total", "US-01 a US-25", "25", "48"],
           ],
           larguras=[6.2, 5.4, 1.6, 3.3], tamanho=9.0)
    fonte(doc, "README.md e control/*.java (contagem de mapeamentos @GetMapping/@PostMapping/@PutMapping/"
               "@PatchMapping/@DeleteMapping).")

    legenda_tabela(doc, "Rastreabilidade: história de usuário, regra implementada e endpoint")
    tabela(doc,
           ["História", "Regra implementada", "Endpoint"],
           [
               ["US-01 - Login",
                "Autenticação por e-mail e senha; senha conferida contra o hash bcrypt",
                "POST /login"],
               ["US-02 - Proteger rotas",
                "Rotas internas exigem sessão: 401 para API e 302 para navegador, com retorno à rota pedida",
                "InterceptorSeguranca"],
               ["US-03 - Cadastrar cliente",
                "Validação de campos obrigatórios; registro salvo e exibido na listagem",
                "POST /api/clientes"],
               ["US-04 - Consultar e filtrar",
                "Filtro por nome ou CPF, com versão otimizada por projeção",
                "GET /api/clientes?termo= ; GET /api/clientes/resumo"],
               ["US-05 - Editar cliente",
                "Formulário preenchido com os dados atuais; CPF permanece único",
                "PUT /api/clientes/{id}"],
               ["US-06 - Excluir cliente",
                "Confirmação na tela; bloqueio quando há pets ou agendamentos vinculados",
                "DELETE /api/clientes/{id}"],
               ["US-07 - Cadastrar pet vinculado",
                "Tutor obrigatório; idade validada entre 0 e 40 anos",
                "POST /api/pets"],
               ["US-08 - Consultar e filtrar pets",
                "Filtro pelo nome do pet ou do tutor; lista nome, espécie e tutor",
                "GET /api/pets?termo= ; GET /api/pets/resumo"],
               ["US-09 - Editar pet",
                "Campos preenchidos; o tutor vinculado não é alterado por esta tela",
                "PUT /api/pets/{id}"],
               ["US-10 - Excluir pet",
                "Bloqueio quando há agendamento futuro ou histórico de atendimentos",
                "DELETE /api/pets/{id}"],
               ["US-11 - Cadastrar agendamento",
                "Lista apenas os pets do tutor; valor e duração derivam do serviço; status inicial AGENDADO",
                "POST /api/agendamentos"],
               ["US-12 - Listar com filtros",
                "Filtro por data e/ou status, ordenado por horário; agenda do dia por projeção",
                "GET /api/agendamentos ; GET /api/agendamentos/agenda"],
               ["US-13 - Atualizar status",
                "Registra o novo status e a data/hora da alteração",
                "PATCH /api/agendamentos/{id}/status"],
               ["US-14 - Logout",
                "Invalida a sessão HTTP",
                "POST /logout"],
               ["US-15 - CPF duplicado",
                "Valida formato e dígitos verificadores; bloqueia duplicidade com \"CPF já cadastrado\"",
                "POST /api/clientes ; PUT /api/clientes/{id}"],
               ["US-16 - Cancelar agendamento",
                "Exige confirmação, muda para CANCELADO e libera o horário; realizado não cancela",
                "PATCH /api/agendamentos/{id}/cancelar"],
               ["US-17 - Conflito de horário",
                "Mesmo dia e horário com atendimento ativo: 409, sem gravar",
                "POST /api/agendamentos ; PUT /api/agendamentos/{id}"],
               ["US-18 - Cadastrar produto",
                "Valida quantidade e preço negativos; define o estoque mínimo",
                "POST /api/produtos"],
               ["US-19 - Atualizar quantidade",
                "Entrada e saída com registro no histórico; saída acima do disponível é impedida",
                "PATCH /api/produtos/{id}/movimentar"],
               ["US-20 - Alerta de estoque crítico",
                "Produto destacado quando a quantidade é igual ou inferior ao mínimo",
                "GET /api/produtos ; GET /api/produtos/estoque-critico"],
               ["US-21 - Excluir produto",
                "Sem movimentação exclui; com histórico responde 409 e sugere inativar",
                "DELETE /api/produtos/{id} ; PATCH /api/produtos/{id}/inativar"],
               ["US-22 - Cards de indicadores",
                "Totais de clientes, de pets e de agendamentos do mês, zerados quando não há dados",
                "GET /api/dashboard"],
               ["US-23 - Gráfico por período",
                "Agregação semanal (8 semanas) ou mensal (6 meses), com eixos zerados sem erro",
                "GET /api/dashboard?periodo="],
               ["US-24 - Estoque crítico no painel",
                "Lista ordenada do mais crítico ao menos crítico, com indicador de estoque normal",
                "GET /api/dashboard/estoque-critico"],
               ["US-25 - Buscar produto",
                "Filtro combinado por nome e categoria",
                "GET /api/produtos?termo=&categoria="],
           ],
           larguras=[4.3, 8.0, 4.4], tamanho=8.3)
    fonte(doc, "README.md, conferido contra control/*.java e service/*.java.")

    h2(doc, "3.3 Requisitos não funcionais e critérios de aceitação")

    par(doc,
        "Os requisitos não funcionais considerados relevantes para o MVP foram registrados em decisões "
        "concretas de implementação e podem ser verificados no código. Dois deles aparecem nomeados nos "
        "comentários das classes (RNF-04 e RNF-09) e os demais correspondem a restrições técnicas adotadas "
        "pela equipe, igualmente verificáveis.")

    legenda_tabela(doc, "Requisitos não funcionais e restrições técnicas adotadas")
    tabela(doc,
           ["Identificação", "Requisito / restrição", "Decisão adotada", "Evidência"],
           [
               ["RNF-04", "Senhas não podem ser armazenadas em texto puro",
                "Hash bcrypt gerado e conferido com BCryptPasswordEncoder; o hash nunca é devolvido nas "
                "respostas nem guardado na sessão",
                "service/AutenticacaoService.java; model/Usuario.java (senha_hash); "
                "security/UsuarioSessao.java"],
               ["RNF-09", "Integridade referencial das exclusões",
                "Exclusões com vínculo são recusadas com 409 e mensagem explicativa, em vez de remoção em "
                "cascata",
                "service/ClienteService.java; service/PetService.java; service/ProdutoService.java"],
               ["Desempenho", "Listagens devem carregar apenas o necessário",
                "Consultas nativas com projeções (interfaces) para telas de listagem",
                "repository/*Repository.java; projection/*.java"],
               ["Portabilidade", "O projeto deve ser executado sem instalação de servidor de banco",
                "Banco H2 em memória, criado e populado automaticamente na subida da aplicação",
                "pom.xml; application.properties; data.sql"],
               ["Usabilidade", "Mensagens de erro devem ser compreensíveis ao atendente",
                "Resposta de erro padronizada, com mensagem e detalhamento por campo",
                "dto/ErroResposta.java; exception/GlobalExceptionHandler.java"],
               ["Segurança de sessão", "Sessão com cookie protegido e tempo limitado",
                "Cookie PETCLEANSESSION com atributo HttpOnly e tempo de inatividade de 60 minutos",
                "application.properties"],
               ["Limite de upload", "Foto de perfil com tamanho controlado",
                "Limite de 2 MB validado no service e replicado na configuração do servlet",
                "service/UsuarioService.java; application.properties"],
               ["Idioma e formatação", "Números e datas no padrão brasileiro",
                "Locale fixo pt-BR e leitura do script de carga em UTF-8",
                "application.properties"],
               ["Documentação", "A API deve ser auto-documentada",
                "Swagger UI e especificação OpenAPI gerados a partir das anotações do código",
                "swagger/SwaggerConfig.java; springdoc-openapi 2.8.13"],
           ],
           larguras=[2.2, 4.2, 6.0, 4.3], tamanho=8.3)
    fonte(doc, "Elaborada pelos autores a partir do código-fonte e de application.properties.")

    h2(doc, "3.4 Gerenciamento da equipe com Scrum e Kanban")

    par(doc,
        "A coordenação ficou com a Helen, responsável pelo gerenciamento das demandas, pelo "
        "acompanhamento das entregas e pela aplicação das práticas de Scrum e Kanban. O README do "
        "repositório registra a relação entre as práticas ágeis adotadas e o que se observa no código; a "
        "Tabela 7 reproduz essa correspondência, acrescentando a evidência verificável em cada caso.")

    legenda_tabela(doc, "Práticas ágeis adotadas e evidências no projeto")
    tabela(doc,
           ["Prática", "Como se materializou no PetClean", "Evidência"],
           [
               ["Kanban - fluxo com políticas explícitas",
                "Cada história tem endpoint próprio, mensagem de erro explícita e código de status "
                "documentado, o que funciona como política de entrada e saída de cada etapa do fluxo",
                "control/*.java; exception/GlobalExceptionHandler.java"],
               ["WIP limitado e entregas pequenas (XP)",
                "Um endpoint por história, com serviços e validações de escopo reduzido",
                "service/*.java; testes-api.sh valida uma história por vez"],
               ["Definition of Done",
                "Critérios Dado/Quando/Então convertidos em testes automatizados de integração",
                "src/test/java/.../ApiPetCleanIntegrationTest.java (28 testes)"],
               ["Simplicidade - MVP primeiro",
                "O núcleo indispensável foi implementado de forma direta, sem generalizações "
                "antecipadas",
                "Ausência de camadas ou abstrações não utilizadas no pacote service/"],
               ["Inspeção contínua",
                "Roteiro de validação documentado, com resultado esperado de cada verificação",
                "docs/VALIDACAO.md; docs/COMO-TESTAR.md"],
               ["Registro de decisões e pendências",
                "Migração tecnológica documentada com matriz de rastreabilidade e lista de "
                "incompatibilidades",
                "docs/MIGRACAO-PHP-JAVA.md"],
           ],
           larguras=[4.0, 7.2, 5.5], tamanho=8.3)
    fonte(doc, "README.md (seção 5) e documentos de docs/, conferidos contra o código-fonte.")

    # =========================================================================
    # 4. ETAPA 2
    # =========================================================================
    h1(doc, "4. ETAPA 2 - PROGRAMAÇÃO, TESTE E IMPLANTAÇÃO EM AMBIENTE DE TESTES PARA UM MVP "
            "DE SISTEMA/SOFTWARE")

    par(doc, "Objetivo: Projetar, desenvolver, testar e entregar um MVP funcional.",
        italico=True, depois=8)

    h2(doc, "4.1 Arquitetura, tecnologias e evolução de PHP para Java")

    par(doc,
        "O PetClean começou a ser desenvolvido em PHP, com páginas que misturavam marcação HTML e "
        "consultas ao banco feitas diretamente por PDO, controle de acesso com a sessão nativa da "
        "linguagem e formulários enviados por fetch com FormData para scripts auxiliares. Ao longo do "
        "semestre, seguindo as orientações dos professores e o conteúdo das disciplinas, o projeto foi "
        "migrado para Java com Spring Boot, mantendo a interface visual original. A migração está "
        "documentada em docs/MIGRACAO-PHP-JAVA.md, inclusive com a matriz de rastreabilidade página a "
        "página e o registro das incompatibilidades encontradas.")

    par(doc,
        "A Tabela 8 resume a diferença entre as duas versões. Importa notar que o acervo da versão PHP "
        "não está preservado no histórico do repositório - o Git contém apenas a versão Java - e que as "
        "informações sobre a versão anterior provêm do documento de migração escrito pela equipe.")

    legenda_tabela(doc, "Comparação entre a versão original em PHP e a versão atual em Java")
    tabela(doc,
           ["Aspecto", "Versão original (PHP)", "Versão atual (Java)"],
           [
               ["Linguagem e plataforma", "PHP, com marcação e consulta na própria página",
                "Java 17, com Spring Boot 3.5.16 e Maven (wrapper incluso)"],
               ["Renderização das telas", "echo, foreach e if embutidos no HTML",
                "Thymeleaf (th:text, th:each, th:if), emitindo o mesmo HTML"],
               ["Acesso a dados", "PDO com MySQL, instruções SQL dentro de cada página",
                "Spring Data JPA sobre Hibernate; H2 em memória no ambiente de testes"],
               ["Sessão", "$_SESSION['usuario']",
                "HttpSession com o atributo USUARIO_AUTENTICADO e cookie PETCLEANSESSION"],
               ["Comunicação da tela", "fetch para scripts php/, com FormData",
                "fetch para /api/**, com JSON, centralizado em static/js/api.js"],
               ["Validação", "Verificações dispersas nos scripts PHP",
                "Bean Validation nos DTOs (@Valid) mais validações de negócio nos services"],
               ["Tratamento de erro", "Mensagens variadas por script",
                "GlobalExceptionHandler com resposta JSON padronizada (ErroResposta)"],
               ["Documentação da API", "Inexistente",
                "Swagger UI e OpenAPI gerados por springdoc-openapi 2.8.13"],
               ["Testes automatizados", "Não identificados no acervo recebido",
                "34 testes JUnit, além de scripts de verificação de ponta a ponta"],
           ],
           larguras=[3.6, 6.1, 6.8], tamanho=8.6)
    fonte(doc, "docs/MIGRACAO-PHP-JAVA.md (seções 1 e 3), pom.xml e application.properties.")

    par(doc,
        "A aplicação é organizada em camadas, com separação rigorosa de responsabilidades: a camada de "
        "controle cuida apenas do protocolo HTTP, a camada de serviço concentra as regras de negócio e a "
        "camada de repositório isola o acesso ao banco. A Figura 1 apresenta essa organização e os "
        "elementos transversais.")

    figura(doc, "fig01_arquitetura.png",
           "arquitetura em camadas do PetClean e pacotes transversais",
           largura_cm=16.4,
           fonte_texto="Elaborada pelos autores a partir de pom.xml, application.properties e dos pacotes "
                       "control/, service/, repository/, model/, dto/, security/ e exception/.")

    legenda_tabela(doc, "Dependências declaradas no pom.xml e finalidade de cada uma")
    tabela(doc,
           ["Dependência", "Finalidade no PetClean"],
           [
               ["spring-boot-starter-web", "Camada Web, controllers REST e servidor de arquivos estáticos"],
               ["spring-boot-starter-data-jpa", "Mapeamento objeto-relacional (Hibernate) e repositórios"],
               ["spring-boot-starter-validation", "Bean Validation nos DTOs de entrada (@Valid)"],
               ["spring-boot-starter-thymeleaf", "Renderização das 8 páginas do painel no servidor"],
               ["spring-security-crypto", "BCryptPasswordEncoder para o hash de senhas (RNF-04)"],
               ["com.h2database:h2 (runtime)", "Banco de dados relacional em memória e console web"],
               ["springdoc-openapi-starter-webmvc-ui 2.8.13", "Swagger UI e especificação OpenAPI"],
               ["spring-boot-starter-test (test)", "JUnit 5, MockMvc e infraestrutura de teste"],
           ],
           larguras=[6.2, 10.3], tamanho=9.0)
    fonte(doc, "pom.xml (Spring Boot 3.5.16, Java 17, groupId br.com.fatecmaua, artifactId petclean).")

    legenda_tabela(doc, "Organização dos pacotes da aplicação")
    tabela(doc,
           ["Pacote", "Conteúdo", "Responsabilidade"],
           [
               ["model/", "6 entidades JPA e 7 enumerações", "Representar o domínio e o esquema do banco"],
               ["repository/", "6 interfaces", "Consultas: métodos derivados, HQL e SQL nativo"],
               ["projection/", "5 interfaces", "Consultas otimizadas que devolvem apenas colunas necessárias"],
               ["service/", "7 classes @Service e 1 utilitária", "Regras de negócio das 25 histórias"],
               ["control/", "8 @RestController e 2 @Controller", "Endpoints REST e páginas do painel"],
               ["dto/", "13 records", "Contratos de entrada validados e de saída"],
               ["security/", "4 classes", "Sessão, interceptor de acesso e configuração Web MVC"],
               ["exception/", "2 classes", "Exceção de negócio e tratamento centralizado de erros"],
               ["swagger/", "1 classe", "Metadados da documentação OpenAPI"],
           ],
           larguras=[3.2, 5.6, 7.7], tamanho=9.0)
    fonte(doc, "Contagem de arquivos em src/main/java/br/com/fatecmaua/petclean/ (63 arquivos, 4.325 linhas).")

    h2(doc, "4.2 Implementação do MVP: controladores, serviços e endpoints")

    par(doc,
        "A API REST expõe 48 rotas, distribuídas em oito controladores anotados com @RestController. Dois "
        "controladores adicionais anotados com @Controller atendem as nove rotas de páginas: GET /login, "
        "que encaminha o navegador à tela de autenticação, e as oito telas do painel, servidas sob "
        "/paginas/. As rotas REST estão agrupadas por domínio, e cada grupo corresponde a uma tag da "
        "documentação Swagger.")

    legenda_tabela(doc, "Endpoints da API REST do PetClean, agrupados por domínio")
    tabela(doc,
           ["Domínio", "Método e rota", "História atendida"],
           [
               ["Clientes", "GET /api/clientes?termo=", "US-04"],
               ["Clientes", "GET /api/clientes/resumo", "US-04"],
               ["Clientes", "GET /api/clientes/{id}", "US-05"],
               ["Clientes", "POST /api/clientes", "US-03, US-15"],
               ["Clientes", "PUT /api/clientes/{id}", "US-05, US-15"],
               ["Clientes", "DELETE /api/clientes/{id}", "US-06"],
               ["Pets", "GET /api/pets?termo=", "US-08"],
               ["Pets", "GET /api/pets/resumo", "US-08"],
               ["Pets", "GET /api/pets/cliente/{idCliente}", "US-11"],
               ["Pets", "GET /api/pets/{id}", "US-09"],
               ["Pets", "POST /api/pets", "US-07"],
               ["Pets", "PUT /api/pets/{id}", "US-09"],
               ["Pets", "DELETE /api/pets/{id}", "US-10"],
               ["Agendamentos", "GET /api/agendamentos?data=&status=", "US-12"],
               ["Agendamentos", "GET /api/agendamentos/agenda", "US-12"],
               ["Agendamentos", "GET /api/agendamentos/{id}", "US-11"],
               ["Agendamentos", "POST /api/agendamentos", "US-11, US-17"],
               ["Agendamentos", "PUT /api/agendamentos/{id}", "US-17"],
               ["Agendamentos", "PATCH /api/agendamentos/{id}/status", "US-13"],
               ["Agendamentos", "PATCH /api/agendamentos/{id}/cancelar", "US-16"],
               ["Agendamentos", "DELETE /api/agendamentos/{id}", "US-12"],
               ["Estoque", "GET /api/produtos?termo=&categoria=", "US-25"],
               ["Estoque", "GET /api/produtos/resumo", "US-25"],
               ["Estoque", "GET /api/produtos/estoque-critico", "US-20"],
               ["Estoque", "GET /api/produtos/{id}", "US-18"],
               ["Estoque", "POST /api/produtos", "US-18"],
               ["Estoque", "PUT /api/produtos/{id}", "US-19"],
               ["Estoque", "PATCH /api/produtos/{id}/movimentar", "US-19"],
               ["Estoque", "PATCH /api/produtos/{id}/inativar", "US-21"],
               ["Estoque", "DELETE /api/produtos/{id}", "US-21"],
               ["Estoque", "GET /api/produtos/movimentacoes", "US-19"],
               ["Dashboard", "GET /api/dashboard?periodo=", "US-22, US-23"],
               ["Dashboard", "GET /api/dashboard/estoque-critico", "US-24"],
               ["Autenticação", "POST /login", "US-01"],
               ["Autenticação", "POST /logout", "US-14"],
               ["Autenticação", "GET /api/sessao", "US-01, US-02"],
               ["Autenticação", "GET /api/verificar-acesso", "US-02"],
               ["Perfil", "GET /api/usuarios/{id}", "Tela de perfil"],
               ["Perfil", "PUT /api/usuarios/{id}", "Tela de perfil"],
               ["Perfil", "PUT /api/usuarios/{id}/senha", "Tela de perfil"],
               ["Perfil", "POST /api/usuarios/{id}/foto", "Tela de perfil"],
               ["Perfil", "GET /api/usuarios/{id}/foto", "Tela de perfil"],
               ["Catálogos", "GET /api/catalogos/servicos", "US-11"],
               ["Catálogos", "GET /api/catalogos/especies", "US-07"],
               ["Catálogos", "GET /api/catalogos/portes", "US-07"],
               ["Catálogos", "GET /api/catalogos/status-agendamento", "US-13"],
               ["Catálogos", "GET /api/catalogos/categorias-produto", "US-18"],
               ["Catálogos", "GET /api/catalogos/tipos-movimentacao", "US-19"],
           ],
           larguras=[2.6, 8.2, 5.7], tamanho=8.3)
    fonte(doc, "control/*.java (48 mapeamentos REST nos 8 controladores @RestController).")

    par(doc,
        "O comportamento da API em situações de sucesso e de erro é uniforme, o que simplifica tanto o "
        "consumo pelo front-end quanto a verificação por testes. A Tabela 12 descreve o significado de "
        "cada código de status e o exemplo de regra que o provoca.")

    legenda_tabela(doc, "Códigos de status HTTP utilizados pela API")
    tabela(doc,
           ["Código", "Significado na API PetClean", "Exemplo de situação"],
           [
               ["200", "Consulta ou alteração concluída", "GET /api/clientes; PUT /api/pets/{id}"],
               ["201", "Recurso criado", "POST /api/clientes, /api/pets, /api/produtos, /api/agendamentos"],
               ["204", "Operação concluída sem conteúdo de resposta",
                "DELETE sem vínculos; POST /logout; PUT /api/usuarios/{id}/senha"],
               ["400", "Corpo da requisição inválido ou campo fora do padrão",
                "Nome com menos de 3 caracteres; JSON malformado; data em formato inválido"],
               ["401", "Requisição sem sessão autenticada",
                "Acesso a /api/clientes sem login; senha incorreta no POST /login"],
               ["403", "Usuário autenticado sem permissão sobre o recurso",
                "Alterar o perfil de outro usuário (PUT /api/usuarios/{id})"],
               ["404", "Recurso inexistente", "GET /api/clientes/999"],
               ["409", "Conflito com regra de negócio ou integridade",
                "CPF duplicado; horário ocupado; exclusão com vínculos; saída acima do saldo"],
               ["422", "Dado rejeitado por regra de negócio",
                "CPF inválido; data de agendamento passada; pet de outro tutor; foto acima de 2 MB"],
               ["500", "Erro inesperado", "Falha não prevista, registrada com mensagem técnica"],
           ],
           larguras=[1.7, 6.6, 8.2], tamanho=8.6)
    fonte(doc, "exception/ErroNegocioException.java, exception/GlobalExceptionHandler.java e control/*.java.")

    par(doc,
        "A padronização das respostas de erro é feita por um único componente, o GlobalExceptionHandler, "
        "que converte exceções em objetos ErroResposta com os campos status, erro, mensagem, detalhes, "
        "momento e rota. Com isso, o front-end exibe a mensagem real produzida pela regra de negócio - "
        "por exemplo \"CPF já cadastrado\" ou \"Não é possível agendar em data passada\" - em vez de "
        "mensagens genéricas da própria tela.")

    h2(doc, "4.3 Interface web, autenticação e segurança")

    par(doc,
        "A interface foi preservada na migração: o HTML, as 12 folhas de estilo (3.072 linhas) e os "
        "10 arquivos JavaScript da versão em PHP foram mantidos, e apenas a origem dos dados e o destino "
        "dos formulários foram alterados. As oito telas do painel (dashboard, clientes, pets, estoque, "
        "agendamentos, relatórios, perfil e configurações) são renderizadas no servidor por Thymeleaf e "
        "alimentadas pelos mesmos serviços da API; as sete páginas públicas do site (início, sobre nós, "
        "funcionalidades, fale conosco, solicitar demonstração, login e recuperar senha) são estáticas. "
        "Um arquivo novo, static/js/api.js, centraliza as chamadas à API e traduz as respostas para o "
        "formato que os scripts originais já esperavam, de modo que os alertas, as confirmações e o "
        "recarregamento da página continuaram idênticos aos do sistema em PHP.")

    par(doc,
        "Três ajustes de interface foram inevitáveis e estão registrados no documento de migração: os "
        "modais de cliente e de pet receberam campos obrigatórios que não existiam no formulário original "
        "(CPF e endereço; espécie e porte), e o campo de categoria do estoque, que em PHP era texto livre, "
        "passou a ser uma lista de seleção com os seis valores do enum da API. Fora isso, nenhuma regra de "
        "CSS foi criada ou alterada.")

    par(doc,
        "O controle de acesso é feito por sessão HTTP, sem o uso do Spring Security completo - decisão "
        "registrada no README como forma de manter o projeto didático. Um HandlerInterceptor registrado "
        "para todas as rotas verifica a existência do usuário na sessão e age de dois modos: requisições "
        "de navegador, reconhecidas pelo cabeçalho Accept contendo text/html, são redirecionadas para "
        "/login com a rota original guardada na sessão, retornando a ela após a autenticação; requisições "
        "de cliente de API recebem 401 com JSON explicativo. A autenticação compara a senha informada com "
        "o hash bcrypt gravado no banco. O fluxo completo está na Figura 2.")

    figura(doc, "fig03_autenticacao.png",
           "fluxo de autenticação (US-01, US-02 e US-14) e proteção de rotas",
           largura_cm=16.4,
           fonte_texto="Elaborada pelos autores a partir de security/InterceptorSeguranca.java, "
                       "security/SessaoService.java, service/AutenticacaoService.java e "
                       "control/LoginController.java.")

    par(doc,
        "Duas limitações de segurança merecem registro, pois decorrem de decisões de escopo e não de "
        "falhas de implementação. Primeira: o modelo de usuário prevê dois perfis, ATENDENTE e GESTOR, e "
        "o perfil é exibido na interface, mas o interceptor verifica apenas se o usuário está autenticado "
        "- não há restrição de acesso por perfil, de modo que ambos os perfis alcançam as mesmas "
        "funcionalidades. Segunda: a aplicação não é multi-inquilino, isto é, não há separação dos dados "
        "por estabelecimento; todos os usuários enxergam a mesma base. A Tabela 13 registra essas e outras "
        "pendências, com o encaminhamento dado pela equipe.")

    legenda_tabela(doc, "Pendências identificadas e encaminhamento dado pela equipe")
    tabela(doc,
           ["Pendência", "Efeito no MVP", "Encaminhamento"],
           [
               ["Recuperação de senha sem endpoint",
                "A tela \"Recuperar senha\" existe, mas o envio não tem backend",
                "Registrado como pendência; depende de serviço de e-mail (fora do escopo do MVP)"],
               ["Solicitação de demonstração sem endpoint",
                "O formulário público exibe mensagem informando a indisponibilidade",
                "Registrado como pendência; o script avisa o usuário em vez de simular o envio"],
               ["Notificações sem persistência",
                "Os alertas são derivados de dados reais (estoque crítico e agenda do dia); a ação "
                "\"marcar todas como lidas\" vale apenas para a sessão do navegador",
                "Solução provisória em sessionStorage, registrada no documento de migração"],
               ["Relatórios com valores fixos em parte dos gráficos",
                "Cinco gráficos mantêm os valores definidos na versão PHP",
                "Mantidos como no original; apenas um deles é alimentado por dados reais"],
               ["Ausência de separação por estabelecimento",
                "Todos os usuários veem a mesma base de dados",
                "Declarado como fora de escopo do MVP"],
               ["Autorização por perfil não aplicada",
                "ATENDENTE e GESTOR acessam as mesmas telas e ações",
                "Perfis modelados e exibidos; a restrição por perfil fica como evolução"],
               ["Banco em memória",
                "Os dados são descartados ao encerrar a aplicação",
                "Adequado ao ambiente de testes; a migração para SGBD persistente é atividade futura"],
           ],
           larguras=[4.6, 6.0, 5.9], tamanho=8.3)
    fonte(doc, "docs/MIGRACAO-PHP-JAVA.md (seções 3.3 e 7) e inspeção de security/ e model/PerfilEnum.java.")

    h2(doc, "4.4 Testes e implantação em ambiente de testes")

    par(doc,
        "A estratégia de teste combinou três abordagens. A primeira é a suíte JUnit, executada pelo Maven "
        "e composta por 34 testes: 28 testes de integração que exercitam a API com MockMvc, verificando "
        "contrato, códigos de status e sessão em casos distribuídos entre os seis épicos e a tela de "
        "perfil; 5 testes unitários da validação de CPF; e 1 teste que apenas verifica se o contexto do "
        "Spring sobe corretamente. A segunda é o script testes-api.sh, que executa 50 verificações de "
        "ponta a ponta contra a aplicação em execução, organizadas história por história e reutilizando "
        "um cookie de sessão. A terceira é o script "
        "validar-estatico.sh, que roda sem servidor e confere resíduos de PHP, links quebrados, "
        "chamadas mapeadas para a API, sintaxe dos arquivos JavaScript, balanceamento do HTML e a "
        "correspondência entre as variáveis usadas nos templates e os atributos enviados pelo controlador "
        "de páginas.")

    legenda_tabela(doc, "Suítes de teste automatizado do PetClean")
    tabela(doc,
           ["Suíte / script", "Quantidade", "Escopo", "Como executar"],
           [
               ["ApiPetCleanIntegrationTest", "28 testes",
                "Contrato da API: login, sessão, validações, conflitos, integridade referencial, "
                "movimentação de estoque, dashboard e perfil",
                "./mvnw test"],
               ["ValidacaoCpfTest", "5 testes",
                "Normalização e dígito verificador do CPF, incluindo rejeição de sequências repetidas",
                "./mvnw test"],
               ["PetCleanApplicationTests", "1 teste",
                "Verificação de que o contexto Spring é carregado sem erro",
                "./mvnw test"],
               ["testes-api.sh", "50 verificações",
                "Smoke test de ponta a ponta: uma verificação por história, com a aplicação em execução",
                "bash testes-api.sh"],
               ["validar-estatico.sh", "8 grupos de checagem",
                "Análise estática do front-end migrado (sem servidor e sem Maven)",
                "bash validar-estatico.sh"],
           ],
           larguras=[3.9, 2.6, 6.0, 4.0], tamanho=8.3)
    fonte(doc, "src/test/java/ (396 linhas), testes-api.sh e validar-estatico.sh.")

    par(doc,
        "A execução dos testes está documentada em docs/VALIDACAO.md, que organiza cinco validações "
        "(V1 a V5) com o resultado esperado de cada uma e um quadro de evidências. A Tabela 15 reproduz "
        "esse quadro, distinguindo o que foi efetivamente executado do que permanece pendente.")

    legenda_tabela(doc, "Registro de evidências das validações (V1 a V5)")
    tabela(doc,
           ["Validação", "Data registrada", "Resultado", "Situação atual"],
           [
               ["V1 - Compilação e testes unitários",
                "07/11/2026",
                "BUILD SUCCESS, 28 testes, 0 falhas, 0 erros (Windows, Java 17.0.12). A primeira execução "
                "apresentou 2 falhas, corrigidas: redirecionamento do interceptor e uso de data fixa em "
                "testes de agendamento",
                "Concluída"],
               ["V2 - Smoke test dos endpoints",
                "Não registrada",
                "Script pronto, com 50 verificações",
                "Pendente de execução e registro"],
               ["V3 - Validação funcional do painel",
                "07/11/2026",
                "4 casos críticos verificados na tela pela própria equipe: proteção de sessão, agendamento "
                "em data passada, CPF repetido e estoque crítico",
                "Parcial - os demais casos dependem do V2"],
               ["V4 - Validação visual",
                "Não registrada",
                "Comparação com capturas de referência da versão PHP",
                "Pendente"],
               ["V5 - Checagens estáticas",
                "07/11/2026",
                "0 falhas e 0 avisos",
                "Concluída"],
           ],
           larguras=[4.0, 2.3, 6.6, 3.6], tamanho=8.3)
    fonte(doc, "docs/VALIDACAO.md (quadro \"Registro de evidências\") e docs/MIGRACAO-PHP-JAVA.md (seção 5).")

    par(doc,
        "Sobre a implantação: o modelo institucional pede a implantação em ambiente de testes, e é "
        "exatamente esse o estágio alcançado. A aplicação é executada localmente pelo comando "
        "spring-boot:run, sobe na porta 8080 e disponibiliza o painel, a documentação Swagger e o console "
        "do banco H2. Não houve implantação em servidor de produção, publicação em nuvem nem entrega do "
        "sistema ao estabelecimento. As datas registradas na Tabela 15 referem-se a execuções feitas pela "
        "própria equipe em seu ambiente de desenvolvimento.")

    # =========================================================================
    # 5. ETAPA 3
    # =========================================================================
    h1(doc, "5. ETAPA 3 - MODELAGEM, IMPLEMENTAÇÃO E TESTE DE UMA BASE PERSISTENTE DE DADOS PARA "
            "ARMAZENAMENTO DOS DADOS DA SOLUÇÃO MVP DESENVOLVIDA")

    par(doc, "Objetivo: Projetar, modelar e implementar a base de dados.", italico=True, depois=8)

    h2(doc, "5.1 Escolha e configuração do sistema gerenciador de banco de dados")

    par(doc,
        "Na versão em PHP, o acesso ao banco era feito por PDO sobre MySQL. Na versão atual, o ambiente "
        "de testes passou a usar o H2 em memória, escolhido por permitir que o projeto seja executado em "
        "qualquer máquina sem instalação de servidor de banco: a aplicação cria o esquema e carrega os "
        "dados de demonstração automaticamente na subida. Essa escolha tem uma consequência que precisa "
        "ser explicitada: por ser em memória, todo o conteúdo é descartado ao encerrar a aplicação, o que "
        "é adequado para demonstração e teste, mas incompatível com uso definitivo. A migração para um "
        "SGBD persistente é atividade futura, indicada na Seção 7.")

    par(doc,
        "O esquema físico não é escrito à mão: é gerado pelo Hibernate a partir do mapeamento das "
        "entidades, com ddl-auto=create. O script de carga é executado depois da criação das tabelas, "
        "graças às propriedades defer-datasource-initialization e spring.sql.init.mode=always. A Tabela 16 "
        "reúne as configurações relevantes.")

    legenda_tabela(doc, "Configurações de persistência (application.properties)")
    tabela(doc,
           ["Propriedade", "Valor", "Efeito"],
           [
               ["spring.datasource.url", "jdbc:h2:mem:petcleandb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE",
                "Banco em memória nomeado, preservado enquanto a JVM estiver ativa"],
               ["spring.jpa.hibernate.ddl-auto", "create",
                "Recria o esquema a partir das entidades a cada subida"],
               ["spring.jpa.database-platform", "org.hibernate.dialect.H2Dialect",
                "Dialeto SQL do H2"],
               ["spring.jpa.defer-datasource-initialization", "true",
                "Garante que o script de carga rode depois de o Hibernate criar as tabelas"],
               ["spring.sql.init.mode", "always", "Executa o data.sql em toda subida"],
               ["spring.sql.init.encoding", "UTF-8",
                "Evita a corrupção de acentos do script de carga"],
               ["spring.h2.console.enabled / path", "true / /h2-console",
                "Console web para inspeção das tabelas"],
               ["spring.jpa.show-sql", "true", "Exibe o SQL gerado no log"],
               ["spring.servlet.session.cookie.name", "PETCLEANSESSION", "Nome do cookie de sessão"],
               ["server.servlet.session.cookie.http-only", "true", "Cookie inacessível a scripts da página"],
               ["server.servlet.session.timeout", "60m", "Tempo de inatividade antes de encerrar a sessão"],
               ["spring.servlet.multipart.max-file-size", "2MB",
                "Limite do servlet alinhado à validação de 2 MB da foto de perfil"],
           ],
           larguras=[5.3, 5.2, 6.0], tamanho=8.3)
    fonte(doc, "src/main/resources/application.properties.")

    h2(doc, "5.2 Modelo de dados: entidades, atributos e relacionamentos")

    par(doc,
        "O modelo de dados é composto por seis entidades e sete enumerações. As entidades representam o "
        "tutor e seus pets, os atendimentos agendados, os produtos em estoque, o histórico de movimentações "
        "e os usuários do sistema. As enumerações foram adotadas para todos os campos cujos valores são "
        "fechados - espécie, porte, serviço, status do agendamento, categoria de produto, tipo de "
        "movimentação e perfil de acesso - o que impede a gravação de valores fora do catálogo e permite "
        "que o Swagger liste as opções automaticamente. Todas são gravadas como texto "
        "(@Enumerated(EnumType.STRING)), o que mantém o banco legível no console do H2.")

    figura(doc, "fig02_der.png",
           "diagrama de entidades e relacionamentos do modelo de dados do MVP",
           largura_cm=16.6,
           fonte_texto="Elaborada pelos autores a partir de src/main/java/br/com/fatecmaua/petclean/model/.")

    legenda_tabela(doc, "Entidades, atributos e restrições do modelo")
    tabela(doc,
           ["Entidade (tabela)", "Atributos e restrições relevantes", "Origem no código"],
           [
               ["cliente",
                "id (PK); nome (120, obrigatório); cpf (11, obrigatório e único); telefone (20); "
                "e-mail (120); endereço (200)",
                "model/Cliente.java"],
               ["pet",
                "id (PK); fk_cliente (FK obrigatória); nome (80); espécie (enum); raça (80); "
                "porte (enum); idade (0 a 40)",
                "model/Pet.java"],
               ["agendamento",
                "id (PK); fk_cliente e fk_pet (FK obrigatórias); serviço (enum); data; hora; "
                "valor (10,2); duração em minutos; status (enum); observação (255); atualizado_em; "
                "motivo_cancelamento (255)",
                "model/Agendamento.java"],
               ["produto",
                "id (PK); nome (120); categoria (enum); quantidade; estoque_minimo; preço (10,2); "
                "ativo (padrão verdadeiro)",
                "model/Produto.java"],
               ["movimentacao_estoque",
                "id (PK); fk_produto (FK obrigatória); tipo (enum ENTRADA/SAÍDA); quantidade; "
                "observação (255); registrado_em",
                "model/MovimentacaoEstoque.java"],
               ["usuario",
                "id (PK); nome (120); e-mail (120, obrigatório e único); senha_hash (100, bcrypt); "
                "perfil (enum); telefone (20); nome_petshop (120); endereço (200); foto (LOB); "
                "foto_content_type (60); data_alteracao_senha",
                "model/Usuario.java"],
           ],
           larguras=[3.0, 9.4, 4.1], tamanho=8.3)
    fonte(doc, "src/main/java/br/com/fatecmaua/petclean/model/*.java.")

    legenda_tabela(doc, "Relacionamentos, cardinalidades e regras de integridade")
    tabela(doc,
           ["Relacionamento", "Cardinalidade", "Regra de integridade aplicada"],
           [
               ["cliente -> pet", "1 : N",
                "Um tutor pode ter vários pets; todo pet tem um tutor obrigatório. A exclusão do tutor é "
                "recusada enquanto houver pets vinculados"],
               ["cliente -> agendamento", "1 : N",
                "O agendamento guarda o tutor, mesmo conhecendo o pet, porque a tela precisa exibir os "
                "dois. A exclusão do tutor é recusada enquanto houver agendamentos"],
               ["pet -> agendamento", "1 : N",
                "A exclusão do pet é recusada se houver agendamento futuro (data atual ou posterior, "
                "desde que não cancelado) ou qualquer histórico de atendimento"],
               ["produto -> movimentacao_estoque", "1 : N",
                "Toda entrada e saída é registrada. Produto com histórico não pode ser excluído, apenas "
                "inativado"],
               ["usuario", "Sem relacionamento",
                "A entidade de acesso é independente das demais, o que explica a ausência de separação "
                "dos dados por estabelecimento"],
           ],
           larguras=[3.9, 2.6, 10.0], tamanho=8.3)
    fonte(doc, "model/*.java, service/ClienteService.java, service/PetService.java e service/ProdutoService.java.")

    legenda_tabela(doc, "Enumerações do domínio e valores admitidos")
    tabela(doc,
           ["Enumeração", "Valores", "Uso"],
           [
               ["EspecieEnum", "CACHORRO, GATO, AVE, ROEDOR, REPTIL, OUTRO", "Cadastro de pet (US-07)"],
               ["PorteEnum", "PEQUENO, MEDIO, GRANDE", "Cadastro de pet (US-07)"],
               ["ServicoEnum",
                "BANHO (45 min, R$ 45,00), TOSA (40 min, R$ 50,00), BANHO_E_TOSA (75 min, R$ 85,00), "
                "HIDRATACAO (50 min, R$ 60,00), CONSULTA_VETERINARIA (30 min, R$ 120,00)",
                "Catálogo de serviços; define valor e duração do atendimento (US-11)"],
               ["StatusAgendamentoEnum", "AGENDADO, CONFIRMADO, REALIZADO, CANCELADO",
                "Fluxo do atendimento (US-11 a US-16)"],
               ["CategoriaProdutoEnum", "RACAO, MEDICAMENTO, HIGIENE, BRINQUEDO, ACESSORIO, OUTRO",
                "Classificação do estoque (US-18, US-25)"],
               ["TipoMovimentacaoEnum", "ENTRADA, SAIDA", "Histórico do estoque (US-19)"],
               ["PerfilEnum", "ATENDENTE, GESTOR", "Perfil de acesso exibido na interface"],
           ],
           larguras=[3.4, 8.2, 4.9], tamanho=8.3)
    fonte(doc, "src/main/java/br/com/fatecmaua/petclean/model/*Enum.java.")

    h2(doc, "5.3 Carga inicial e verificação de integridade")

    par(doc,
        "O arquivo data.sql reúne 71 registros de demonstração, usados para que o painel apresente dados "
        "em qualquer execução. As datas dos agendamentos são calculadas de forma relativa, com a função "
        "DATEADD, de modo que o histórico, o dia corrente e os próximos dias permaneçam coerentes "
        "independentemente de quando a aplicação for executada - cuidado necessário porque as séries "
        "temporais do painel dependem desse histórico. Ao final do script, as sequências de identificadores "
        "são reiniciadas para que os vínculos por chave estrangeira continuem válidos.")

    legenda_tabela(doc, "Composição da carga inicial de dados (data.sql)")
    tabela(doc,
           ["Tabela", "Registros", "Observação"],
           [
               ["usuario", "4",
                "Três usuários com a senha petclean123 e um com gestor123; senhas gravadas em hash bcrypt"],
               ["cliente", "8", "Tutores da região do ABC paulista, com CPFs válidos e distintos"],
               ["pet", "10", "Pets distribuídos entre os tutores, com espécies e portes variados"],
               ["agendamento", "24",
                "17 atendimentos no histórico, 3 no dia corrente e 4 nos dias seguintes; datas relativas"],
               ["produto", "10", "Quatro itens em situação de estoque crítico; um item sem movimentação"],
               ["movimentacao_estoque", "15", "Entradas e saídas que compõem o histórico do estoque"],
               ["Total", "71", "Carregados automaticamente a cada subida da aplicação"],
           ],
           larguras=[3.6, 2.2, 10.7], tamanho=9.0)
    fonte(doc, "src/main/resources/data.sql (contagem de instruções insert por tabela).")

    par(doc,
        "A integridade referencial é verificada por regras explícitas de negócio, e não apenas por "
        "restrições do banco. Em todos os casos de violação, a API responde 409 com uma mensagem que "
        "explica o motivo e, quando cabível, indica a alternativa disponível. A Tabela 21 resume as "
        "situações testadas e o comportamento observado.")

    legenda_tabela(doc, "Verificações de integridade e comportamento da API")
    tabela(doc,
           ["Situação", "Comportamento", "Resultado esperado nos testes"],
           [
               ["Exclusão de tutor com pets ou agendamentos",
                "Recusa com 409, informando quantos pets e quantos agendamentos estão vinculados",
                "DELETE /api/clientes/1 -> 409"],
               ["Exclusão de pet com agendamento futuro",
                "Recusa com 409, orientando a cancelar o agendamento antes",
                "DELETE /api/pets/1 -> 409"],
               ["Exclusão de produto com movimentação",
                "Recusa com 409, sugerindo a inativação por PATCH /api/produtos/{id}/inativar",
                "DELETE /api/produtos/1 -> 409"],
               ["Exclusão de produto sem movimentação", "Concluída com 204",
                "DELETE /api/produtos/10 -> 204"],
               ["Cadastro com CPF já existente", "Recusa com 409 e o CPF formatado",
                "POST /api/clientes -> 409"],
               ["Cadastro com CPF de dígito verificador inválido", "Recusa com 422",
                "POST /api/clientes -> 422"],
               ["Agendamento em data passada", "Recusa com 422",
                "POST /api/agendamentos -> 422"],
               ["Agendamento em horário já ocupado", "Recusa com 409, sem gravar",
                "POST /api/agendamentos -> 409"],
               ["Cancelamento de atendimento já realizado", "Recusa com 409",
                "PATCH /api/agendamentos/{id}/cancelar -> 409"],
               ["Saída de estoque acima do disponível", "Recusa com 409, informando o saldo",
                "PATCH /api/produtos/{id}/movimentar -> 409"],
               ["Alteração do perfil de outro usuário", "Recusa com 403",
                "PUT /api/usuarios/2 com sessão do usuário 1 -> 403"],
           ],
           larguras=[5.4, 6.4, 4.7], tamanho=8.3)
    fonte(doc, "testes-api.sh (50 verificações) e src/test/java/.../ApiPetCleanIntegrationTest.java.")

    h2(doc, "5.4 Consultas, repositórios e projeções")

    par(doc,
        "As seis interfaces de repositório estendem JpaRepository, o que fornece as operações básicas sem "
        "que a equipe escreva implementação - não há classe de repositório concreta no projeto. A partir "
        "daí, três níveis de consulta são usados: métodos derivados, em que o nome do método expressa a "
        "consulta; consultas escritas com @Query em HQL, para filtros e contagens; e consultas nativas com "
        "projeções, para as telas de listagem, que trazem apenas as colunas exibidas.")

    legenda_tabela(doc, "Exemplos representativos de consultas da camada de persistência")
    tabela(doc,
           ["Tipo", "Exemplo no repositório", "Finalidade"],
           [
               ["Método derivado", "findByDataOrderByHora(LocalDate data)",
                "Agenda do dia ordenada por horário (US-12)"],
               ["Método derivado", "existsByCpfAndIdNot(String cpf, Long id)",
                "Verificar CPF duplicado na edição, ignorando o próprio registro (US-15)"],
               ["Método derivado", "existsByProduto(Produto produto)",
                "Impedir a exclusão de produto com histórico (US-21)"],
               ["HQL - @Query", "contarConflitosNoHorario(data, hora, idIgnorado)",
                "Conta agendamentos ativos no mesmo dia e horário (US-17)"],
               ["HQL - @Query", "contarAgendamentosFuturosDoPet(idPet, hoje)",
                "Impede a exclusão de pet com atendimento futuro (US-10)"],
               ["HQL - @Query", "listarEstoqueCritico()",
                "Produtos abaixo do mínimo, ordenados do maior para o menor déficit (US-20, US-24)"],
               ["SQL nativo + projeção", "filtrarResumo(termo) em PetRepository",
                "Devolve nome do pet, espécie e nome do tutor para a listagem (US-08)"],
               ["SQL nativo + projeção", "listarResumoDoDia(data) em AgendamentoRepository",
                "Agenda do dia com nomes de cliente, pet e serviço já resolvidos (US-12)"],
               ["SQL nativo + projeção", "contarPorDiaNoPeriodo(inicio, fim)",
                "Agrupamento por dia usado na série semanal e mensal do painel (US-23)"],
               ["Agregação HQL", "valorTotalDoEstoque()",
                "Soma de preço x quantidade para o card de valor de estoque (US-22)"],
           ],
           larguras=[2.8, 6.8, 6.9], tamanho=8.3)
    fonte(doc, "src/main/java/br/com/fatecmaua/petclean/repository/*.java e projection/*.java.")

    par(doc,
        "Cabe destacar uma decisão que revela o cuidado com a modelagem: a ordenação do estoque crítico, "
        "do item com maior falta para o de menor falta, é feita na consulta e não no JavaScript da tela. "
        "Como se trata de uma regra de negócio, ela foi mantida na camada de persistência, onde pode ser "
        "testada independentemente da interface.")

    # =========================================================================
    # 6. ETAPA 4
    # =========================================================================
    h1(doc, "6. ETAPA 4 - DOCUMENTAÇÃO E RELATO DAS AÇÕES E FUNÇÕES DESEMPENHADAS POR CADA "
            "INTEGRANTE DA EQUIPE EXECUTORA DO PROJETO")

    par(doc, "Objetivo: Aplicar técnicas de gerenciamento de equipes a partir de análises das habilidades "
             "técnicas e humanas dos integrantes.", italico=True, depois=8)

    par(doc,
        "Esta seção descreve as ações de cada integrante. A divisão adotada para a apresentação técnica "
        "do sistema é a registrada no material de apresentação da equipe (docs/apresentacao): a Helen "
        "responde pelo bloco de modelos e entidades, o Gabriel pelo bloco de banco de dados e repositórios "
        "e o João Vitor pelo bloco de Swagger, CRUD e endpoints. Essa divisão convive com a atribuição "
        "geral de funções declarada na Seção 2, na qual a Helen coordena as demandas, o Gabriel responde "
        "pelo front-end e pela interface e o João Vitor pelo back-end e pelo banco de dados.")

    h2(doc, "6.1 Helen Aclina")

    par(doc,
        "Função declarada: gerenciamento do projeto, coordenação das demandas e acompanhamento das "
        "entregas, com aplicação de práticas de Scrum e Kanban.")
    marcadores(doc, [
        "Conduziu o planejamento e o acompanhamento das 25 histórias de usuário distribuídas em seis "
        "épicos, mantendo o fluxo de trabalho e as políticas de cada etapa (Seção 3.4).",
        "Respondeu pelo Bloco 01 do material de apresentação da API - Modelos e Entidades (slides 1 a 6), "
        "que descreve a arquitetura em camadas, as seis entidades, as sete enumerações, os "
        "relacionamentos e as regras de integridade referencial.",
        "Acompanhou o registro das decisões e das pendências do projeto, material preservado nos "
        "documentos de docs/ e no README do repositório.",
    ])
    par(doc,
        "Habilidades aplicadas: organização e visão de conjunto do produto; comunicação entre os "
        "integrantes; capacidade de traduzir a rotina do estabelecimento em requisitos verificáveis; "
        "leitura do modelo de dados suficiente para apresentá-lo publicamente.")

    h2(doc, "6.2 Gabriel Wagner")

    par(doc,
        "Função declarada: desenvolvimento do front-end e da interface do sistema.")
    marcadores(doc, [
        "Trabalhou na camada de apresentação, composta por 12 folhas de estilo (3.072 linhas), "
        "11 arquivos JavaScript (1.010 linhas, incluindo o novo api.js), 8 templates Thymeleaf "
        "(1.940 linhas) e 7 páginas públicas, preservando o visual da versão em PHP.",
        "Participou da adaptação dos formulários às exigências da API: inclusão dos campos CPF e "
        "endereço no modal de cliente, de espécie e porte no modal de pet e da conversão da categoria do "
        "estoque de texto livre para lista de seleção.",
        "Respondeu pelo Bloco 02 do material de apresentação da API - Banco de Dados e Repositories "
        "(slides 7 a 10), que descreve o H2, a carga inicial, as interfaces de repositório e as consultas "
        "em HQL, SQL nativo e projeções.",
    ])
    par(doc,
        "Habilidades aplicadas: construção de interfaces com HTML, CSS e JavaScript; atenção à "
        "fidelidade visual na migração; compreensão da camada de persistência a ponto de apresentá-la; "
        "trabalho colaborativo na integração entre tela e API.")

    h2(doc, "6.3 João Vitor")

    par(doc,
        "Função declarada: desenvolvimento do back-end e do banco de dados.")
    marcadores(doc, [
        "Implementou a API REST em Java com Spring Boot: 8 controladores com 48 rotas, 7 serviços de "
        "negócio, 6 repositórios, 5 projeções, 13 DTOs e o tratamento centralizado de erros, totalizando "
        "63 arquivos Java e 4.325 linhas na aplicação.",
        "Modelou e implementou a base persistente: seis entidades, sete enumerações, o esquema gerado "
        "pelo Hibernate e o script de carga com 71 registros de demonstração (Seção 5).",
        "Estruturou a verificação automatizada: 28 testes de integração com MockMvc, 5 testes unitários "
        "de CPF, o script de smoke test com 50 verificações e o validador estático do front-end.",
        "Respondeu pelo Bloco 03 do material de apresentação da API - Swagger, CRUD e Endpoints "
        "Especializados (slides 11 a 15), que descreve a documentação automática, os códigos de status e "
        "os endpoints com regras de negócio.",
    ])
    par(doc,
        "Habilidades aplicadas: programação em Java e no ecossistema Spring; modelagem relacional e "
        "escrita de consultas; automação de testes; documentação técnica de API.")

    h2(doc, "6.4 Síntese da divisão do trabalho, habilidades e dificuldades")

    legenda_tabela(doc, "Divisão do trabalho, artefatos de referência e habilidades mobilizadas")
    tabela(doc,
           ["Integrante", "Função geral", "Bloco técnico apresentado", "Habilidades técnicas",
            "Habilidades humanas"],
           [
               ["Helen Aclina", "Gerenciamento, coordenação das demandas e acompanhamento das entregas",
                "Bloco 01 - Modelos e Entidades (slides 1 a 6)",
                "Leitura de modelo de dados e de arquitetura em camadas",
                "Liderança, organização, mediação e comunicação"],
               ["Gabriel Wagner", "Desenvolvimento do front-end e da interface",
                "Bloco 02 - Banco de Dados e Repositories (slides 7 a 10)",
                "HTML, CSS, JavaScript e Thymeleaf; noções de consultas e repositórios",
                "Atenção a detalhes, colaboração na integração tela-API"],
               ["João Vitor", "Desenvolvimento do back-end e do banco de dados",
                "Bloco 03 - Swagger, CRUD e Endpoints (slides 11 a 15)",
                "Java, Spring Boot, JPA/Hibernate, SQL, testes automatizados e OpenAPI",
                "Autonomia técnica, registro documental e organização de evidências"],
           ],
           larguras=[2.4, 3.8, 3.9, 3.6, 3.0], tamanho=8.0)
    fonte(doc, "Declaração da equipe e docs/apresentacao/README.md (divisão dos blocos da apresentação).")

    par(doc,
        "As principais dificuldades enfrentadas pela equipe estão registradas nos próprios documentos do "
        "projeto e merecem ser relacionadas. A migração de PHP para Java exigiu reescrever a origem dos "
        "dados de todas as telas sem alterar o visual, o que gerou onze incompatibilidades catalogadas e tratadas caso a "
        "caso: cinco foram integralmente resolvidas (campos obrigatórios ausentes nos formulários de cliente e de pet, categoria de estoque como texto livre, ausência de endpoints de perfil e bloqueio indevido de arquivos estáticos pelo interceptor) e as demais foram contornadas com ajuste de interface ou registradas como pendência de "
        "escopo. A página de relatórios chegou a falhar com erro de resposta truncada, causado pela "
        "injeção de valores do servidor em scripts no meio do documento; a correção consistiu em passar "
        "os dados por atributos data-* e lê-los com JSON.parse. Os testes de agendamento falharam quando "
        "as datas fixas usadas nos casos de teste se tornaram passadas, o que levou à substituição por "
        "datas calculadas a partir do dia corrente. Por fim, a ausência de JDK e Maven em um dos "
        "ambientes de trabalho bloqueou parte das validações, que seguem como atividades futuras.")

    # =========================================================================
    # 7. CONCLUSÃO
    # =========================================================================
    h1(doc, "7. CONCLUSÃO")

    par(doc,
        "O PetClean alcançou o objetivo de entregar um MVP funcional para a gestão de um pet shop de "
        "pequeno porte. O sistema cobre, de ponta a ponta, o ciclo que vai do cadastro do tutor e de seus "
        "pets até o atendimento na agenda, passando pelo controle de estoque, pelos alertas de reposição e "
        "pelo painel de indicadores, com acesso protegido por usuário e senha. As 25 histórias de usuário "
        "levantadas na etapa de documentação encontram correspondência em endpoints, regras de negócio e "
        "testes automatizados, o que permitiu à equipe demonstrar rastreabilidade entre o que foi pedido e "
        "o que foi construído.")

    par(doc,
        "Do ponto de vista técnico, o projeto cumpriu as três entregas centrais do modelo institucional. "
        "A base de dados foi modelada em seis entidades e sete enumerações, com relacionamentos e regras "
        "de integridade aplicadas tanto no esquema quanto na camada de negócio. A aplicação foi organizada "
        "em camadas, com separação entre controle, regras de negócio e persistência, o que tornou possível "
        "testar as regras sem subir servidor. A documentação ficou em grande parte automatizada, por meio "
        "do Swagger, e complementada pelos documentos de migração, de validação e de teste mantidos no "
        "repositório.")

    par(doc,
        "A contribuição esperada para a comunidade é oferecer a um pequeno estabelecimento uma "
        "alternativa organizada de gestão, em substituição a planilhas e controles manuais, ao mesmo "
        "tempo em que os alunos aplicaram, em situação real de demanda, os conteúdos de Engenharia de "
        "Software, Banco de Dados, Linguagens de Programação e Gestão de Equipes. Essa contribuição, "
        "porém, ainda é potencial: o sistema foi desenvolvido e validado internamente pela equipe em "
        "ambiente de testes, mas não foi apresentado formalmente ao estabelecimento, não foi implantado "
        "em produção e não contou com a participação dos usuários do pet shop em validações ou na coleta "
        "de feedback. Não há, portanto, resultado medido junto ao beneficiário.")

    par(doc,
        "As dificuldades enfrentadas foram registradas ao longo do relatório e na própria documentação do "
        "projeto: a migração tecnológica de PHP para Java com preservação da interface, o tratamento das "
        "onze incompatibilidades entre as duas versões, a correção da página de relatórios, o ajuste dos "
        "testes que dependiam de datas fixas e a limitação de infraestrutura em um dos ambientes de "
        "desenvolvimento. Cada uma delas foi enfrentada com registro documental da causa e da solução, o "
        "que é, em si, um resultado de aprendizagem para a equipe.")

    par(doc,
        "Como encaminhamentos, a equipe identifica as seguintes atividades futuras, relacionadas por "
        "ordem de prioridade para a continuidade do projeto:")
    marcadores(doc, [
        "Apresentar formalmente o sistema ao pet shop e conduzir uma sessão de validação com os usuários "
        "reais, registrando o retorno recebido - etapa prevista no próprio modelo institucional e ainda "
        "não realizada.",
        "Executar e registrar as validações pendentes: o smoke test de ponta a ponta (V2) e a validação "
        "visual comparada às capturas da versão original (V4).",
        "Migrar a base de dados do H2 em memória para um sistema gerenciador persistente, condição "
        "necessária para qualquer uso definitivo do sistema.",
        "Implementar as funcionalidades previstas e não contempladas no MVP: recuperação de senha, envio "
        "da solicitação de demonstração, persistência das notificações lidas e alimentação por dados "
        "reais dos gráficos que hoje exibem valores fixos.",
        "Aplicar a autorização por perfil, hoje apenas modelada, e avaliar a separação dos dados por "
        "estabelecimento caso o sistema venha a atender mais de um pet shop.",
    ])

    par(doc,
        "O saldo do trabalho é um MVP coerente com o escopo definido, sustentado por código organizado, "
        "testes automatizados e documentação verificável, e com um conjunto de pendências explicitado com "
        "honestidade. A etapa que falta - apresentar o resultado ao estabelecimento e ouvir quem vai "
        "usar o sistema - é justamente a que devolve ao projeto o seu sentido de extensão comunitária.")

    # =========================================================================
    # REFERENCIAS
    # =========================================================================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("REFERÊNCIAS")
    r.font.name = FONTE
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = AZUL

    referencias = [
        "FATEC MAUÁ. Modelo de relatório de Projeto de Extensão Comunitária (Curricularização). "
        "Mauá: Faculdade de Tecnologia de Mauá, [s.d.]. Documento-base estrutural deste relatório "
        "(Modelo_projeto.pdf).",
        "JVITORSI-DEV. PetClean: API REST de gestão para pet shops. 2026. Repositório público. "
        "Disponível em: https://github.com/jvitorsi-dev/PetClean. Acesso em: 10 nov. 2026.",
        "ORACLE. Java 17 Documentation. Disponível em: https://docs.oracle.com/en/java/javase/17/. "
        "Acesso em: 10 nov. 2026.",
        "VMWARE. Spring Boot Reference Documentation (versão 3.5). Disponível em: "
        "https://docs.spring.io/spring-boot/docs/current/reference/html/. Acesso em: 10 nov. 2026.",
        "VMWARE. Spring Data JPA Reference Guide. Disponível em: "
        "https://docs.spring.io/spring-data/jpa/reference/. Acesso em: 10 nov. 2026.",
        "H2 DATABASE ENGINE. H2 Database. Disponível em: https://www.h2database.com/. "
        "Acesso em: 10 nov. 2026.",
        "SPRINGDOC. springdoc-openapi: library for OpenAPI 3 with Spring Boot. Disponível em: "
        "https://springdoc.org/. Acesso em: 10 nov. 2026.",
        "JUNIT. JUnit 5 User Guide. Disponível em: https://junit.org/junit5/docs/current/user-guide/. "
        "Acesso em: 10 nov. 2026.",
        "PHP DOCUMENTATION GROUP. PHP Data Objects (PDO). Disponível em: "
        "https://www.php.net/manual/en/book.pdo.php. Acesso em: 10 nov. 2026.",
    ]
    for ref in referencias:
        pr = doc.add_paragraph()
        pr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pr.paragraph_format.left_indent = Cm(0.0)
        pr.paragraph_format.space_after = Pt(8)
        pr.paragraph_format.line_spacing = 1.4
        rr = pr.add_run(ref)
        rr.font.name = FONTE
        rr.font.size = Pt(11)

    doc.save(SAIDA)
    return SAIDA


if __name__ == "__main__":
    print("gerado:", construir())
