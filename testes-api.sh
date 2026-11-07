#!/usr/bin/env bash
# =====================================================================
# PetClean - smoke test das 25 historias de usuario
# Uso: bash testes-api.sh   (com a API rodando em http://localhost:8080)
# =====================================================================
BASE=http://localhost:8080
COOKIE=$(mktemp)
PASS=0; FAIL=0

req() { # metodo rota corpo [codigo_esperado]
  local metodo=$1 rota=$2 corpo=$3 esperado=$4
  local args=(-s -o /tmp/resp.txt -w "%{http_code}" -X "$metodo" "$BASE$rota" -b "$COOKIE" -c "$COOKIE")
  if [ -n "$corpo" ]; then args+=(-H "Content-Type: application/json" -d "$corpo"); fi
  local codigo
  codigo=$(curl "${args[@]}")
  if [ "$codigo" = "$esperado" ]; then
    PASS=$((PASS+1)); echo "OK   $codigo  $metodo $rota"
  else
    FAIL=$((FAIL+1)); echo "FAIL $codigo (esperado $esperado)  $metodo $rota"; head -c 300 /tmp/resp.txt; echo
  fi
}

echo "=== US-02: rota protegida sem sessao deve responder 401 ==="
req GET /api/clientes "" 401

echo
echo "=== US-01: login ==="
req POST /login '{"email":"helen@petclean.com","senha":"errada"}' 401
req POST /login '{"email":"helen@petclean.com","senha":"petclean123"}' 200

echo
echo "=== US-03 / US-04 / US-05 / US-06 / US-15: clientes ==="
req GET /api/clientes "" 200
req GET "/api/clientes?termo=Maria" "" 200
req GET /api/clientes/resumo "" 200
req POST /api/clientes '{"nome":"Teste Novo","cpf":"123.456.789-09","telefone":"(11) 90000-0000","email":"teste.novo@email.com","endereco":"Rua Teste, 1"}' 409
req POST /api/clientes '{"nome":"Teste Novo","cpf":"111.222.333-44","telefone":"(11) 90000-0000","email":"teste.novo@email.com","endereco":"Rua Teste, 1"}' 422
NOVO=$(curl -s -X POST "$BASE/api/clientes" -H "Content-Type: application/json" -b "$COOKIE" -c "$COOKIE" \
  -d '{"nome":"Teste Novo","cpf":"987.654.321-00","telefone":"(11) 90000-0000","email":"teste.novo@email.com","endereco":"Rua Teste, 1"}')
echo "     cliente criado: $NOVO"
ID_NOVO=$(echo "$NOVO" | sed -n 's/.*"id":\([0-9]*\).*/\1/p')
req PUT "/api/clientes/$ID_NOVO" '{"nome":"Teste Editado","cpf":"987.654.321-00","telefone":"(11) 91111-1111","email":"editado@email.com","endereco":"Rua Teste, 2"}' 200
req DELETE /api/clientes/1 "" 409
req DELETE "/api/clientes/$ID_NOVO" "" 204

echo
echo "=== US-07 / US-08 / US-09 / US-10: pets ==="
req GET /api/pets "" 200
req GET "/api/pets?termo=Thor" "" 200
req GET /api/pets/resumo "" 200
req GET /api/pets/cliente/1 "" 200
req POST /api/pets '{"idCliente":1,"nome":"X","especie":"CACHORRO","raca":"SRD","porte":"MEDIO","idade":-3}' 400
req POST /api/pets '{"idCliente":1,"nome":"Xerife","especie":"CACHORRO","raca":"SRD","porte":"MEDIO","idade":3}' 201
req PUT /api/pets/1 '{"idCliente":99,"nome":"Thor Editado","especie":"CACHORRO","raca":"Golden","porte":"GRANDE","idade":5}' 200
req DELETE /api/pets/1 "" 409

echo
echo "=== US-11 / US-12 / US-13 / US-16 / US-17: agendamentos ==="
req GET /api/agendamentos "" 200
req GET "/api/agendamentos?status=AGENDADO" "" 200
req GET /api/agendamentos/agenda "" 200
# datas derivadas de hoje (nunca literais: o script tem de continuar valido em qualquer dia)
HOJE=$(date +%F)
ONTEM=$(date -d "yesterday" +%F 2>/dev/null || date -v-1d +%F)
FUTURO=$(date -d "+30 days" +%F 2>/dev/null || date -v+30d +%F)
req POST /api/agendamentos "{\"idCliente\":1,\"idPet\":1,\"servico\":\"BANHO\",\"data\":\"$ONTEM\",\"hora\":\"10:00\"}" 422
req POST /api/agendamentos "{\"idCliente\":1,\"idPet\":1,\"servico\":\"BANHO\",\"data\":\"$HOJE\",\"hora\":\"09:00\"}" 409
req POST /api/agendamentos "{\"idCliente\":1,\"idPet\":3,\"servico\":\"BANHO\",\"data\":\"$FUTURO\",\"hora\":\"08:00\"}" 422
AG=$(curl -s -X POST "$BASE/api/agendamentos" -H "Content-Type: application/json" -b "$COOKIE" -c "$COOKIE" \
  -d "{\"idCliente\":1,\"idPet\":1,\"servico\":\"BANHO_E_TOSA\",\"data\":\"$FUTURO\",\"hora\":\"08:00\"}")
echo "     agendamento criado: $AG"
ID_AG=$(echo "$AG" | sed -n 's/.*"id":\([0-9]*\).*/\1/p')
req PATCH "/api/agendamentos/$ID_AG/status" '{"status":"CONFIRMADO"}' 200
req PATCH "/api/agendamentos/$ID_AG/cancelar?motivo=Cliente%20desmarcou" "" 200
req PATCH "/api/agendamentos/17/cancelar" "" 409

echo
echo "=== US-18 / US-19 / US-20 / US-21 / US-25: estoque ==="
req GET /api/produtos "" 200
req GET "/api/produtos?termo=Racao" "" 200
req GET "/api/produtos?categoria=MEDICAMENTO" "" 200
req GET /api/produtos/resumo "" 200
req GET /api/produtos/estoque-critico "" 200
req POST /api/produtos '{"nome":"Produto Ruim","categoria":"OUTRO","quantidade":-1,"estoqueMinimo":2,"preco":10.0}' 400
req PATCH /api/produtos/1/movimentar '{"tipo":"SAIDA","quantidade":999,"observacao":"teste"}' 409
req PATCH /api/produtos/1/movimentar '{"tipo":"SAIDA","quantidade":2,"observacao":"Venda"}' 200
req DELETE /api/produtos/1 "" 409
req PATCH "/api/produtos/1/inativar?ativo=false" "" 200
req DELETE /api/produtos/10 "" 204
req GET /api/produtos/movimentacoes "" 200

echo
echo "=== US-22 / US-23 / US-24: dashboard ==="
req GET /api/dashboard "" 200
req GET "/api/dashboard?periodo=semanal" "" 200
req GET "/api/dashboard?periodo=mensal" "" 200
req GET /api/dashboard/estoque-critico "" 200


echo
echo "=== Tela de Perfil: dados, senha e foto ==="
req GET /api/usuarios/1 "" 200
req PUT /api/usuarios/1 '{"nome":"Helen Vitoria Silva Aclina","email":"helen@petclean.com","telefone":"(11) 91234-5678","nomePetshop":"PetClean Central","endereco":"Rua das Flores, 123 - Santo Andre/SP"}' 200
req PUT /api/usuarios/1/senha '{"senhaAtual":"senha-errada","novaSenha":"outraSenha123"}' 422
req PUT /api/usuarios/2 '{"nome":"Nao Pode","email":"gabriel@petclean.com"}' 403

echo
echo "=== US-14: logout ==="
req POST /logout "" 204
req GET /api/clientes "" 401

echo
echo "======================================================"
echo " RESUMO: $PASS testes OK | $FAIL falhas"
echo "======================================================"
rm -f "$COOKIE"
