# Relatório do Projeto de Extensão Comunitária (Curricularização) — PetClean

Entrega final: **`Relatorio_PetClean_Projeto_Extensao.docx`**

Documento redigido a partir da análise integral do código-fonte deste repositório e da estrutura
definida em `Modelo_projeto.pdf` (FATEC Mauá — Curso Superior de Tecnologia em Desenvolvimento de
Software Multiplataforma).

## Estrutura

Mantém as sete seções obrigatórias do modelo, com capa, sumário, tabelas numeradas, figuras,
paginação (a partir da Seção 1) e referências:

| Seção | Conteúdo |
|---|---|
| 1 | Características do Projeto de Extensão (ficha institucional preenchida) |
| 2 | Informações da Equipe de Trabalho |
| 3 | Etapa 1 — Documentação de Engenharia de Software (regras de negócio, épicos/US, RNF, Scrum e Kanban) |
| 4 | Etapa 2 — Programação, teste e implantação em ambiente de testes do MVP (arquitetura, PHP → Java, endpoints, segurança, testes) |
| 5 | Etapa 3 — Modelagem, implementação e teste da base persistente (H2, DER, carga inicial, consultas) |
| 6 | Etapa 4 — Relato das ações e funções de cada integrante |
| 7 | Conclusão |

Subtópicos: 3.1 a 3.4, 4.1 a 4.4, 5.1 a 5.4 e 6.1 a 6.4, conforme o modelo.

## Como regenerar

```bash
python3 -m venv .venv && .venv/bin/pip install matplotlib python-docx
cd docs/relatorio
.venv/bin/python gerar_figuras.py     # figuras em figuras/*.png
.venv/bin/python gerar_relatorio.py   # gera o .docx
```

| Arquivo | Função |
|---|---|
| `gerar_figuras.py` | Desenha as três figuras (arquitetura em camadas, DER e fluxo de autenticação) com matplotlib |
| `gerar_relatorio.py` | Monta o DOCX: estilos, capa, campo de sumário, 23 tabelas, 3 figuras, rodapé com paginação e referências |
| `figuras/` | PNGs gerados (300 dpi) |

## Observações de uso

- **Sumário:** gerado por campo automático do Word/LibreOffice. Se abrir vazio, selecione todo o
  documento (`Ctrl+A`) e pressione `F9` (Word) ou use *Ferramentas › Atualizar › Índices*
  (LibreOffice).
- **Rastreabilidade:** todos os números citados (63 arquivos Java, 4.325 linhas, 48 rotas REST,
  25 histórias, 34 testes, 71 registros no `data.sql`, 12 CSS, 1.010 linhas de JS, 1.940 linhas de
  templates) foram conferidos diretamente no repositório.
- **Situação declarada:** o relatório registra que o sistema foi desenvolvido e validado apenas
  internamente pela equipe em ambiente de testes, sem apresentação formal ao estabelecimento, sem
  implantação em produção e sem validação por usuários.
