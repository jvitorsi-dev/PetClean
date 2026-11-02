# PetClean — API REST de Gestão para Pet Shops

Projeto Java **Spring Boot** construído a partir do relatório de *Gestão Ágil de Projetos de Software*
(Kanban + XP aplicados à gestão do PetClean). Implementa os **6 épicos** e as **25 histórias de usuário**
descritas no documento, com os critérios de aceitação *Dado/Quando/Então* verificados por testes.

Segue o mesmo modelo do projeto de referência (`projeto-musica`): mesmas camadas
(`model`, `repository`, `projection`, `control`, `swagger`), Spring Data JPA, banco H2 em memória,
`import.sql` para a carga inicial e springdoc/Swagger UI para documentação.

---

## 1. Como executar

Pré-requisitos: **JDK 17+** (Maven não é necessário — o projeto traz o wrapper).

```bash
# Windows
mvnw.cmd spring-boot:run

# Linux / macOS
./mvnw spring-boot:run
```

Depois de subir, acesse:

| Recurso | URL |
|---|---|
| Portal do projeto (página inicial) | http://localhost:8080/ |
| Swagger UI (todos os endpoints) | http://localhost:8080/swagger-ui.html |
| OpenAPI JSON | http://localhost:8080/api-docs |
| Tela de login (US-01) | http://localhost:8080/login |
| Console do banco H2 | http://localhost:8080/h2-console |

No console do H2 use: **JDBC URL** `jdbc:h2:mem:petcleandb`, **usuário** `sa`, **senha** vazia.

### Usuários de demonstração (senha em hash bcrypt — RNF-04)

| E-mail | Senha | Perfil |
|---|---|---|
| helen@petclean.com | petclean123 | Atendente |
| gabriel@petclean.com | petclean123 | Gestor |
| joao@petclean.com | petclean123 | Atendente |
| gestor@petclean.com | gestor123 | Gestor |

### Testes

```bash
./mvnw test          # 27 testes JUnit (criterios de aceitacao)
bash testes-api.sh   # 45 verificacoes de ponta a ponta na API rodando
```

---

## 2. Autenticação e proteção de rotas (EP-06)

A autenticação usa **sessão HTTP com cookie** (`PETCLEANSESSION`), sem necessidade de Spring Security
completo, o que mantém o projeto didático:

1. `POST /login` com e-mail e senha → valida o hash bcrypt e cria a sessão.
2. Um `HandlerInterceptor` protege **todas** as rotas internas (`/api/**`):
   * cliente de API (sem `Accept: text/html`) → **401** com JSON explicativo;
   * navegador → **302** para `/login`, guardando a rota de origem; após o login o usuário
     **volta para a página solicitada** (US-02, critério 2 — a rota é devolvida no campo `rotaPendente`).
3. `POST /logout` invalida a sessão (US-14).
4. `GET /api/sessao` devolve o usuário autenticado.

```bash
# exemplo com curl
curl -c cookie.txt -X POST http://localhost:8080/login \
     -H "Content-Type: application/json" \
     -d '{"email":"helen@petclean.com","senha":"petclean123"}'

curl -b cookie.txt http://localhost:8080/api/clientes?termo=Maria
```

---

## 3. Rastreabilidade: história → código → endpoint

### EP-01 — Gerenciamento de Clientes
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-03** Cadastrar cliente | validação de campos obrigatórios; salva e aparece na listagem | `POST /api/clientes` |
| **US-04** Consultar e filtrar | filtro por nome ou CPF (HQL) + versão otimizada com projection | `GET /api/clientes?termo=` · `GET /api/clientes/resumo` |
| **US-05** Editar cliente | formulário preenchido, dados atualizados; CPF continua único | `PUT /api/clientes/{id}` |
| **US-06** Excluir cliente | confirmação no cliente; **bloqueia** se houver pets/agendamentos (RNF-09) | `DELETE /api/clientes/{id}` |
| **US-15** CPF duplicado | valida formato + dígitos verificadores e bloqueia duplicidade com “CPF já cadastrado” | `POST`/`PUT /api/clientes` |

### EP-02 — Gerenciamento de Pets
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-07** Cadastrar pet vinculado | tutor obrigatório; idade validada (0–40) | `POST /api/pets` |
| **US-08** Consultar e filtrar | filtro por nome do pet ou do tutor; lista nome, espécie e tutor | `GET /api/pets?termo=` · `GET /api/pets/resumo` |
| **US-09** Editar pet | campos preenchidos; **tutor não é alterado** por esta tela (critério 4) | `PUT /api/pets/{id}` |
| **US-10** Excluir pet | bloqueia se houver agendamento futuro ou histórico | `DELETE /api/pets/{id}` |

### EP-03 — Controle de Agendamentos
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-11** Cadastrar agendamento | só lista pets do cliente; valor e duração vêm do serviço; status inicial `AGENDADO` | `POST /api/agendamentos` |
| **US-12** Listar com filtros | por data e/ou status, ordenado por horário; agenda do dia em projection | `GET /api/agendamentos?data=&status=` · `GET /api/agendamentos/agenda` |
| **US-13** Atualizar status | salva o status e registra `atualizadoEm` (data/hora) | `PATCH /api/agendamentos/{id}/status` |
| **US-16** Cancelar | exige confirmação, muda para `CANCELADO` e **libera o horário**; realizado não cancela | `PATCH /api/agendamentos/{id}/cancelar` |
| **US-17** Conflito de horário | mesmo dia + horário ativo → **409**, sem gravar | `POST/PUT /api/agendamentos` |

### EP-04 — Controle de Estoque
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-18** Cadastrar produto | valida quantidade/preço negativos; define o estoque mínimo | `POST /api/produtos` |
| **US-19** Atualizar quantidade | entrada/saída com histórico; saída maior que o disponível é impedida | `PATCH /api/produtos/{id}/movimentar` |
| **US-20** Alerta de estoque crítico | campo `estoqueCritico` destacado quando `quantidade <= estoqueMinimo` | `GET /api/produtos` · `/estoque-critico` |
| **US-21** Excluir produto | exclui sem movimentação; com histórico devolve 409 **sugerindo inativar** | `DELETE /api/produtos/{id}` · `PATCH /api/produtos/{id}/inativar` |
| **US-25** Buscar por nome/categoria | filtro combinado, em tempo real | `GET /api/produtos?termo=&categoria=` |

### EP-05 — Dashboards Analíticos
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-22** Cards de KPIs | total de clientes, total de pets, agendamentos do mês (0 quando vazio) | `GET /api/dashboard` |
| **US-23** Gráfico por período | `semanal` (8 semanas) ou `mensal` (6 meses), eixos zerados sem erro | `GET /api/dashboard?periodo=` |
| **US-24** Estoque crítico | lista ordenada do mais crítico ao menos crítico + indicador `estoqueNormal` | `GET /api/dashboard/estoque-critico` |

### EP-06 — Autenticação e Acesso
| História | Regra implementada | Endpoint |
|---|---|---|
| **US-01** Login | e-mail + senha; senha em **bcrypt** (RNF-04); erro “Credenciais invalidas” | `POST /login` |
| **US-02** Proteger rotas | 401 para API / 302 para navegador, com retorno à rota pedida | `InterceptorSeguranca` |
| **US-14** Logout | invalida a sessão | `POST /logout` |

---

## 4. Estrutura do projeto

```
petclean/
├── pom.xml
├── mvnw / mvnw.cmd
├── testes-api.sh                     # smoke test das 25 histórias (curl)
└── src/
    ├── main/java/br/com/fatecmaua/petclean/
    │   ├── PetCleanApplication.java
    │   ├── control/                  # controllers REST (uma classe por épico)
    │   │   ├── LoginController.java       EP-06 (US-01, US-02, US-14)
    │   │   ├── ClienteController.java     EP-01
    │   │   ├── PetController.java         EP-02
    │   │   ├── AgendamentoController.java EP-03
    │   │   ├── ProdutoController.java     EP-04
    │   │   ├── DashboardController.java   EP-05
    │   │   ├── CatalogoController.java    domínios para os formulários
    │   │   └── PaginaController.java      página /login
    │   ├── service/                  # regras de negócio das histórias
    │   │   ├── ClienteService.java        US-03..US-06, US-15
    │   │   ├── PetService.java            US-07..US-10
    │   │   ├── AgendamentoService.java    US-11..US-13, US-16, US-17
    │   │   ├── ProdutoService.java        US-18..US-21, US-25
    │   │   ├── DashboardService.java      US-22..US-24
    │   │   ├── AutenticacaoService.java   US-01 (bcrypt)
    │   │   └── ValidacaoCpf.java          US-15 (dígitos verificadores)
    │   ├── model/                    # entidades JPA + enums
    │   │   ├── Cliente, Pet, Agendamento, Produto, MovimentacaoEstoque, Usuario
    │   │   └── EspecieEnum, PorteEnum, ServicoEnum, StatusAgendamentoEnum,
    │   │       CategoriaProdutoEnum, TipoMovimentacaoEnum, PerfilEnum
    │   ├── repository/               # Spring Data JPA (HQL + SQL nativo)
    │   ├── projection/               # interfaces de consulta otimizada
    │   ├── dto/                      # requests validados + respostas
    │   ├── security/                 # sessão, interceptor e configuração web
    │   ├── exception/                # exceção de negócio + handler global
    │   └── swagger/SwaggerConfig.java
    ├── main/resources/
    │   ├── application.properties
    │   ├── import.sql                # dados de demonstração
    │   └── static/index.html         # portal com atalhos e roteiro de teste
    └── test/java/...                 # 27 testes JUnit
```

---

## 5. Decisões de projeto (ligação com o relatório)

| Tema do relatório | Como aparece no código |
|---|---|
| **Kanban — fluxo e políticas explícitas** | Cada história tem endpoint próprio e mensagem de erro explícita (409/422), funcionando como “política explícita” de entrada/saída do fluxo. |
| **WIP limitado / entregas pequenas (XP)** | Commits e endpoints pequenos, um por história; `testes-api.sh` valida uma história por vez. |
| **Definition of Done** | Critérios *Dado/Quando/Então* transformados em testes JUnit (`ApiPetCleanIntegrationTest`). |
| **Simplicidade (MVP primeiro)** | `Must Have` implementado de forma direta; recursos `Should/Could` acrescentados sem alterar o núcleo. |
| **Integridade referencial (RNF-09)** | `ClienteService.excluir` e `PetService.excluir` bloqueiam a exclusão com vínculos e explicam o motivo. |
| **Segurança (RNF-04)** | `BCryptPasswordEncoder` do `spring-security-crypto`; o hash nunca é exposto nas respostas. |

---

## 6. Coleção de requisições (exemplos)

```http
### US-01 login
POST /login
Content-Type: application/json

{ "email": "helen@petclean.com", "senha": "petclean123" }

### US-03 cadastrar cliente
POST /api/clientes
Content-Type: application/json

{ "nome": "Maria da Silva", "cpf": "123.456.789-09", "telefone": "(11) 98765-4321",
  "email": "maria@email.com", "endereco": "Rua das Flores, 100 - Santo Andre/SP" }

### US-07 cadastrar pet
POST /api/pets
Content-Type: application/json

{ "idCliente": 1, "nome": "Thor", "especie": "CACHORRO", "raca": "Golden Retriever",
  "porte": "GRANDE", "idade": 4 }

### US-11 cadastrar agendamento
POST /api/agendamentos
Content-Type: application/json

{ "idCliente": 1, "idPet": 1, "servico": "BANHO_E_TOSA", "data": "2026-11-05", "hora": "09:00" }

### US-19 movimentar estoque
PATCH /api/produtos/1/movimentar
Content-Type: application/json

{ "tipo": "SAIDA", "quantidade": 2, "observacao": "Venda no balcao" }

### US-13 / US-16 status e cancelamento
PATCH /api/agendamentos/1/status
Content-Type: application/json

{ "status": "CONFIRMADO" }
```

---

## 7. Observação sobre versões

O projeto de referência usava Spring Boot 4.1.1 com dependências renomeadas
(`spring-boot-starter-webmvc`, `spring-boot-h2console`). Para garantir que compile e rode
em qualquer ambiente com JDK 17, este projeto usa **Spring Boot 3.5.16** com os starters
equivalentes (`spring-boot-starter-web`, `spring-boot-starter-data-jpa`) e `springdoc-openapi 2.8.13`.
A estrutura de pacotes e o estilo de código permanecem idênticos ao modelo.
