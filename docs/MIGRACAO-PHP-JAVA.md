# Migração PetClean — PHP puro → API Java (Spring Boot)

Documento de acompanhamento da migração do front-end PHP (PDO + `$_SESSION` + `fetch/FormData`)
para a API Java já existente neste repositório, **preservando a interface visual original**.

> Regra central: o HTML/CSS/JS original foi preservado. O que mudou é **de onde os dados vêm**
> (antes: consultas PDO dentro de cada `.php`; agora: `services` Java + Thymeleaf) e **para onde
> os formulários vão** (antes: `php/*.php`; agora: `/api/**`).

---

## 1. Estratégia adotada

| Item | Antes (PHP) | Depois (Java) |
| --- | --- | --- |
| Renderização | `<?php echo ?>`, `foreach`, `if` dentro do HTML | Thymeleaf (`th:text`, `th:each`, `th:if`) — **mesmo HTML emitido** |
| Sessão | `$_SESSION['usuario']` | `HttpSession` + `USUARIO_AUTENTICADO` (já existente na API) |
| Dados | `PDO`/`SELECT` dentro da página | `*Service` injetados no `PaginaPainelController` |
| AJAX | `fetch("../php/x.php", {body: FormData})` | `fetch("/api/x", {body: JSON})` via `js/api.js` |
| Atualização da tela | `window.location.reload()` | **mantido** (mesmo comportamento) |
| Mensagens | `alert()` / `confirm()` | **mantidos** com os textos originais |
| Rotas | `paginas/*.php` | `paginas/*.html` (61 links internos reescritos) |

Única dependência nova: `spring-boot-starter-thymeleaf` (renderização server-side, sem SPA e sem
reescrever os 8 templates como JavaScript).

---

## 2. A. Diagnóstico

### 2.1 Acervo recebido
- 4 dumps `.md` com todo o código PHP (páginas do painel, páginas públicas, `php/` de apoio).
- 18 folhas CSS (4.635 linhas), 11 arquivos JS (865 linhas), 17 imagens + 18 capturas de tela.
- Capturas tiradas com a UI a **75%** (sidebar 256 px, header 88,80 px) — comparar renderizando a 75 %.

### 2.2 Chamadas AJAX encontradas no PHP (20 endpoints fictícios)
`clientes/{salvar,editar,excluir}`, `pets/{salvar,editar,excluir}`,
`estoque/{salvar,editar,excluir}`, `agendamentos/{salvar,editar,excluir}`,
`login/enviar`, `autenticacao/{logout,recuperar}`, `notificacoes/{listar,marcar-lidas}`,
`perfil/{atualizar-cadastro,alterar_senha}`, `solicitar-demo/processar-solicitacao`.

### 2.3 Estado do painel antes desta etapa
Nenhum `css/`, `js/`, `assets/` ou `templates/` existia no repositório (nem no histórico do Git):
os arquivos chegaram por upload e **não** persistiam entre sessões — motivo pelo qual foram
copiados para dentro de `src/main/resources/`.

---

## 3. B. Matriz de rastreabilidade

### 3.1 Páginas

| # | Arquivo PHP original | Rota nova | Template / arquivo | Fonte de dados (Java) | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | `index.php` / `inicio.php` | `/paginas/inicio.html` | `static/paginas/inicio.html` | estática | ✅ |
| 2 | `sobrenos.php` | `/paginas/sobrenos.html` | `static/paginas/sobrenos.html` | estática | ✅ |
| 3 | `funcionalidades.php` | `/paginas/funcionalidades.html` | `static/paginas/funcionalidades.html` | estática | ✅ |
| 4 | `faleconosco.php` | `/paginas/faleconosco.html` | `static/paginas/faleconosco.html` | `js/faleconosco.js` (sem backend) | ✅ |
| 5 | `solicitar-demo.php` | `/paginas/solicitar-demo.html` | `static/paginas/solicitar-demo.html` | — | ⚠️ I6 (sem endpoint) |
| 6 | `login.php` | `/paginas/login.html` (+ `GET /login` → 302) | `static/paginas/login.html` | `POST /login` | ✅ |
| 7 | `recuperar-senha.php` | `/paginas/recuperar-senha.html` | (idem) | — | ⚠️ I6 (sem endpoint) |
| 8 | `paginas/dashboard.php` | `/paginas/dashboard.html` | `templates/paginas/dashboard.html` | `Cliente/Pet/AgendamentoService` | ✅ |
| 9 | `paginas/relatorios.php` | `/paginas/relatorios.html` | `templates/paginas/relatorios.html` | 4 contadores + 5 gráficos | 🟡 |
| 10 | `paginas/clientes.php` | `/paginas/clientes.html` | `templates/paginas/clientes.html` | `ClienteService` | ✅ leitura / ⚠️ I2 gravação |
| 11 | `paginas/pets.php` | `/paginas/pets.html` | `templates/paginas/pets.html` | `PetService`, `ClienteService` | ✅ leitura / ⚠️ I3 gravação |
| 12 | `paginas/estoque.php` | `/paginas/estoque.html` | `templates/paginas/estoque.html` | `ProdutoService` | ✅ leitura / ⚠️ I4 gravação |
| 13 | `paginas/agendamentos.php` | `/paginas/agendamentos.html` | `templates/paginas/agendamentos.html` | `AgendamentoService`, `PetService` | ✅ |
| 14 | `paginas/perfil.php` | `/paginas/perfil.html` | `templates/paginas/perfil.html` | sessão | ✅ (API própria do perfil) |
| 15 | `paginas/configuracoes.php` | `/paginas/configuracoes.html` | `templates/paginas/configuracoes.html` | sessão | ✅ |

### 3.2 Chamadas AJAX → endpoints reais

| Chamada original | Endpoint usado | Observação |
| --- | --- | --- |
| `login/enviar.php` | `POST /login` | `password` → `senha`; FormData → JSON; usa `rotaPendente` |
| `autenticacao/logout.php` | `POST /logout` | 204 e redireciona para `login.html` |
| `clientes/salvar.php` | `POST /api/clientes` | ⚠️ I2 |
| `clientes/editar.php` | `PUT /api/clientes/{id}` | ⚠️ I2 |
| `clientes/excluir.php` | `DELETE /api/clientes/{id}` | ⚠️ I7 (API devolve 409 se houver pets) |
| `pets/salvar.php` / `editar.php` | `POST /api/pets` / `PUT /api/pets/{id}` | ⚠️ I3 |
| `pets/excluir.php` | `DELETE /api/pets/{id}` | 409 quando há agendamentos |
| `estoque/salvar.php` / `editar.php` | `POST /api/produtos` / `PUT /api/produtos/{id}` | ⚠️ I4 (categoria texto → enum) |
| `estoque/excluir.php` | `DELETE /api/produtos/{id}` | 409 com movimentações |
| `agendamentos/salvar.php` | `POST /api/agendamentos` | cliente obtido de `GET /api/pets/{id}` |
| `agendamentos/editar.php` | `PUT /api/agendamentos/{id}` | conflito de horário → 409 |
| `agendamentos/excluir.php` | `DELETE /api/agendamentos/{id}` | ✅ |
| `notificacoes/listar.php` | `GET /api/produtos/estoque-critico` + `GET /api/agendamentos/agenda?data=hoje` | alertas derivados de dados reais |
| `notificacoes/marcar-lidas.php` | — | sem persistência: `sessionStorage` |
| `perfil/atualizar-cadastro.php` | `PUT /api/usuarios/{id}` | ✅ |
| `perfil/alterar_senha.php` | `PUT /api/usuarios/{id}/senha` | ✅ |
| `solicitar-demo/processar-solicitacao.php` | — | ⚠️ I6 (sem endpoint) |
| `autenticacao/recuperar.php` | — | ⚠️ I6 (sem endpoint) |

### 3.3 Incompatibilidades registradas (I1–I11)

| ID | Incompatibilidade | Tratamento nesta etapa |
| --- | --- | --- |
| I1 | API não é multi-tenant (`usuario_id`) | dados globais; documentado |
| I2 | `ClienteRequest` exige `cpf` e `endereco`; o formulário original não os possui | **resolvido**: campos CPF e Endereço adicionados ao modal (`D1`, seção 9) |
| I3 | `PetRequest` exige `especie` e `porte` (ausentes no formulário) | **resolvido**: selects de Espécie e Porte adicionados ao modal (`D1`) |
| I4 | `categoria` é enum no Java e `varchar(50)` livre no PHP | **resolvido**: o campo virou lista de seleção com as 6 categorias (seção 9.2) |
| ~~I5~~ | ~~Sem endpoints de perfil, foto, senha~~ | **resolvido**: `Usuario` ganhou `telefone`, `nomePetshop`, `endereco`, `foto` e `dataAlteracaoSenha`; a API expõe `GET|PUT /api/usuarios/{id}`, `PUT /api/usuarios/{id}/senha` e `POST|GET /api/usuarios/{id}/foto`, e a tela de Perfil voltou a salvar |
| I6 | Sem recuperação de senha / SMTP / demonstração | idem I5 |
| I7 | PHP fazia *cascade*; a API responde **409** | mensagem real da API exibida |
| I8 | `cargo` PHP (`Administrador`/`Demonstração`) ≠ `PerfilEnum` (`Atendente`/`Gestor`) | exibe a descrição real do perfil |
| I9 | Interceptor bloqueava `/css`, `/js`, `/assets` → 401 | liberados em `ConfiguracaoWeb` |
| I10 | Guarda de sessão no PHP (`$_SESSION`) | `GET /api/sessao` / 401 tratado em `api.js` |
| I11 | `relatorios.php` tem 5 gráficos com valores fixos e sem endpoint | mantidos fixos (como no original); apenas o donut usa `totalTutores` |

---

## 4. C. Implementação

### 4.1 Arquivos criados

```
src/main/resources/
├── static/
│   ├── css/            12 folhas do projeto original (as 6 "mortas" ficaram de fora)
│   ├── js/             10 arquivos originais + api.js (novo)
│   ├── assets/         imagens + icones/*.png
│   └── paginas/        7 páginas públicas (.html)
├── templates/paginas/  8 páginas do painel (.html + Thymeleaf)
src/main/java/.../control/PaginaPainelController.java   (novo)
docs/MIGRACAO-PHP-JAVA.md                               (este arquivo)
```

### 4.2 Arquivos alterados

| Arquivo | Alteração |
| --- | --- |
| `pom.xml` | + `spring-boot-starter-thymeleaf` |
| `application.properties` | locale `pt_BR` fixo (R$ 1.234,56) e cache de template desligado |
| `security/ConfiguracaoWeb.java` | `/css/**`, `/js/**`, `/assets/**` e as 7 páginas públicas liberadas |
| `security/InterceptorSeguranca.java` | mantém o 302 para `/login` (contrato da US-02), que encaminha o navegador para `paginas/login.html` |
| `control/PaginaController.java` | `GET /login` agora redireciona para a página original de login |
| `static/js/*.js` | URLs `../php/*.php` → API REST (JSON); mantidos `alert`, `confirm` e `reload()` |
| `templates/paginas/configuracoes.html` | corrigido `</spa n>` (erro de digitação do PHP original que quebrava o layout) |
| `templates/paginas/relatorios.html` | script dos gráficos com `th:inline="javascript"` e array do donut corrigido |
| `mvnw` | permissão de execução |

### 4.3 Como o Thymeleaf foi aplicado
- `<?php echo $x; ?>` → `[[${x}]]` (texto) ou `th:text` / `th:value` / `th:data-*` (atributos);
- `foreach` → `th:each` (inclusive nas `<option>` dos selects);
- `if (empty($lista))` → `th:if` na linha "nenhum registro encontrado";
- `if (!empty($fotoPerfil))` → `th:block th:if/th:unless` (avatar com foto ou inicial);
- `json_encode($array)` nos gráficos → `th:inline="javascript"` com `/*[[${...}]]*/`;
- `number_format($x, 2, ',', '.')` → `#numbers.formatDecimal(x, 1, 2)` com locale `pt_BR`;
- `date('d/m/Y', strtotime($x))` → `#temporals.format(x, 'dd/MM/yyyy')`.

Nenhuma classe CSS, cor, fonte, ícone ou espaçamento foi alterado. As classes sem regra no CSS
original (`.fundo-rosa-topo`, `.seta`, `.container10` …) continuam sem regra — são apenas hooks.

---

## 5. D. Validação funcional

> **Status: APROVADA em 07/11/2026** (`mvnw.cmd clean test`, Windows, Java 17.0.12).
> A primeira execução deu **28 testes / 2 falhas** (nenhum erro de compilação); as duas falhas foram
> investigadas e corrigidas (abaixo) e a re-execução terminou em **BUILD SUCCESS, 28 testes,
> 0 falhas, 0 erros**. Depois disso entraram **6 testes da tela de Perfil** (dados, senha, foto,
> 403 e 422), totalizando **34**. A validação visual (V4) segue pendente.

**Falhas encontradas e corrigidas**

| Teste | Causa | Correção | Situação |
| --- | --- | --- | --- |
| `navegacaoSemSessaoRedireciona` | eu havia trocado o 302 do interceptor de `/login` para `/paginas/login.html` | interceptor voltou a redirecionar para `/login` (o contrato da US-02); quem encaminha para a página é o próprio `GET /login` | ✅ passou |
| `conflitoDeHorario` | **pré-existente e alheia à migração**: o teste usava a data fixa `2026-11-05`, que passou a ser data passada (a API recusa com 422) | as 4 datas literais dos testes de agendamento passaram a ser calculadas por `LocalDate.now().plusDays(7)` (`DATA_FUTURA`) | ✅ passou |

### 5.1 O que foi verificado estaticamente (executado de fato)
- 0 blocos PHP remanescentes nos 8 templates (`grep -rn "<?php\|<?=\|endforeach\|endif"` → vazio).
- Todas as variáveis usadas nos templates existem no `PaginaPainelController` (checagem por script).
- Todas as propriedades acessadas existem nas entidades (`a.pet.nome`, `p.estoqueCritico`, …).
- HTML balanceado nos 15 arquivos (só o `</spa n>` original estava quebrado — corrigido).
- 0 referências locais quebradas (`../css`, `../js`, `../assets`).
- Sintaxe dos 11 arquivos JS validada com `node --check` (0 erros), inclusive os scripts inline.

### 5.2 Roteiro de teste a executar (pendente)
```bash
./mvnw spring-boot:run      # http://localhost:8080
# 1) http://localhost:8080/paginas/login.html  (helen@petclean.com / petclean123)
# 2) após o login: dashboard → clientes → pets → estoque → agendamentos → relatórios → perfil
# 3) CRUD: cliente, pet, produto, agendamento (editar e excluir)
# 4) notificações (sino) e logout
# 5) curl -c cookies -X POST localhost:8080/login -H 'Content-Type: application/json' \
#         -d '{"email":"helen@petclean.com","senha":"petclean123"}'
bash testes-api.sh          # smoke test das 25 US da API
```

Casos de erro esperados (e documentados, não corrigidos): CPF/endereço ausentes (I2),
espécie/porte ausentes (I3), categoria inválida (I4), 409 ao excluir com vínculos (I7).

---

## 6. E. Validação visual

> **Status: PENDENTE** — depende do servidor em execução (item D). Comparação a ser feita com as
> 18 capturas de referência, renderizando o navegador a **75 %** (as capturas foram tiradas nessa
> escala) e com massa de dados equivalente (`LOLA`, `POPY`, shampoo — 1 registro por tabela).

Procedimento: abrir cada uma das 15 páginas, capturar a tela a 75 %, sobrepor com a captura de
referência correspondente e conferir: sidebar 256 px, header 88,80 px, `#FF8C94`, cards com raio
16 px, sombra `0 1px 3px rgba(0,0,0,.05)`, Poppins, ícones `assets/icones/*.png`.

Diferenças previstas e já justificadas (não são regressões de layout):
1. legenda do perfil mostra o perfil real (`Atendente`/`Gestor`) e não `Demonstração` (I8);
2. campos de perfil/telefone/petshop vazios — a API não tem essas colunas (I5);
3. números de dashboard/relatórios refletem o `data.sql` da API (8 clientes, 10 pets, 10 produtos)
   e não a massa da captura.

---

## 7. F. Pendências

| ID | Pendência | Impacto | Precisa de decisão |
| --- | --- | --- | --- |
| D1 | ~~Formulários sem `cpf`+`endereco`, `especie`+`porte` e `categoria` livre~~ | **resolvido na seção 9** | não |
| D2 | Perfil, foto, senha, recuperação e demonstração sem endpoint | botões avisam que o recurso não existe na API | **sim** — criar endpoints ou aceitar como fora de escopo |
| D3 | Ausência de multi-tenant (`usuario_id`) | todos os usuários veem a mesma base | **sim** — fora de escopo declarado |
| — | Acentuação do `data.sql` no Windows: o log do Hibernate no run do usuário mostrou `'SiamÃªs'`, `'RaÃ§Ã£o'` | pode ser só o console ou mojibake real (Java 17 no Windows lê o script com o charset da plataforma) — **verificar na tela de estoque**; se estiver corrompido, renomear `data.sql` → `data.sql` (o `spring.sql.init.encoding=UTF-8` já está configurado) | **sim** |
| — | Chart.js vinha de CDN (`cdn.jsdelivr.net`) | biblioteca servida localmente em `static/js/vendor/chart.umd.min.js` (v4.6.1); nenhuma mudança visual |
| — | Página de relatórios em branco com `ERR_INCOMPLETE_CHUNKED_ENCODING` | **resolvido e confirmado pelo usuário em 07/11/2026.** Causa: a inlining de JavaScript do Thymeleaf (`<script th:inline="javascript">` + `/*[[${...}]]*/`) falhava **no meio do documento** — depois de o buffer de 8 KB já ter sido enviado, o que cortava a resposta (daí o erro de *chunked encoding* em vez de um 500 limpo). Os valores passaram a ir em atributos `data-*` (JSON serializado no controller para o dashboard) e o JS lê por `dataset` + `JSON.parse` |
| — | `HIDRATACAO` existe no enum e não no PHP | serviço novo aparece na API mas não no select (mantido como o original) | não |
| — | Validação funcional (D) e visual (E) | bloqueadas pelo ambiente (sem JDK/Maven) | executar localmente |

---

## 8. G. Execução

```bash
./mvnw spring-boot:run          # aplicação em http://localhost:8080
# páginas do painel:  /paginas/dashboard.html, clientes.html, pets.html, estoque.html,
#                     agendamentos.html, relatorios.html, perfil.html, configuracoes.html
# site público:       /paginas/inicio.html
# API/Swagger:        /swagger-ui.html   |   console H2: /h2-console
```

Credenciais de demonstração (`data.sql`): `helen@petclean.com` / `petclean123` (Atendente),
`gestor@petclean.com` / `gestor123` (Gestor).

---

## 9. Resolução de D1 (campos obrigatórios)

Implementado o "Fix 1 + 2 + 3(a)" aprovado:

| Arquivo | Alteração |
| --- | --- |
| `templates/paginas/clientes.html` | + campos **CPF** (`maxlength=14`) e **Endereço** (`maxlength=200`); `th:data-cpf` / `th:data-endereco` no botão Editar |
| `templates/paginas/pets.html` | + selects **Espécie** (6 opções) e **Porte** (3 opções, com acentuação "Médio"); `th:data-especie` / `th:data-porte` |
| `control/PaginaPainelController.java` | `especies`, `portes` e `portesLabel` no modelo da página de pets |
| `static/js/clientes.js` | envia `cpf` (máscara 000.000.000-00 na edição) e `endereco` no JSON |
| `static/js/pets.js` | preenche e envia `especie` e `porte` |
| `static/js/estoque.js` | envia o valor do `<select>` de categoria (o mapa de conversão de texto foi removido) |

**Impacto visual (mínimo e inevitável):** os dois modais ficaram mais altos (cliente 3→5 campos,
pet 4→6 campos, ~+155 px cada). Nenhuma regra de CSS foi criada ou alterada; foram reutilizadas as
classes `.form-modal-group` e o estilo inline já usado pelo `<select>` do tutor. Em viewports com
menos de ~650 px de altura útil o modal pode encostar nas bordas — correção opcional de 1 linha em
`perfil.css` (`.modal-box { max-height: 90vh; overflow-y: auto; }`), **não aplicada**.

### 9.2 Categoria do estoque: campo de texto → lista de seleção (opção A)

Confirmado no código da API: `categoria` é o enum `CategoriaProdutoEnum` (6 valores) e o
`ProdutoRequest` a exige como `@NotNull`. O PHP original a tratava como texto livre
(`categoria varchar(50) NOT NULL`), com um `<input>` cujo placeholder sugeria "Alimentos" e
"Farmácia" — valores que **não existem** no contrato. Por isso o campo virou `<select>`:

```html
<select id="prod-categoria" name="categoria" required>
    <option value="">Selecione...</option>
    <option th:each="cat : ${categorias}" th:value="${cat.name()}"
            th:text="${categoriasLabel[cat.name()]}"></option>
</select>
```

| Item | Detalhe |
| --- | --- |
| Arquivos | `templates/paginas/estoque.html`, `PaginaPainelController.estoque()` (`model.addAttribute("categorias", CategoriaProdutoEnum.values())`), `static/js/estoque.js` |
| Estilo | inline, idêntico ao `<select>` do tutor/serviço (`border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px`) — **nenhuma regra de CSS criada ou alterada** |
| Rótulos | `Ração`, `Medicamento`, `Higiene`, `Brinquedo`, `Acessório`, `Outro` (acentuados, como no banco original) |
| Edição | o botão Editar já traz `th:data-categoria="${p.categoria.name()}"`, que casa com o `value` da opção |
| Divergência | **deliberada** em relação à captura PHP (input → select); justificada pelo enum da API e registrada aqui |
| Ganho | elimina digitação inválida e o mapa de conversão de grafia que existia no JS |

**Captura / pré-visualização:** ver `docs/preview/modal-cliente.html`, `docs/preview/modal-pet.html`
e `docs/preview/modal-estoque.html`
— páginas estáticas com o **markup real dos modais** e o **CSS real do projeto** (dados de exemplo),
usadas para conferir o resultado sem precisar subir o servidor. Não é a aplicação em execução.

---
