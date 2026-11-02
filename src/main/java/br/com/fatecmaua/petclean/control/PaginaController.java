package br.com.fatecmaua.petclean.control;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import br.com.fatecmaua.petclean.security.SessaoService;
import br.com.fatecmaua.petclean.security.UsuarioSessao;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;

/**
 * US-01 e US-02: tela de login do sistema. O front-end consumido e a API REST;
 * esta pagina existe para que a navegacao sem sessao tenha destino (o interceptor
 * redireciona para /login) e devolve 302 de volta para a rota de origem.
 */
@Controller
@Tag(name = "06 - Autenticacao e Acesso", description = "Login, logout e sessao do usuario (EP-06)")
public class PaginaController {

	@Autowired
	private SessaoService sessaoService;

	@Operation(description = "US-02 (1) - Pagina de login para onde as rotas internas redirecionam "
			+ "quando nao ha sessao. US-01: envia as credenciais para POST /login.", tags = "06 - Autenticacao e Acesso")
	@GetMapping(value = "/login", produces = MediaType.TEXT_HTML_VALUE)
	public ResponseEntity<String> login(HttpServletRequest request) {
		UsuarioSessao usuario = sessaoService.usuarioAtual(request);

		if (usuario != null) {
			// US-02 (2): com sessao ativa o usuario volta para a rota pendente
			String pendente = sessaoService.consumirRotaPendente(request);
			String destino = pendente == null ? "/" : pendente;
			return ResponseEntity.status(HttpStatus.FOUND).header("Location", destino).build();
		}
		return ResponseEntity.ok(HTML_LOGIN);
	}

	private static final String HTML_LOGIN = """
			<!DOCTYPE html>
			<html lang="pt-BR">
			<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<title>PetClean - Login</title>
			<style>
			  :root { --azul:#0f6e8c; --erro:#c0392b; }
			  * { box-sizing:border-box; }
			  body { margin:0; min-height:100vh; display:grid; place-items:center;
			         font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
			         background:linear-gradient(135deg,#0f6e8c,#2e9e6b); color:#1d2a31; padding:20px; }
			  .caixa { width:100%; max-width:390px; background:#fff; border-radius:16px; padding:30px 28px;
			           box-shadow:0 18px 40px rgba(0,0,0,.22); }
			  h1 { margin:0 0 4px; font-size:22px; color:var(--azul); }
			  p.sub { margin:0 0 20px; font-size:13px; color:#5d7078; }
			  label { display:block; font-size:13px; font-weight:600; margin:14px 0 6px; }
			  input { width:100%; padding:11px 12px; border:1px solid #cddbe2; border-radius:9px; font-size:14px; }
			  button { width:100%; margin-top:20px; padding:12px; border:0; border-radius:9px;
			           background:var(--azul); color:#fff; font-size:15px; font-weight:700; cursor:pointer; }
			  .msg { margin-top:14px; font-size:13px; padding:10px 12px; border-radius:8px; display:none; }
			  .msg.erro { display:block; background:#fdecea; color:var(--erro); }
			  .dica { margin-top:18px; font-size:12px; line-height:1.6; color:#6b7c85;
			          border-top:1px dashed #d8e3e9; padding-top:14px; }
			  code { background:#eef3f6; padding:1px 5px; border-radius:4px; }
			</style>
			</head>
			<body>
			<div class="caixa">
			  <h1>PetClean</h1>
			  <p class="sub">Entre com seu e-mail e senha para acessar o sistema.</p>
			  <form id="form">
			    <label for="email">E-mail</label>
			    <input id="email" type="email" placeholder="helen@petclean.com" required>
			    <label for="senha">Senha</label>
			    <input id="senha" type="password" placeholder="********" required>
			    <button type="submit">Entrar</button>
			  </form>
			  <div id="msg" class="msg"></div>
			  <div class="dica">
			    <strong>Usuarios de demonstracao</strong><br>
			    <code>helen@petclean.com</code> / <code>petclean123</code> - atendente<br>
			    <code>gestor@petclean.com</code> / <code>gestor123</code> - gestor
			  </div>
			</div>
			<script>
			document.getElementById('form').addEventListener('submit', async (e) => {
			  e.preventDefault();
			  const msg = document.getElementById('msg');
			  msg.className = 'msg'; msg.textContent = '';
			  const resposta = await fetch('/login', {
			    method: 'POST',
			    headers: { 'Content-Type': 'application/json' },
			    body: JSON.stringify({
			      email: document.getElementById('email').value,
			      senha: document.getElementById('senha').value
			    })
			  });
			  const dados = await resposta.json().catch(() => ({}));
			  if (!resposta.ok) {
			    msg.className = 'msg erro';
			    msg.textContent = dados.mensagem || 'Credenciais invalidas.';
			    return;
			  }
			  const destino = dados.rotaPendente && dados.rotaPendente.startsWith('/api/')
			    ? '/swagger-ui.html' : (dados.rotaPendente || '/');
			  window.location.href = destino;
			});
			</script>
			</body>
			</html>
			""";

}
