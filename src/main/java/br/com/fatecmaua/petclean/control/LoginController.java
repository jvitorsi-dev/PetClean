package br.com.fatecmaua.petclean.control;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.dto.ErroResposta;
import br.com.fatecmaua.petclean.dto.LoginRequest;
import br.com.fatecmaua.petclean.dto.LoginResponse;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.security.SessaoService;
import br.com.fatecmaua.petclean.security.UsuarioSessao;
import br.com.fatecmaua.petclean.service.AutenticacaoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;

/**
 * EP-06 - Autenticacao e Acesso: US-01 (login), US-02 (protecao de rotas),
 * US-14 (logout).
 */
@RestController
@Tag(name = "06 - Autenticacao e Acesso", description = "Login, logout e sessao do usuario (EP-06)")
public class LoginController {

	@Autowired
	private AutenticacaoService autenticacaoService;

	@Autowired
	private SessaoService sessaoService;

	@Operation(description = "US-01 - Realiza o login com e-mail e senha. "
			+ "Credenciais validas criam a sessao e devolvem o usuario autenticado; "
			+ "senha incorreta devolve 401 com a mensagem 'Credenciais invalidas'.", tags = "06 - Autenticacao e Acesso", responses = {
					@ApiResponse(responseCode = "200", description = "Login realizado com sucesso"),
					@ApiResponse(responseCode = "401", description = "Credenciais invalidas", content = @Content(schema = @Schema(implementation = ErroResposta.class))) })
	@PostMapping("/login")
	public LoginResponse login(@RequestBody @Valid LoginRequest dados, HttpServletRequest request) {
		UsuarioSessao usuario = autenticacaoService.autenticar(dados);
		sessaoService.autenticar(request, usuario);

		// US-02 (2): devolve a rota que o usuario tentou acessar antes do login
		String rotaPendente = sessaoService.consumirRotaPendente(request);
		return new LoginResponse(usuario, rotaPendente, "Login realizado com sucesso.");
	}

	@Operation(description = "US-14 - Encerra a sessao (logout). A sessao e invalidada, "
			+ "portanto qualquer requisicao seguinte volta a exigir login.", tags = "06 - Autenticacao e Acesso")
	@PostMapping("/logout")
	public ResponseEntity<Void> logout(HttpServletRequest request) {
		sessaoService.encerrar(request);
		return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
	}

	@Operation(description = "US-01/US-02 - Informa o usuario autenticado na sessao atual. "
			+ "Devolve 401 quando nao ha sessao valida.", tags = "06 - Autenticacao e Acesso")
	@GetMapping("/api/sessao")
	public UsuarioSessao sessaoAtual(HttpServletRequest request) {
		UsuarioSessao usuario = sessaoService.usuarioAtual(request);
		if (usuario == null) {
			throw ErroNegocioException.naoAutorizado("Acesso nao autenticado.");
		}
		return usuario;
	}

	@Operation(description = "US-02 - Rota usada para conferir a protecao de rotas internas: "
			+ "sem sessao a API responde 401 e o navegador e redirecionado para /login.", tags = "06 - Autenticacao e Acesso")
	@GetMapping("/api/verificar-acesso")
	public ResponseEntity<String> verificarAcesso() {
		return ResponseEntity.ok("Acesso autorizado: existe sessao autenticada.");
	}

}
