package br.com.fatecmaua.petclean.security;

import org.springframework.stereotype.Component;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

/**
 * Acesso centralizado a sessao HTTP: chave do usuario autenticado e rota pendente
 * usada no redirecionamento pos-login (US-02, criterio 2).
 */
@Component
public class SessaoService {

	public static final String CHAVE_USUARIO = "USUARIO_AUTENTICADO";
	public static final String CHAVE_ROTA_PENDENTE = "ROTA_PENDENTE";

	public void autenticar(HttpServletRequest request, UsuarioSessao usuario) {
		HttpSession sessao = request.getSession(true);
		sessao.setAttribute(CHAVE_USUARIO, usuario);
	}

	/** US-14: logout encerra a sessao por completo. */
	public void encerrar(HttpServletRequest request) {
		HttpSession sessao = request.getSession(false);
		if (sessao != null) {
			sessao.invalidate();
		}
	}

	public UsuarioSessao usuarioAtual(HttpServletRequest request) {
		HttpSession sessao = request.getSession(false);
		if (sessao == null) {
			return null;
		}
		Object valor = sessao.getAttribute(CHAVE_USUARIO);
		return valor instanceof UsuarioSessao usuario ? usuario : null;
	}

	public void registrarRotaPendente(HttpServletRequest request, String rota) {
		request.getSession(true).setAttribute(CHAVE_ROTA_PENDENTE, rota);
	}

	/**
	 * US-02 (2): apos o login o usuario deve voltar para a pagina solicitada.
	 * A rota pendente e devolvida uma unica vez e entao removida da sessao.
	 */
	public String consumirRotaPendente(HttpServletRequest request) {
		HttpSession sessao = request.getSession(false);
		if (sessao == null) {
			return null;
		}
		Object rota = sessao.getAttribute(CHAVE_ROTA_PENDENTE);
		sessao.removeAttribute(CHAVE_ROTA_PENDENTE);
		return rota == null ? null : rota.toString();
	}

}
