package br.com.fatecmaua.petclean.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/** US-01: login com e-mail e senha. */
@Schema(description = "Credenciais de acesso")
public record LoginRequest(

		@Schema(description = "E-mail do usuario", example = "helen@petclean.com")
		@NotBlank(message = "o e-mail e obrigatorio")
		@Email(message = "informe um e-mail valido")
		String email,

		@Schema(description = "Senha em texto puro (comparada com o hash bcrypt)", example = "petclean123")
		@NotBlank(message = "a senha e obrigatoria")
		String senha) {

}
