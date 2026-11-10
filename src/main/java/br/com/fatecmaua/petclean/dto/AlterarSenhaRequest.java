package br.com.fatecmaua.petclean.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * Alteracao de senha pelo proprio usuario (equivalente ao perfil/alterar_senha.php).
 * Exige a senha atual, como no formulario original (RNF-04: bcrypt).
 */
@Schema(description = "Dados para alterar a senha do usuario autenticado")
public record AlterarSenhaRequest(

		@Schema(description = "Senha atual", example = "petclean123")
		@NotBlank(message = "a senha atual e obrigatoria")
		String senhaAtual,

		@Schema(description = "Nova senha (minimo 6 caracteres)", example = "novaSenha123")
		@NotBlank(message = "a nova senha e obrigatoria")
		@Size(min = 6, max = 60, message = "a nova senha deve ter entre 6 e 60 caracteres")
		String novaSenha) {

}
