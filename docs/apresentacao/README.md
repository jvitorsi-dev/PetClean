# Apresentação — API do PetClean

Material de apresentação do back-end (API REST) do PetClean, usado no Projeto
Interdisciplinar. O visual segue o front do próprio sistema: cartões brancos de
cantos arredondados, rosa `#FF8C94`, menta `#A8E6CE`, pêssego `#FFD3B5`, fundo
claro e a fonte **Poppins** — os mesmos tokens de `static/css/menus-globais.css`
e `static/css/dashboard.css`. As ilustrações (logotipo, ícones do menu e os
avatares dos integrantes) são os arquivos originais de `static/assets`.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| **`PetClean-API.pptx`** | Apresentação editável (15 slides, 16:9) com **notas do apresentador** em cada slide e a marcação de quem fala. |
| **`index.html`** | Versão para navegador, pixel a pixel igual aos slides. Abra no Chrome/Edge e use `←` `→` para navegar, `N` para ver o roteiro e `F` para tela cheia. Funciona offline. |
| **`ROTEIRO.md`** | Roteiro de fala completo, bloco por bloco, com o tempo alvo de cada slide. |
| `assets/`, `fontes/` | Imagens e a fonte Poppins usadas pelos dois formatos (nada depende de internet). |
| `gerador/` | Código que gera o `.pptx`, o `index.html` e o `ROTEIRO.md`. |

## Roteiro: 15 minutos, três blocos iguais

| Bloco | Integrante | Slides | Tempo |
|---|---|---|---|
| **01 · Modelos e Entidades** | Helen Aclina | 1 — 6 | 4:40 (janela 0:00 — 5:00) |
| **02 · Banco de Dados e Repositories** | Gabriel Wagner | 7 — 10 | 4:40 (janela 5:00 — 10:00) |
| **03 · Swagger, CRUD e Endpoints** | João Vitor Silva | 11 — 15 | 4:40 (janela 10:00 — 15:00) |

Os tempos por slide somam **14:00**; o minuto restante cobre as duas trocas de
apresentador. Cada bloco abre com um slide-divisor que anuncia quem assume.

### Slide a slide

| # | Slide | Quem | ⏱ |
|---|---|---|---|
| 01 | Capa | Helen | 0:30 |
| 02 | Roteiro dos três blocos | Helen | 0:40 |
| 03 | Arquitetura em camadas | Helen | 0:50 |
| 04 | Modelos e Entidades (6 entidades + 7 enums) | Helen | 1:20 |
| 05 | Relacionamentos e integridade referencial | Helen | 0:50 |
| 06 | A entidade `Pet` no código | Helen | 0:30 |
| 07 | **Divisor — Bloco 02** | Gabriel | — |
| 08 | Banco de Dados H2 e `data.sql` | Gabriel | 1:25 |
| 09 | Repositories (Spring Data JPA) | Gabriel | 1:30 |
| 10 | HQL, SQL nativo e projections | Gabriel | 1:25 |
| 11 | **Divisor — Bloco 03** | João Vitor | — |
| 12 | Swagger / OpenAPI | João Vitor | 1:30 |
| 13 | Operações CRUD e status HTTP | João Vitor | 1:30 |
| 14 | Endpoints especializados | João Vitor | 1:00 |
| 15 | Fechamento: os seis requisitos | João Vitor | 0:30 |

## Cobertura dos requisitos

| Requisito do trabalho | Onde aparece |
|---|---|
| **Modelos/Entidades** | slides 04, 05 e 06 — `Cliente`, `Pet`, `Agendamento`, `Produto`, `MovimentacaoEstoque`, `Usuario` |
| **Banco de Dados (H2)** | slide 08 — datasource em memória, console web, `ddl-auto` e `data.sql` |
| **Repositories** | slides 09 e 10 — as 6 interfaces `JpaRepository`, query methods e `@Query` |
| **Swagger / OpenAPI** | slide 12 — `SwaggerConfig`, springdoc, esquema de sessão por cookie |
| **Operações CRUD** | slide 13 — POST/GET/PUT/DELETE com 201, 200, 204 e os erros 400/401/404/409/422 |
| **Endpoints especializados** | slide 14 — filtros, agenda do dia, conflito de horário, estoque crítico e dashboard |

As 7 tags de domínio reúnem 43 endpoints; os 5 do perfil do usuário formam a
oitava tag, totalizando **48 rotas REST** (os controllers também servem as 8
páginas Thymeleaf do painel, que não entram nessa conta).

Todos os números citados saíram do próprio repositório: 6 entidades, 7 enums,
6 repositories, 5 projections, 48 endpoints REST e 71 registros no `data.sql`
(8 clientes, 10 pets, 10 produtos, 15 movimentações, 24 agendamentos e 4
usuários).

## Como abrir

- **PowerPoint / LibreOffice / Google Slides** — abra `PetClean-API.pptx`; as
  notas do apresentador estão em *Exibir › Anotações*.
- **Navegador** — abra `index.html` (funciona offline). Setas navegam, `N` mostra
  o roteiro do slide, `F` entra em tela cheia. Para imprimir/exportar em PDF, use
  `Ctrl+P` (o CSS já define uma página por slide).

## Como regerar

A apresentação é gerada por código, então qualquer ajuste é feito nos arquivos
de `gerador/` e o material é reconstruído:

```bash
pip install python-pptx pillow fonttools brotli
python gerador/make.py       # gera PetClean-API.pptx, index.html e preview/
python gerador/roteiro.py    # gera ROTEIRO.md
```

| Arquivo | Conteúdo |
|---|---|
| `gerador/engine.py` | Motor de desenho: um modelo de elementos renderizado em PPTX e em HTML. |
| `gerador/deck.py` | Conteúdo dos 15 slides + notas do apresentador. |
| `gerador/roteiro.py` | Exporta as notas para `ROTEIRO.md`. |
| `gerador/preview.py` | Pré-visualização em PNG e checagem de texto que estoura a caixa. |

Para editar texto à mão, o `.pptx` é um arquivo comum do PowerPoint: tudo é
caixa de texto nativa, exceto as ilustrações (logotipo, ícones e avatares).

## Dicas para a apresentação

- Abra o **`index.html`** no navegador do projetor se quiser garantir que as
  fontes e o layout fiquem idênticos aos slides; use o `.pptx` se precisar
  editar ou quiser as anotações na tela do apresentador.
- O momento de maior impacto é uma demonstração de 40 segundos do
  `http://localhost:8080/swagger-ui.html` logo depois do slide 12, com a
  aplicação rodando via `./mvnw spring-boot:run`.
- Os tempos estão nas notas de cada slide — use a tela do apresentador com
  cronômetro.
