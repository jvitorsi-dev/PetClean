package br.com.fatecmaua.petclean.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/** US-03, US-05 e US-15: dados de entrada de cliente. */
@Schema(description = "Dados para cadastro/edicao de cliente")
public record ClienteRequest(

		@Schema(description = "Nome completo", example = "Maria da Silva")
		@NotBlank(message = "o nome e obrigatorio")
		@Size(min = 3, max = 120, message = "o nome deve ter entre 3 e 120 caracteres")
		String nome,

		@Schema(description = "CPF com 11 digitos (pontuacao e ignorada)", example = "123.456.789-01")
		@NotBlank(message = "o CPF e obrigatorio")
		@Pattern(regexp = "^\\d{3}\\.?\\d{3}\\.?\\d{3}-?\\d{2}$", message = "o CPF deve ter 11 digitos")
		String cpf,

		@Schema(description = "Telefone de contato", example = "(11) 98765-4321")
		@NotBlank(message = "o telefone e obrigatorio")
		@Size(min = 8, max = 20, message = "o telefone deve ter entre 8 e 20 caracteres")
		String telefone,

		@Schema(description = "E-mail de contato", example = "maria@email.com")
		@NotBlank(message = "o e-mail e obrigatorio")
		@Email(message = "informe um e-mail valido")
		String email,

		@Schema(description = "Endereco completo", example = "Rua das Flores, 100 - Santo Andre/SP")
		@NotBlank(message = "o endereco e obrigatorio")
		@Size(max = 200, message = "o endereco deve ter no maximo 200 caracteres")
		String endereco) {

}
