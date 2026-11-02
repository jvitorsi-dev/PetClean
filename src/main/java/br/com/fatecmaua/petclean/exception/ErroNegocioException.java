package br.com.fatecmaua.petclean.exception;

import org.springframework.http.HttpStatus;

/**
 * Excecao de regra de negocio. Carrega o status HTTP adequado para a resposta da API
 * (400 para dados invalidos, 404 para recurso inexistente, 409 para conflitos como
 * CPF duplicado, horario ocupado ou integridade referencial).
 */
public class ErroNegocioException extends RuntimeException {

	private static final long serialVersionUID = 1L;

	private final HttpStatus status;

	public ErroNegocioException(String mensagem, HttpStatus status) {
		super(mensagem);
		this.status = status;
	}

	public ErroNegocioException(String mensagem) {
		this(mensagem, HttpStatus.CONFLICT);
	}

	public HttpStatus getStatus() {
		return status;
	}

	// ---------------------------------------------------------------------
	// Atalhos usados pelos services, cada um ligado a uma historia do PDF
	// ---------------------------------------------------------------------

	/** US-04 (3), US-08 (3) etc.: registro inexistente. */
	public static ErroNegocioException naoEncontrado(String mensagem) {
		return new ErroNegocioException(mensagem, HttpStatus.NOT_FOUND);
	}

	/** US-03 (3), US-07 (3): campo obrigatorio/invalido. */
	public static ErroNegocioException dadosInvalidos(String mensagem) {
		return new ErroNegocioException(mensagem, HttpStatus.UNPROCESSABLE_ENTITY);
	}

	/** US-06 (2), US-15 (1), US-17 (1), US-19 (2), US-21 (2): conflito de regra. */
	public static ErroNegocioException conflito(String mensagem) {
		return new ErroNegocioException(mensagem, HttpStatus.CONFLICT);
	}

	/** US-01 (2), US-02 (1): credenciais invalidas ou acesso nao autenticado. */
	public static ErroNegocioException naoAutorizado(String mensagem) {
		return new ErroNegocioException(mensagem, HttpStatus.UNAUTHORIZED);
	}

}
