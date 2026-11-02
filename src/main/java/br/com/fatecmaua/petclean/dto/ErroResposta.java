package br.com.fatecmaua.petclean.dto;

import java.time.LocalDateTime;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Corpo padrao de erro da API. Mantem a mesma estrutura para erros de validacao,
 * regras de negocio e erros inesperados.
 */
@Schema(description = "Resposta padrao de erro da API")
public record ErroResposta(

		@Schema(description = "Status HTTP", example = "409") int status,

		@Schema(description = "Categoria do erro", example = "Conflito") String erro,

		@Schema(description = "Mensagem legivel para o usuario", example = "CPF ja cadastrado") String mensagem,

		@Schema(description = "Detalhes por campo, quando houver erro de validacao") List<String> detalhes,

		@Schema(description = "Momento em que o erro foi gerado") LocalDateTime momento,

		@Schema(description = "Rota da requisicao", example = "/clientes") String rota) {

	public ErroResposta(int status, String erro, String mensagem, List<String> detalhes, String rota) {
		this(status, erro, mensagem, detalhes, LocalDateTime.now(), rota);
	}

}
