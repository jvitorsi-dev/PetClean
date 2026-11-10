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
	public ResponseEntity<Void> login(HttpServletRequest request) {
		UsuarioSessao usuario = sessaoService.usuarioAtual(request);

		if (usuario != null) {
			// US-02 (2): com sessao ativa o usuario volta para a rota pendente
			String pendente = sessaoService.consumirRotaPendente(request);
			String destino = pendente == null ? "/paginas/dashboard.html" : pendente;
			return ResponseEntity.status(HttpStatus.FOUND).header("Location", destino).build();
		}

		// A tela de login do sistema e a pagina original do projeto (paginas/login.html)
		return ResponseEntity.status(HttpStatus.FOUND).header("Location", "/paginas/login.html").build();
	}
}
