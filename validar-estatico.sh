#!/usr/bin/env bash
# =====================================================================
# PetClean - validacoes estaticas da migracao PHP -> Java
# Uso: bash validar-estatico.sh
# Roda sem servidor e sem Maven. Usa python3/node apenas se existirem.
# =====================================================================
cd "$(dirname "$0")" || exit 1
FALHAS=0
AVISOS=0

ok()     { echo "  OK    $1"; }
falha()  { FALHAS=$((FALHAS+1)); echo "  FALHA $1"; }
aviso()  { AVISOS=$((AVISOS+1)); echo "  AVISO $1"; }

TPL=src/main/resources/templates/paginas
STC=src/main/resources/static
CTRL=src/main/java/br/com/fatecmaua/petclean/control/PaginaPainelController.java

echo "== 1. Residuos de PHP no front-end =="
RES=$(grep -rn "<?php\|<?=\|endforeach\|endif;" "$TPL" "$STC" --include="*.html" --include="*.js" 2>/dev/null)
if [ -z "$RES" ]; then ok "nenhum bloco PHP remanescente"; else falha "PHP remanescente:"; echo "$RES"; fi

echo "== 2. Links .php ainda ativos (href/src/action/location) =="
VIVOS=$(grep -rnoE "(href|src|action)=[\"'][^\"']*\.php|location\.href=['\"][^\"']*\.php" "$TPL" "$STC" --include="*.html" --include="*.js" 2>/dev/null)
if [ -z "$VIVOS" ]; then ok "nenhum link .php ativo"; else aviso "links .php ativos (apontam para arquivos inexistentes):"; echo "$VIVOS"; fi

echo "== 3. Chamadas fetch para a API (/api, /login, /logout) =="
CHAMADAS=$(grep -rhoE "PetCleanApi\.(get|post|put|patch|del)\(\"[^\"]+\"|fetch\(\"/(api|login|logout)[^\"]*\"" "$STC/js" 2>/dev/null | sort -u)
if [ -z "$CHAMADAS" ]; then falha "nenhuma chamada encontrada (esperado usar PetCleanApi)"; else ok "$(echo "$CHAMADAS" | wc -l) chamadas mapeadas"; fi

echo "== 4. Sintaxe dos arquivos JS =="
if command -v node >/dev/null 2>&1; then
  ERRO=0
  for f in "$STC"/js/*.js; do node --check "$f" 2>/dev/null || { falha "sintaxe: $f"; ERRO=1; }; done
  [ "$ERRO" = "0" ] && ok "node --check sem erros em $(ls "$STC"/js/*.js | wc -l) arquivos"
else
  aviso "node nao instalado - checagem de sintaxe JS ignorada"
fi

echo "== 5. HTML balanceado e variaveis dos templates =="
if command -v python3 >/dev/null 2>&1; then
  python3 - "$TPL" "$CTRL" <<'PY'
import sys, glob, re
from html.parser import HTMLParser

TPL, CTRL = sys.argv[1], sys.argv[2]
VAZIAS = {'br','img','input','meta','link','hr','source','area','base','col','embed','param','track','wbr'}

class P(HTMLParser):
    def __init__(s): super().__init__(); s.pilha=[]; s.erros=[]
    def handle_starttag(s,t,a):
        if t not in VAZIAS: s.pilha.append((t,s.getpos()))
    def handle_endtag(s,t):
        if t in VAZIAS: return
        if s.pilha and s.pilha[-1][0]==t: s.pilha.pop()
        elif any(x[0]==t for x in s.pilha):
            while s.pilha and s.pilha[-1][0]!=t: s.erros.append(s.pilha.pop())
            if s.pilha: s.pilha.pop()
        else: s.erros.append((t,s.getpos()))

falhas=0
for f in sorted(glob.glob(TPL+"/*.html")):
    p=P(); p.feed(open(f,encoding="utf-8").read())
    if p.pilha or p.erros:
        falhas+=1; print(f"  FALHA HTML desbalanceado em {f}: {p.pilha[:3]}{p.erros[:3]}")
if not falhas: print(f"  OK    HTML balanceado nos {len(glob.glob(TPL+'/*.html'))} templates")

ctrl=open(CTRL,encoding="utf-8").read()
modelo=set(re.findall(r'addAttribute\("([A-Za-z0-9_]+)"',ctrl))
modelo|={"servicosLabel","categoriasLabel","portesLabel"}
IGN={'true','false','null','and','or','not','eq','ne','gt','lt','ge','le','div','mod',
     'lists','numbers','temporals','mm','yyyy','dd','HH'}
faltando=0
for f in sorted(glob.glob(TPL+"/*.html")):
    t=open(f,encoding="utf-8").read()
    locais=set(re.findall(r'th:each="\s*([A-Za-z0-9_]+)\s*:',t))
    usados=set()
    for e in re.findall(r'\$\{([^}]*)\}',t):
        for m in re.finditer(r'(?<![\w.\'"])([a-zA-Z_][a-zA-Z0-9_]*)',e): usados.add(m.group(1))
    falta=sorted(u for u in usados if u not in modelo and u not in locais
                 and u not in IGN and not u[0].isupper())
    if falta:
        faltando+=1; print(f"  FALHA variaveis sem origem em {f}: {falta}")
if not faltando: print("  OK    todas as variaveis dos templates existem no controller")
PY
else
  aviso "python3 nao instalado - checagens de HTML/variaveis ignoradas"
fi

echo "== 6. Referencias locais (css/js/assets) =="
if command -v python3 >/dev/null 2>&1; then
  python3 - "$TPL" "$STC" <<'PY'
import sys, glob, os, re
TPL, STC = sys.argv[1], sys.argv[2]
quebradas=[]
for f in glob.glob(TPL+"/*.html")+glob.glob(STC+"/paginas/*.html"):
    t=open(f,encoding="utf-8").read()
    for m in re.finditer(r'(?:src|href)="(\.\./[^"]+)"', t):
        alvo=os.path.join(STC, m.group(1)[3:])
        if not os.path.exists(alvo): quebradas.append(f"{os.path.basename(f)} -> {m.group(1)}")
if quebradas:
    print("  FALHA referencias quebradas:"); [print("        "+q) for q in quebradas]
else:
    print("  OK    nenhuma referencia local quebrada")
PY
fi

echo "== 7. Arquivos de pagina esperados =="
for pag in dashboard relatorios clientes pets estoque agendamentos perfil configuracoes; do
  [ -f "$TPL/$pag.html" ] || falha "template ausente: paginas/$pag.html"
done
for pag in inicio sobrenos funcionalidades faleconosco solicitar-demo login recuperar-senha; do
  [ -f "$STC/paginas/$pag.html" ] || falha "pagina publica ausente: paginas/$pag.html"
done
[ "$FALHAS" = "0" ] && ok "8 templates do painel + 7 paginas publicas presentes"

echo
echo "======================================================"
echo " Falhas: $FALHAS   Avisos: $AVISOS"
echo "======================================================"
[ "$FALHAS" = "0" ]
