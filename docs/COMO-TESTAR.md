# Como testar o PetClean (guia prático)

Este guia é para **você**, não para o computador. São três etapas: subir a aplicação,
rodar o teste automático e fazer 4 verificações clicando na tela.

---

## 1. Subir a aplicação

Na pasta do projeto (Windows):

```cmd
mvnw.cmd spring-boot:run
```

Espere aparecer `Started PetCleanApplication`. Abra no navegador:

```
http://localhost:8080
```

**Login:** `helen@petclean.com` — **Senha:** `petclean123`

> O banco é em memória (H2). Cada vez que a aplicação sobe, ela volta ao estado inicial:
> 8 tutores, 10 pets, 11 produtos, agendamentos de hoje até +5 dias. Isso é normal.

---

## 2. O teste automático (não precisa clicar em nada)

Com a aplicação rodando, abra outro terminal **na pasta do projeto** e rode:

```bash
bash testes-api.sh
```

> No Windows use o **Git Bash** (o mesmo que você já usa para `bash validar-estatico.sh`).

O resultado são 46 linhas. Cada uma começa com `OK` ou `FAIL`, e no fim aparece:

```
 RESUMO: 46 testes OK | 0 falhas
```

**O que ele verifica:** login, logout, acesso sem sessão (401), CRUD de clientes, CRUD de pets,
agendamentos (data passada, pet de outro tutor, horário duplicado, cancelamento), estoque
(saída maior que o saldo, produto inativo) e os números do dashboard.

**Duas coisas importantes:**

1. **Este script altera os dados** (cria cliente/pet/agendamento, inativa o produto 1, exclui o
   produto 10). Rode-o **por último** ou **reinicie a aplicação** depois (`Ctrl+C` e suba de novo)
   para voltar ao estado do seed.
2. Se aparecer um `FAIL`, copie a linha inteira e as 5 linhas seguintes — ali vem a resposta da API
   dizendo o que o sistema devolveu.

---

## 3. As 4 verificações manuais

### Teste A — Botão "Invalidar Todas as Sessões"

| # | O que fazer |
|---|---|
| 1 | No menu lateral, clique em **Configurações** (último item) |
| 2 | Desça até o bloco vermelho **"Invalidar Todas as Sessões"** |
| 3 | Clique no botão |
| 4 | Deve aparecer a caixa: *"Tem certeza que deseja invalidar todas as sessões e deslogar do sistema?"* → clique **OK** |
| 5 | **Esperado:** a tela volta para o **login** |

**Para confirmar que a sessão morreu de verdade:** tente abrir `http://localhost:8080/paginas/dashboard.html` —
deve voltar para o login.

---

### Teste B — Agendar em data passada

| # | O que fazer |
|---|---|
| 1 | Menu lateral → **Agendamentos** |
| 2 | Clique em **+ Novo Agendamento** (canto superior direito) |
| 3 | Tutor: qualquer um · Pet: um pet do tutor · Serviço: Banho |
| 4 | **Data: ontem** — clique no campo de data e escolha o dia anterior |
| 5 | Hora: `10:00` → **Salvar** |
| 6 | **Esperado:** aparece a caixa *"Nao e possivel agendar em data passada."* e o agendamento **não** entra na lista |

> A mensagem vem do backend (regra de negócio), não da tela — é o sistema recusando, como o PHP fazia.

---

### Teste C — Cadastrar CPF repetido

| # | O que fazer |
|---|---|
| 1 | Menu lateral → **Clientes** |
| 2 | Clique em **+ Novo Cliente** |
| 3 | Nome: qualquer · **CPF: `529.982.247-25`** (CPF que já existe no seed, da Helena) |
| 4 | Preencha telefone e e-mail com qualquer coisa → **Salvar** |
| 5 | **Esperado:** aparece *"CPF ja cadastrado: 529.982.247-25."* e o cliente **não** é criado |

---

### Teste D — Estoque: quantidade abaixo do mínimo

| # | O que fazer |
|---|---|
| 1 | Menu lateral → **Estoque** |
| 2 | Na linha **"Ração Premium Adulto 10kg"** (Qtd Atual 12, Mínimo 5), clique em **Editar** |
| 3 | Mude a **quantidade para 4** → **Salvar** |
| 4 | **Esperado:** o número da linha vira **4**, em vermelho, com um **triângulo de alerta** ao lado |
| 5 | Agora repita com **"Vermífugo Suspensão 10ml"** (está com 0): mude para **10** → **Salvar** |
| 6 | **Esperado:** o triângulo de alerta **desaparece** dessa linha |

> Na tela de estoque não existe botão de "movimentação" — igual ao PHP original, a quantidade é
> alterada pelo **Editar**. O endpoint de movimentação (`PATCH /api/produtos/{id}/movimentar`)
> existe na API e é coberto pelo `testes-api.sh` (inclusive o caso de saída maior que o saldo).

---

## 4. O que NÃO dá para testar pela tela (e por quê)

Não é falha — é a tela impedindo o erro antes de chegar na API. Esses casos são cobertos pelo
`testes-api.sh`, que chama a API direto:

| Regra | Por que não dá pela tela | Onde é testado |
|---|---|---|
| Pet de outro tutor no agendamento | a tela recarrega a lista de pets conforme o tutor escolhido, então o par errado nunca é montado | `testes-api.sh` (POST com pet 3 e cliente 1 → 422) |
| Saída maior que o saldo em estoque | não há tela de movimentação | `testes-api.sh` (PATCH com 999 unidades → 409) |
| Horário já ocupado | só aparece se você criar dois agendamentos iguais, o que polui os dados de teste | `testes-api.sh` (POST no mesmo dia/hora → 409) |

---

## 5. Se algo falhar, me mande isto

1. **A tela**: print ou a frase exata que apareceu (a caixa de alerta).
2. **O terminal**: as linhas que aparecem no console do `spring-boot:run` naquele momento
   (procure linhas com `ERROR` ou `Exception`).
3. Se for no `testes-api.sh`: a linha `FAIL` inteira.

Com isso eu vou direto ao ponto, sem chutar.

---

## 6. Checklist rápido para marcar

```
[ ] 1. Aplicação sobe sem erro (Started PetCleanApplication)
[ ] 2. Login com helen@petclean.com funciona
[ ] 3. Dashboard mostra os 3 gráficos
[ ] 4. Relatórios mostra os 5 gráficos
[ ] 5. Acentos corretos no estoque e nos pets (Ração, Siamês, Vermífugo)
[ ] 6. Teste A — Invalidar sessões volta para o login
[ ] 7. Teste B — agendamento em data passada é recusado
[ ] 8. Teste C — CPF repetido é recusado
[ ] 9. Teste D — alerta de estoque crítico aparece e desaparece
[ ] 10. bash testes-api.sh → 46 OK / 0 falhas
[ ] 11. bash validar-estatico.sh → 0 falhas / 0 avisos
```
