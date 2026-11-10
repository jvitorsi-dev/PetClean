#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera as figuras tecnicas do relatorio de extensao do PetClean.

Todas as informacoes desenhadas foram extraidas do proprio codigo-fonte:
  - camadas  -> src/main/java/br/com/fatecmaua/petclean/*
  - entidades-> src/main/java/br/com/fatecmaua/petclean/model/*
  - fluxo    -> security/InterceptorSeguranca.java, security/SessaoService.java,
                service/AutenticacaoService.java, control/LoginController.java

Uso: python3 gerar_figuras.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(SAIDA, exist_ok=True)

AZUL = "#1F4E79"
AZUL_CLARO = "#DCE6F1"
CINZA = "#5A5A5A"
CINZA_CLARO = "#F2F2F2"
VERDE = "#2E7D52"
VERMELHO = "#B3261E"
LARANJA = "#B26A00"

plt.rcParams["font.family"] = "DejaVu Sans"


def caixa(ax, x, y, w, h, titulo, linhas=None, cor_fundo=AZUL_CLARO,
          cor_borda=AZUL, cor_titulo="white", tam_titulo=10.5, tam_linha=8.3,
          raio=0.10, titulo_fundo=None):
    """Caixa com faixa de titulo e linhas de texto."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={raio}",
                                linewidth=1.1, edgecolor=cor_borda, facecolor=cor_fundo, zorder=2))
    # faixa do titulo
    faixa_h = min(0.30, h * 0.42)
    ax.add_patch(FancyBboxPatch((x, y + h - faixa_h), w, faixa_h,
                                boxstyle=f"round,pad=0.0,rounding_size={raio}",
                                linewidth=0, edgecolor="none",
                                facecolor=titulo_fundo or cor_borda, zorder=3))
    ax.add_patch(plt.Rectangle((x, y + h - faixa_h + 0.001), w, faixa_h / 2,
                               linewidth=0, facecolor=titulo_fundo or cor_borda, zorder=3))
    ax.text(x + w / 2, y + h - faixa_h / 2, titulo, ha="center", va="center",
            color=cor_titulo, fontsize=tam_titulo, fontweight="bold", zorder=4)
    if linhas:
        topo = y + h - faixa_h - 0.10
        for i, texto in enumerate(linhas):
            ax.text(x + 0.08, topo - i * 0.185, texto, ha="left", va="top",
                    color="#20303A", fontsize=tam_linha, zorder=4, linespacing=1.25)
    return (x, y, w, h)


def seta(ax, p1, p2, cor=CINZA, estilo="-", texto=None, desloc=(0, 0), raio=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.25, color=cor, linestyle=estilo,
                                 shrinkA=2, shrinkB=2, zorder=1,
                                 connectionstyle=f"arc3,rad={raio}"))
    if texto:
        mx = (p1[0] + p2[0]) / 2 + desloc[0]
        my = (p1[1] + p2[1]) / 2 + desloc[1]
        ax.text(mx, my, texto, ha="center", va="center", color=cor, fontsize=8,
                fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.95))


# =============================================================================
# FIGURA 1 - Arquitetura em camadas
# =============================================================================
def figura_arquitetura():
    fig, ax = plt.subplots(figsize=(9.6, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    ax.text(5, 7.85, "Arquitetura em camadas da solucao PetClean",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=AZUL)

    L = 1.05
    W = 5.4
    H = 0.95

    camadas = [
        (6.75, "1. Cliente (navegador)", ["Paginas Thymeleaf  +  HTML/CSS/JS  (fetch para /api/**)"], "#E8F1E4", VERDE),
        (5.45, "2. Camada de controle -  control/", ["8 @RestController (48 rotas REST)  +  2 @Controller (9 paginas)",
                                                     "Bean Validation (@Valid)  |  HandlerInterceptor de seguranca"], AZUL_CLARO, AZUL),
        (4.15, "3. Camada de servico -  service/", ["7 @Service: regras de negocio das 25 historias de usuario",
                                                    "Transacoes (@Transactional)  |  ValidacaoCpf (digito verificador)"], "#FFF2CC", LARANJA),
        (2.85, "4. Camada de persistencia -  repository/", ["6 interfaces JpaRepository: query methods, @Query HQL e SQL nativo",
                                                            "5 projections (consultas otimizadas)"], AZUL_CLARO, AZUL),
        (1.55, "5. Banco de dados", ["H2 em memoria  (jdbc:h2:mem:petcleandb)  -  schema gerado por ddl-auto=create"], "#EDE7F6", "#5B3A9E"),
    ]
    for y, titulo, linhas, fundo, borda in camadas:
        caixa(ax, L, y, W, H, titulo, linhas, cor_fundo=fundo, cor_borda=borda,
              titulo_fundo=borda, tam_titulo=9.8, tam_linha=8.0)

    for i in range(len(camadas) - 1):
        y_top = camadas[i][0]
        y_bot = camadas[i + 1][0] + H
        ax.annotate("", xy=(L + W / 2, y_bot + 0.03), xytext=(L + W / 2, y_top - 0.03),
                    arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.3))

    # caixas transversais
    caixa(ax, 6.95, 5.30, 2.85, 1.30, "Transversal: seguranca",
          ["InterceptorSeguranca (US-02)", "SessaoService (HttpSession)", "UsuarioSessao + bcrypt (RNF-04)"],
          cor_fundo="#FDECEA", cor_borda=VERMELHO, titulo_fundo=VERMELHO, tam_titulo=9.0, tam_linha=7.8)
    caixa(ax, 6.95, 3.95, 2.85, 1.10, "Transversal: contratos",
          ["13 DTOs (records) validados", "ErroResposta + GlobalExceptionHandler"],
          cor_fundo=CINZA_CLARO, cor_borda=CINZA, titulo_fundo=CINZA, tam_titulo=9.0, tam_linha=7.8)
    caixa(ax, 6.95, 2.60, 2.85, 1.10, "Transversal: documentacao",
          ["Swagger UI (/swagger-ui.html)", "springdoc-openapi 2.8.13"],
          cor_fundo="#E8F1E4", cor_borda=VERDE, titulo_fundo=VERDE, tam_titulo=9.0, tam_linha=7.8)
    caixa(ax, 6.95, 1.40, 2.85, 1.00, "Transversal: carga inicial",
          ["data.sql - 71 registros (UTF-8)"],
          cor_fundo="#EDE7F6", cor_borda="#5B3A9E", titulo_fundo="#5B3A9E", tam_titulo=9.0, tam_linha=7.8)

    ax.text(5, 0.46, "Pacote-base: br.com.fatecmaua.petclean  |  Spring Boot 3.5.16 (Java 17)  |  "
                     "H2 em memoria  |  48 rotas REST",
            ha="center", va="center", fontsize=7.6, color="#555555", style="italic")

    fig.tight_layout()
    caminho = os.path.join(SAIDA, "fig01_arquitetura.png")
    fig.savefig(caminho, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return caminho


# =============================================================================
# FIGURA 2 - Diagrama de entidades e relacionamentos
# =============================================================================
def figura_der():
    fig, ax = plt.subplots(figsize=(10.4, 7.4))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 9.6)
    ax.axis("off")

    ax.text(6.1, 9.30, "Modelo de dados do PetClean: entidades e relacionamentos",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=AZUL)

    CINZA_ENT = ("#F7F9FB", "#4A6D8C")

    def ent(nome, x, y, w, attrs):
        h = 0.40 + 0.195 * len(attrs)
        caixa(ax, x, y, w, h, nome, attrs, cor_fundo=CINZA_ENT[0], cor_borda=CINZA_ENT[1],
              titulo_fundo=CINZA_ENT[1], tam_titulo=9.6, tam_linha=7.7, raio=0.07)
        return (x, y, w, h)

    # linha superior
    c = ent("cliente", 0.30, 6.15, 2.85, ["id (PK)", "nome", "cpf (UNIQUE, 11)", "telefone", "email", "endereco"])
    p = ent("pet", 4.65, 6.15, 2.85, ["id (PK)", "fk_cliente (FK)", "nome", "especie", "raca", "porte", "idade"])
    a = ent("agendamento", 9.00, 6.15, 3.05,
            ["id (PK)", "fk_cliente (FK)", "fk_pet (FK)", "servico", "data", "hora", "valor",
             "duracao_minutos", "status", "observacao", "atualizado_em", "motivo_cancelamento"])
    # linha inferior
    pr = ent("produto", 0.30, 1.35, 2.85, ["id (PK)", "nome", "categoria", "quantidade", "estoque_minimo", "preco", "ativo"])
    mv = ent("movimentacao_estoque", 4.65, 1.35, 2.85,
             ["id (PK)", "fk_produto (FK)", "tipo", "quantidade", "observacao", "registrado_em"])
    us = ent("usuario", 9.00, 1.35, 3.05,
             ["id (PK)", "nome", "email (UNIQUE)", "senha_hash (bcrypt)", "perfil", "telefone",
              "nome_petshop", "endereco", "foto (LOB)", "data_alteracao_senha"])

    # cliente 1:N pet
    seta(ax, (c[0] + c[2], c[1] + c[3] / 2), (p[0], p[1] + p[3] / 2), cor=CINZA, texto="1 : N")
    # pet 1:N agendamento
    seta(ax, (p[0] + p[2], p[1] + p[3] / 2), (a[0], a[1] + a[3] / 2), cor=CINZA, texto="1 : N")
    # cliente 1:N agendamento (rota inferior)
    y_rota = 5.72
    ax.plot([c[0] + c[2] / 2, c[0] + c[2] / 2, a[0] + a[2] / 2, a[0] + a[2] / 2],
            [c[1], y_rota, y_rota, a[1]], color=CINZA, lw=1.25, zorder=1)
    ax.add_patch(FancyArrowPatch((a[0] + a[2] / 2, y_rota + 0.02), (a[0] + a[2] / 2, a[1] - 0.03),
                                 arrowstyle="-|>", mutation_scale=13, color=CINZA, lw=1.25, zorder=1))
    ax.text((c[0] + a[0] + a[2]) / 2, y_rota, "1 : N", ha="center", va="center", fontsize=8,
            fontweight="bold", color=CINZA, zorder=5,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.95))
    # produto 1:N movimentacao
    seta(ax, (pr[0] + pr[2], pr[1] + pr[3] / 2), (mv[0], mv[1] + mv[3] / 2), cor=CINZA, texto="1 : N")

    # usuario isolado
    ax.text(us[0] + us[2] / 2, 0.92, "entidade de acesso - sem vinculo com as demais (limitacao registrada: ausencia de multi-tenant)",
            ha="center", va="center", fontsize=7.5, color=VERMELHO, style="italic")

    # legenda
    ax.text(6.1, 0.60,
            "PK = chave primaria (GenerationType.IDENTITY)   |   FK = chave estrangeira (ManyToOne, obrigatoria)   |   "
            "Schema gerado pelo Hibernate (spring.jpa.hibernate.ddl-auto=create)",
            ha="center", va="center", fontsize=7.4, color="#555555")
    ax.text(6.1, 0.30, "Esquema fisico gerado pelo Hibernate a partir do mapeamento JPA (ddl-auto=create).",
            ha="center", va="center", fontsize=7.4, color="#555555", style="italic")

    fig.tight_layout()
    caminho = os.path.join(SAIDA, "fig02_der.png")
    fig.savefig(caminho, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return caminho


# =============================================================================
# FIGURA 3 - Fluxo de autenticacao e protecao de rotas
# =============================================================================
def figura_auth():
    fig, ax = plt.subplots(figsize=(10.0, 6.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.6)
    ax.axis("off")

    ax.text(6, 8.25, "Autenticacao e protecao de rotas (US-01, US-02 e US-14)",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color=AZUL)

    # coluna esquerda: acesso a rota protegida
    caixa(ax, 0.30, 6.55, 3.10, 1.05, "Requisicao para /api/** ou /paginas/*.html",
          ["Navegador (Accept: text/html)  |  Cliente de API (Accept: application/json)"],
          cor_fundo=AZUL_CLARO, cor_borda=AZUL, titulo_fundo=AZUL, tam_titulo=8.8, tam_linha=7.6)

    # losango de decisao
    dx, dy, dw, dh = 1.05, 4.55, 1.60, 1.30
    ax.add_patch(Polygon([[dx + dw / 2, dy + dh], [dx + dw, dy + dh / 2], [dx + dw / 2, dy], [dx, dy + dh / 2]],
                         closed=True, facecolor="#FFF2CC", edgecolor=LARANJA, lw=1.2, zorder=2))
    ax.text(dx + dw / 2, dy + dh / 2, "Existe\nUsuarioSessao\nna HttpSession?", ha="center", va="center",
            fontsize=7.6, color="#5C4100", zorder=4, fontweight="bold", linespacing=1.25)

    ax.annotate("", xy=(dx + dw / 2, dy + dh + 0.05), xytext=(1.85, 6.50),
                arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.3))

    # sim
    caixa(ax, 0.15, 2.85, 3.05, 0.72, "Acesso permitido", ["preHandle() retorna true"],
          cor_fundo="#E8F1E4", cor_borda=VERDE, titulo_fundo=VERDE, tam_titulo=8.6, tam_linha=7.6)

    # nao - navegador
    caixa(ax, 3.55, 4.70, 3.30, 1.42, "Navegador: HTTP 302",
          ["SessaoService.registrarRotaPendente(rota)", "redireciona para GET /login", "apos autenticar, volta a rota pedida"],
          cor_fundo="#FFF2CC", cor_borda=LARANJA, titulo_fundo=LARANJA, tam_titulo=8.8, tam_linha=7.6)

    # nao - API
    caixa(ax, 3.55, 2.35, 3.30, 1.42, "Cliente de API: HTTP 401",
          ["ErroNegocioException(UNAUTHORIZED)", "JSON ErroResposta { status, erro, mensagem, ... }"],
          cor_fundo="#FDECEA", cor_borda=VERMELHO, titulo_fundo=VERMELHO, tam_titulo=8.8, tam_linha=7.6)

    ax.annotate("", xy=(3.50, 5.41), xytext=(dx + dw, dy + dh / 2),
                arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.25))
    ax.text(3.30, 5.72, "nao + text/html", fontsize=7.4, color=CINZA, ha="right", va="center")
    ax.annotate("", xy=(3.50, 3.06), xytext=(dx + dw, dy + dh / 2),
                arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.25))
    ax.text(3.30, 3.86, "nao + JSON", fontsize=7.4, color=CINZA, ha="right", va="center")
    ax.annotate("", xy=(1.67, 3.60), xytext=(dx + dw / 2, dy),
                arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.25))
    ax.text(1.95, 4.15, "sim", fontsize=7.4, color=CINZA, ha="left", va="center")

    # coluna direita: login
    caixa(ax, 7.40, 6.55, 4.25, 1.05, "POST /login  { email, senha }",
          ["LoginRequest com @NotBlank e @Email (@Valid)"],
          cor_fundo=AZUL_CLARO, cor_borda=AZUL, titulo_fundo=AZUL, tam_titulo=8.8, tam_linha=7.6)

    caixa(ax, 7.40, 4.95, 4.25, 1.35, "AutenticacaoService.autenticar()",
          ["UsuarioRepository.findByEmailIgnoreCase()", "BCryptPasswordEncoder.matches(senha, senha_hash)",
           "incompativel: 401 Credenciais invalidas"],
          cor_fundo="#FDECEA", cor_borda=VERMELHO, titulo_fundo=VERMELHO, tam_titulo=8.8, tam_linha=7.6)

    caixa(ax, 7.40, 3.15, 4.25, 1.55, "SessaoService.autenticar()",
          ["HttpSession.setAttribute(USUARIO_AUTENTICADO, UsuarioSessao)",
           "UsuarioSessao = (id, nome, email, perfil) - sem senha",
           "cookie PETCLEANSESSION, HttpOnly, timeout 60 min"],
          cor_fundo="#E8F1E4", cor_borda=VERDE, titulo_fundo=VERDE, tam_titulo=8.8, tam_linha=7.6)

    caixa(ax, 7.40, 1.75, 4.25, 1.16, "Resposta 200 - LoginResponse",
          ["{ usuario, rotaPendente, mensagem }", "rotaPendente consumida uma unica vez da sessao"],
          cor_fundo="#EDE7F6", cor_borda="#5B3A9E", titulo_fundo="#5B3A9E", tam_titulo=8.8, tam_linha=7.6)

    ax.annotate("", xy=(9.52, 6.50), xytext=(9.52, 6.32), arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.3))
    ax.annotate("", xy=(9.52, 4.90), xytext=(9.52, 4.72), arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.3))
    ax.annotate("", xy=(9.52, 3.10), xytext=(9.52, 2.94), arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.3))
    # login -> voltar a rota
    ax.annotate("", xy=(6.90, 5.41), xytext=(7.36, 2.33),
                arrowprops=dict(arrowstyle="-|>", color=VERDE, lw=1.3, linestyle="--",
                                connectionstyle="arc3,rad=0.18"))
    ax.text(5.92, 4.28, "retorna a\npagina pedida", fontsize=7.4, color=VERDE, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.95))

    # logout
    caixa(ax, 0.15, 1.75, 3.05, 0.80, "POST /logout (US-14)", ["HttpSession.invalidate() -> 204"],
          cor_fundo=CINZA_CLARO, cor_borda=CINZA, titulo_fundo=CINZA, tam_titulo=8.6, tam_linha=7.6)
    ax.annotate("", xy=(1.67, 2.80), xytext=(1.67, 2.58), arrowprops=dict(arrowstyle="-|>", color=CINZA, lw=1.2))

    ax.text(6, 1.05,
            "Perfis previstos no modelo (PerfilEnum: ATENDENTE, GESTOR) sao exibidos na interface; "
            "o interceptor valida apenas autenticacao, nao autorizacao por perfil.",
            ha="center", va="center", fontsize=7.5, color=VERMELHO, style="italic",
            bbox=dict(boxstyle="round,pad=0.22", fc="#FDECEA", ec="none", alpha=0.9))
    ax.text(6, 0.44, "Classes envolvidas: security/InterceptorSeguranca.java, security/SessaoService.java, "
                     "service/AutenticacaoService.java, control/LoginController.java.",
            ha="center", va="center", fontsize=7.3, color="#555555", style="italic")

    fig.tight_layout()
    caminho = os.path.join(SAIDA, "fig03_autenticacao.png")
    fig.savefig(caminho, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return caminho


if __name__ == "__main__":
    for f in (figura_arquitetura, figura_der, figura_auth):
        print("gerado:", f())
