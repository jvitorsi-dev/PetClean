package br.com.fatecmaua.petclean.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * US-02 (1): toda rota interna exige autenticacao.
 * <ul>
 * <li>Requisicoes de API (prefixo /api) recebem 401 com JSON explicativo;</li>
 * <li>requisicoes de navegacao recebem 302 para /login, guardando a rota pendente
 * para o retorno pos-login (US-02, criterio 2).</li>
 * </ul>
 */
@Component
public class InterceptorSeguranca implements HandlerInterceptor {

	@Autowired
	private SessaoService sessaoService;

	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
			throws Exception {

		// Pre-flight de CORS e sempre liberado
		if ("OPTIONS".equalsIgnoreCase(request.getMethod())) {
			return true;
		}

		UsuarioSessao usuario = sessaoService.usuarioAtual(request);
		if (usuario != null) {
			return true;
		}

		String rota = request.getRequestURI();

		// US-02 (1): navegacao no browser (Accept: text/html) e redirecionada para /login,
		// guardando a rota de origem para voltar depois do login (criterio 2).
		if (ehNavegacaoDeNavegador(request)) {
			sessaoService.registrarRotaPendente(request, rota);
			response.sendRedirect(request.getContextPath() + "/paginas/login.html");
			return false;
		}

		// Clientes de API recebem 401 em JSON, com a instrucao de autenticacao.
		throw new ErroNegocioException(
				"Acesso nao autenticado. Efetue login em POST /login e reenvie a requisicao com o cookie de sessao.",
				HttpStatus.UNAUTHORIZED);
	}

	/** true quando o cliente aceita HTML (browser) e nao pediu explicitamente JSON. */
	private boolean ehNavegacaoDeNavegador(HttpServletRequest request) {
		String accept = request.getHeader("Accept");
		if (accept == null) {
			return false;
		}
		String minusculo = accept.toLowerCase();
		return minusculo.contains("text/html") && !minusculo.contains("application/json");
	}

}
