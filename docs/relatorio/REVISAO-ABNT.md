# Revisão acadêmica e adequação à ABNT — Relatório PetClean

Revisão integral do relatório do Projeto de Extensão Comunitária (Curricularização) da FATEC Mauá,
realizada segundo as normas **NBR 14724** (trabalhos acadêmicos), **NBR 6023** (referências),
**NBR 6024** (numeração progressiva), **NBR 6027** (sumário), **NBR 6028** (resumo) e
**NBR 10520** (citações).

Entrega revisada: **`Relatorio_PetClean_Projeto_Extensao.docx`**

---

## 1. Principais alterações realizadas

### 1.1 Elementos estruturais

| Alteração | Antes | Depois | Norma |
|---|---|---|---|
| Resumo e palavras-chave | inexistentes | incluídos em folha própria, parágrafo único, espaço simples, 5 palavras-chave separadas por ponto e vírgula | NBR 6028 / NBR 14724 |
| Sumário | título numerado como seção | título sem numeração, em folha própria, antes do texto | NBR 6027 |
| Numeração das seções | `1. CARACTERÍSTICAS...` | `1 CARACTERÍSTICAS...` (sem ponto após o último algarismo) | NBR 6024 |
| Capa | título com hífen e sem natureza do trabalho | instituição, curso, título, subtítulo, natureza do trabalho, integrantes, local e ano | NBR 14724 |
| Referências | 9 entradas, nenhuma citada no texto | 12 entradas, todas citadas, em ordem alfabética, espaço simples, alinhadas à esquerda | NBR 6023 |

### 1.2 Formatação

| Item | Antes | Depois |
|---|---|---|
| Recuo da primeira linha | inexistente | 1,25 cm em todos os parágrafos do corpo |
| Espaçamento do corpo | 1,5 | mantido em 1,5 (exigência da NBR 14724) |
| Títulos das seções | Arial 14/12, azul | Arial 12, negrito, preto, espaço simples |
| Corpo do texto | Arial 12 | Arial 12, justificado |
| Margens | 3 / 2 / 3 / 2 cm | mantidas e conferidas nas duas seções do documento |
| Resumo | — | espaço simples, sem recuo |
| Referências | espaço 1,4 | espaço simples, sem recuo, 6 pt entre entradas |

### 1.3 Tabelas

| Item | Antes | Depois |
|---|---|---|
| Identificação | `Tabela 1 - Título` (hífen) | `Tabela 1 – Título` (travessão), acima da tabela |
| Fonte | abaixo, sem padronização | abaixo, padronizada: "Fonte: Elaborada pelos autores (2026), com base em …" ou "Fonte: Dados informados pela equipe (2026)." |
| Bordas | grade completa | apenas três traços horizontais: topo, sob o cabeçalho e base |
| Cabeçalho | faixa azul com texto branco | faixa cinza-clara com texto preto em negrito |
| Corpo | 8,3 a 9 pt | 9 pt, espaço simples |

### 1.4 Figuras

| Item | Antes | Depois |
|---|---|---|
| Identificação | abaixo, com hífen | abaixo da ilustração, com travessão (`Figura 1 – …`), conforme a NBR 14724 |
| Fonte | ausente ou parcial | presente nas três figuras, centralizada, 9 pt |

### 1.5 Citações e referências

- Inseridas **12 citações indiretas** no sistema autor-data, nos pontos em que o texto se apoia em
  fonte externa (Java, Spring Boot, Spring Data JPA, Spring Security, H2, Thymeleaf, springdoc,
  JUnit, PDO/PHP, MySQL e o próprio repositório).
- **Correspondência verificada**: 12 citações ↔ 12 referências, sem citação órfã e sem referência
  não citada.
- Entradas de autor repetido desambiguadas por letras: ORACLE 2026a/2026b e VMWARE 2026a/2026b/2026c.
- Local desconhecido indicado como `[S.l.]` e data desconhecida como `[s.d.]` (modelo institucional).
- Nenhuma referência foi inventada: todos os endereços eletrônicos correspondem à documentação
  oficial das tecnologias efetivamente utilizadas no projeto.

### 1.6 Conteúdo e coerência

| Alteração | Justificativa |
|---|---|
| Contextualização do problema na Seção 1 | a abertura passou a apresentar o problema (dependência de planilhas e controles manuais), com apoio no material de divulgação do sistema |
| Objetivo geral e objetivos específicos na Seção 1 | antes apenas transcritos da ficha; agora explicitados e articulados com as quatro etapas |
| Caracterização metodológica na Seção 1 | pesquisa aplicada, descritiva, estudo de caso único, desenvolvimento iterativo e incremental |
| Eliminação de repetições | a declaração sobre o estágio do projeto ("não apresentado ao estabelecimento / não implantado em produção / sem validação com usuários") aparecia três vezes de forma idêntica; foi mantida integralmente na Seção 1 e condensada nas Seções 4.4 e 7 |
| Correção de imprecisões | "34 testes… cobrindo as histórias US-01 a US-25" → casos distribuídos entre os seis épicos e a tela de perfil; "50 verificações, uma por história" → organizadas história por história |
| Padronização terminológica | "scripts" → "roteiros de verificação"; "templates" → "modelos de página"; "enum" → "enumeração"; "multi-inquilino" mantido onde tecnicamente necessário |
| Aberturas de parágrafo variadas | três parágrafos iniciavam com expressões idênticas da família "sob o aspecto…" |
| Aspas tipográficas | mensagens da API passaram a usar aspas curvas (“ ”) em vez de aspas retas |
| Conclusão | reescrita para responder explicitamente aos objetivos, sem alterar o teor nem acrescentar resultados não verificados |

### 1.7 Preservação

Nada foi inventado. Foram mantidos integralmente:

- as **sete seções** exigidas pelo modelo institucional, na mesma ordem;
- os **subtópicos 3.1 a 3.4, 4.1 a 4.4, 5.1 a 5.4 e 6.1 a 6.4**;
- as **23 tabelas** com todos os seus dados técnicos — extraídas mecanicamente da versão anterior
  para `tabelas.json` e reinseridas sem alteração de conteúdo;
- as **3 figuras**, apenas com adequação de legenda e fonte;
- os nomes dos integrantes, as tecnologias e todos os números técnicos conferidos no código-fonte.

---

## 2. Pendências que dependem de informação adicional

| # | Pendência | Impacto | Como resolver |
|---|---|---|---|
| 1 | Ano do modelo institucional da FATEC Mauá | referência registrada como `[s.d.]` | informar o ano do documento para substituir `[s.d.]` |
| 2 | Titularidade formal do repositório | a referência está em nome do usuário do GitHub (`JVITORSI-DEV`) | decidir se a entrada deve ser em nome dos três autores ou institucional |
| 3 | Folha de rosto | não incluída; a NBR 14724 a torna obrigatória em trabalhos acadêmicos | se exigida, informar o nome do professor orientador para compor a folha |
| 4 | Número de WhatsApp dos integrantes | células da Tabela 2 em branco | informar os números ou confirmar que permanecem em branco |
| 5 | Resumo em língua estrangeira (abstract) | não incluído | exigido para TCC e pós-graduação; para relatório de extensão é facultativo — confirmar com a coordenação |
| 6 | Listas de figuras e de tabelas | não incluídas | são opcionais; recomendáveis se a banca as exigir |
| 7 | Seções primárias em folha própria | as sete seções permanecem em sequência contínua, como no modelo institucional | se o avaliador exigir a regra da NBR 14724 (início em nova folha), a alteração é de uma linha no gerador |
| 8 | Confirmação dos endereços eletrônicos | URLs e datas de acesso foram registrados conforme a documentação oficial vigente | conferir se a instituição exige outro formato de apresentação para documentos eletrônicos |

**Nenhuma dessas pendências foi resolvida por suposição.** Todas dependem de decisão ou dado da
equipe.

---

## 3. Avaliação final de conformidade

### 3.1 Estrutura

| Elemento | Situação |
|---|---|
| Capa | **Conforme** — instituição, curso, título, subtítulo, natureza, autoria, local e ano |
| Folha de rosto | **Não incluída** — depende do nome do orientador (pendência 3) |
| Resumo e palavras-chave | **Conforme** |
| Sumário | **Conforme** — campo automático, atualizável pelo editor |
| Introdução | **Adequada à natureza do trabalho** — a contextualização foi incorporada à Seção 1, preservando a estrutura de sete seções do modelo institucional |
| Objetivos | **Conforme** — geral e específicos explicitados e coerentes com o executado |
| Fundamentação teórica | **Não aplicável** — relatório de atividade de extensão em modelo institucional; não foi criado capítulo teórico para não descaracterizar o trabalho nem exigir citações que a equipe não produziu |
| Metodologia | **Conforme** — caracterização metodológica na Seção 1 + procedimentos descritos em cada etapa |
| Desenvolvimento | **Conforme** — sequência lógica nas Seções 3 a 6 |
| Resultados e discussão | **Adequados** — resultados apresentados nas Seções 4.4, 5.3 e 5.4, com distinção explícita entre o verificado e o pendente |
| Considerações finais | **Conforme** — responde aos objetivos propostos |
| Referências | **Conforme** — 12 entradas, todas citadas, NBR 6023 |

### 3.2 Formatação

| Critério | Situação |
|---|---|
| Fonte Arial 12 no corpo | **Conforme** |
| Margens 3 / 2 / 3 / 2 cm | **Conforme** |
| Espaçamento 1,5 no corpo; simples em resumo, legendas, fontes e referências | **Conforme** |
| Recuo de 1,25 cm na primeira linha | **Conforme** |
| Alinhamento justificado | **Conforme** |
| Numeração progressiva (NBR 6024) | **Conforme** |
| Paginação a partir da primeira folha do texto, sem numeração na capa e nos elementos pré-textuais | **Conforme** |
| Títulos de tabelas acima e fontes abaixo | **Conforme** |
| Títulos de figuras abaixo e fontes depois | **Conforme** |
| Tabelas sem linhas verticais | **Conforme** |

### 3.3 Conteúdo e coerência

- **Coerência interna**: referências cruzadas a tabelas e figuras verificadas automaticamente —
  todas apontam para elementos existentes.
- **Veracidade**: mantida a declaração de que o sistema não foi apresentado formalmente ao
  estabelecimento, não foi implantado em produção e não possui validação com usuários.
- **Rastreabilidade**: 48 rotas REST, 25 histórias, 34 testes, 71 registros de carga, 63 arquivos
  Java e 4.325 linhas — todos os números conferidos no código-fonte, sem alteração.

### 3.4 Conclusão da avaliação

O documento encontra-se **conforme às normas da ABNT nos elementos obrigatórios para a natureza do
trabalho** e preserva integralmente a estrutura de sete seções exigida pelo modelo institucional da
FATEC Mauá. As oito pendências listadas na Seção 2 são decisões ou dados da equipe — não falhas de
revisão — e nenhuma delas foi resolvida por suposição.

---

## 4. Como regenerar

```bash
python3 -m venv .venv && .venv/bin/pip install matplotlib python-docx
cd docs/relatorio
.venv/bin/python gerar_figuras.py     # figuras (300 dpi)
.venv/bin/python gerar_relatorio.py   # DOCX revisado
```

| Arquivo | Função |
|---|---|
| `gerar_relatorio.py` | Gerador do DOCX (estilos ABNT, capa, resumo, sumário, seções, referências) |
| `tabelas.json` | Conteúdo das 23 tabelas, preservado da versão anterior e reinserido sem alteração |
| `gerar_figuras.py` | Desenho das três figuras com matplotlib |
| `figuras/` | PNGs em 300 dpi |
