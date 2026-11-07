# Guia de validação — migração PHP → Java

Como rodar **cada** validação, na ordem, com o resultado esperado. Nada aqui foi executado no
ambiente de desenvolvimento da migração (sem JDK/Maven e sem navegador); é o roteiro para rodar na
sua máquina. Registre as evidências no fim do arquivo.

---

## 0. Pré-requisitos

| Requisito | Como conferir |
| --- | --- |
| JDK 17+ | `java -version` → `openjdk version "17"` (ou superior) |
| Internet no primeiro build | baixa o Maven 3.9.16 (wrapper) e as dependências |
| Navegador | Chrome/Edge/Firefox atualizado |
| Opcional | Node (checagem de sintaxe JS) e Python 3 (checagens de HTML) |

Maven **não** é necessário: o projeto traz o wrapper. No Windows use `mvnw.cmd`; no Linux/macOS
`./mvnw` (o bit de execução já está no repositório).

---

## V1 — Compilação e testes unitários

```bash
./mvnw clean test
```

**Esperado:** `BUILD SUCCESS` e `Tests run: 28, Failures: 0, Errors: 0, Skipped: 0`.

> Primeira execução (07/11/2026): 28 testes, **2 falhas** — `navegacaoSemSessaoRedireciona`
> (redirect do interceptor, já corrigido) e `conflitoDeHorario` (data fixa `2026-11-05` que virou
> passado; agora os testes usam `LocalDate.now().plusDays(7)`). Detalhes na seção 5 do
> `docs/MIGRACAO-PHP-JAVA.md`.

| Suíte | Testes | Cobre |
| --- | --- | --- |
| `ApiPetCleanIntegrationTest` | 22 | US-01 a US-25 (contrato, códigos de status, sessão) |
| `ValidacaoCpfTest` | 5 | normalização e dígito verificador |
| `PetCleanApplicationTests` | 1 | contexto Spring sobe |

Relatório detalhado: `target/surefire-reports/*.txt`.
Se falhar por download, confira proxy/VPN: o build precisa de `repo.maven.apache.org`.

---

## V2 — Smoke test dos endpoints (API pura)

```bash
# terminal 1
./mvnw spring-boot:run          # sobe em http://localhost:8080

# terminal 2
bash testes-api.sh
```

**Esperado:** todas as linhas `OK`, contagem final sem `FAIL`.

O script usa um cookie jar e cria registros no banco em memória. Para zerar a massa, pare a
aplicação e suba de novo (`ddl-auto=create` recria e o `data.sql` repopula).

---

## V3 — Validação funcional do painel (manual)

Suba a aplicação e abra **http://localhost:8080/paginas/login.html**.
Senha de todos: `petclean123` (exceto `gestor@petclean.com` → `gestor123`).

| # | Passo | Esperado |
| --- | --- | --- |
| 1 | Abrir `/paginas/clientes.html` sem sessão | 302 → login; **após entrar, volta para clientes** (`rotaPendente`) |
| 2 | Login com senha errada | caixa `#mensagem-erro` na própria tela (não é `alert`), texto da API |
| 3 | Login com `helen@petclean.com` | cai no dashboard; 4 cards + 3 gráficos (Chart.js via CDN) |
| 4 | Clientes → "Novo Cliente" com CPF `529.982.247-25` | `alert` de sucesso + `reload` com a linha nova |
| 5 | Mesmo CPF de novo | `alert` com a mensagem real: **409** `CPF ja cadastrado: ...` |
| 6 | CPF `111.222.333-44` | **422** `CPF invalido` (dígito verificador) |
| 7 | Deixar nome com 2 letras | **400** com `detalhes: ["nome: o nome deve ter entre 3 e 120 caracteres"]` |
| 8 | Pets → salvar sem espécie/porte | o `required` do `<select>` impede o envio |
| 9 | Pets → editar e salvar | sucesso; `reload` mantém a tabela |
| 10 | Estoque → categoria fora da lista | impossível pelo `<select>` (6 opções) |
| 11 | Estoque → produto com `quantidade < estoque_minimo` | linha destacada em vermelho + sino com alerta |
| 12 | Agendamentos → data no passado | **422** `Nao e possivel agendar para uma data passada` |
| 13 | Agendamentos → mesmo horário/serviço | **409** conflito de horário |
| 14 | Excluir cliente que tem pets | **409** (o PHP fazia cascade; a API bloqueia) |
| 15 | Sino de notificações | lista estoque crítico + agenda de hoje; "Marcar todas" limpa a badge |
| 16 | Sair pelo menu | `POST /logout` → volta ao login; abrir uma página do painel redireciona |

> Item 17 (conhecido): em **Configurações → "Invalidar Todas as Sessões"** o botão ainda aponta para
> `../php/configuracoes/invalidar-sessoes.php` e leva a 404. É o único link `.php` vivo; o
> comportamento original equivale a `POST /logout`.

Códigos de status da API, para conferência: **400** validação de campos (`@Valid`),
**401** sem sessão/senha errada, **404** id inexistente, **409** duplicidade/vínculo/conflito de
horário, **422** regra de negócio (CPF inválido, data passada, pet de outro tutor).

---

## V4 — Validação visual contra as 18 capturas (75 %)

As capturas de referência foram tiradas com a **UI a 75 %** (sidebar 256 px, header 88,80 px).
Comparar sem ajustar a escala produz falso negativo.

1. Guarde as capturas fora do Git (ex.: `docs/referencia/`, adicionado ao `.gitignore`).
2. Abra a página e aplique **75 %**: DevTools → Console → `document.body.style.zoom = 0.75`
   (ou menu do navegador → Zoom → 75 %). Largura de janela de referência: **1440 px**.
3. Meça com o inspetor (Computed):

| Elemento | Esperado |
| --- | --- |
| `.sidebar` | `width: 256px` |
| `.top-header` | `height: 88.8px` |
| `.card`, `.main-table-container` | `border-radius: 16px`, `border: 0.8px #E5E7EB`, `box-shadow: 0 1px 3px rgba(0,0,0,.05)`, `padding: 24px` |
| `.menu-item.active` | fundo `#FFF5F5` + barra 3 px `#FF8C94` |
| Fonte | `Poppins` (painel) |
| Cor primária | `#FF8C94` |

4. Páginas a fotografar (15): `inicio`, `sobrenos`, `funcionalidades`, `faleconosco`,
   `solicitar-demo`, `login`, `recuperar-senha`, `dashboard`, `relatorios`, `clientes`, `pets`,
   `estoque`, `agendamentos`, `perfil`, `configuracoes`.
5. Os **3 modais alterados** (D1) têm pré-visualização própria, também a 75 %:
   `docs/preview/modal-cliente.html`, `docs/preview/modal-pet.html`, `docs/preview/modal-estoque.html`.
6. Massa de dados: as capturas mostram ~1 registro por tabela (LOLA, POPY, shampoo); o `data.sql`
   traz 8 clientes / 10 pets / 10 produtos. Para comparar 1:1, filtre pela busca
   (`/paginas/clientes.html?busca=Maria`) em vez de alterar o banco.
7. Divergências **esperadas** (não são regressões): cargo exibido como Atendente/Gestor;
   campos de perfil vazios; números do dashboard vindos do `data.sql`; categoria do estoque como
   `select`; modais de cliente/pet ~155 px mais altos.

---

## V5 — Checagens estáticas (sem servidor, ~5 s)

```bash
bash validar-estatico.sh
```

**Esperado:** `Falhas: 0`. Ele verifica: resíduo de PHP, links `.php` ativos, chamadas mapeadas para
a API, sintaxe dos JS (se houver Node), HTML balanceado, variáveis de template com origem no
controller, referências locais quebradas e presença dos 15 arquivos de página.

Hoje ele reporta **1 aviso** — exatamente o botão de invalidar sessões citado no item 17 do V3.

---

## Registro de evidências

| Validação | Data | Resultado | Evidência |
| --- | --- | --- | --- |
| V1 testes | | | saída do `mvnw test` |
| V2 smoke | | | saída do `testes-api.sh` |
| V3 funcional | | | tabela acima anotada |
| V4 visual | | | `docs/referencia/*.png` (não versionado) |
| V5 estático | | | saída do `validar-estatico.sh` |

Ao concluir, atualize as seções 5 e 6 de `docs/MIGRACAO-PHP-JAVA.md` marcando o que foi executado.
