package br.com.fatecmaua.petclean.exception;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;

import br.com.fatecmaua.petclean.dto.ErroResposta;
import jakarta.servlet.http.HttpServletRequest;

/**
 * Converte excecoes em respostas JSON padronizadas.
 * Cobre os criterios de aceitacao que exigem mensagem de erro visivel ao usuario
 * (US-03, US-07, US-15, US-17, US-18, US-19, US-21, US-01).
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

	@ExceptionHandler(ErroNegocioException.class)
	public ResponseEntity<ErroResposta> tratarErroNegocio(ErroNegocioException ex, HttpServletRequest req) {
		return ResponseEntity.status(ex.getStatus()).body(new ErroResposta(ex.getStatus().value(),
				titulo(ex.getStatus()), ex.getMessage(), List.of(), req.getRequestURI()));
	}

	/** Bean Validation: devolve todos os campos invalidos de uma vez. */
	@ExceptionHandler(MethodArgumentNotValidException.class)
	public ResponseEntity<ErroResposta> tratarValidacao(MethodArgumentNotValidException ex, HttpServletRequest req) {
		List<String> detalhes = new ArrayList<>();
		for (FieldError erro : ex.getBindingResult().getFieldErrors()) {
			detalhes.add(erro.getField() + ": " + erro.getDefaultMessage());
		}
		return ResponseEntity.status(HttpStatus.BAD_REQUEST)
				.body(new ErroResposta(400, "Dados invalidos", "Revise os campos informados.", detalhes,
						req.getRequestURI()));
	}

	/** JSON malformado, enum invalido, data no formato errado. */
	@ExceptionHandler({ HttpMessageNotReadableException.class, MethodArgumentTypeMismatchException.class,
			MissingServletRequestParameterException.class })
	public ResponseEntity<ErroResposta> tratarRequisicaoInvalida(Exception ex, HttpServletRequest req) {
		String mensagem = ex instanceof HttpMessageNotReadableException
				? "Corpo da requisicao invalido. Verifique tipos, datas (AAAA-MM-DD) e horarios (HH:mm)."
				: "Parametro da requisicao invalido.";
		return ResponseEntity.status(HttpStatus.BAD_REQUEST)
				.body(new ErroResposta(400, "Requisicao invalida", mensagem, List.of(), req.getRequestURI()));
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<ErroResposta> tratarGenerico(Exception ex, HttpServletRequest req) {
		return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
				.body(new ErroResposta(500, "Erro interno", "Nao foi possivel concluir a operacao.",
						List.of(String.valueOf(ex.getMessage())), req.getRequestURI()));
	}

	private String titulo(HttpStatus status) {
		return switch (status) {
			case NOT_FOUND -> "Nao encontrado";
			case UNAUTHORIZED -> "Nao autorizado";
			case FORBIDDEN -> "Acesso negado";
			case CONFLICT -> "Conflito";
			case UNPROCESSABLE_ENTITY -> "Dados invalidos";
			default -> "Erro";
		};
	}

}
