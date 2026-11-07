package br.com.fatecmaua.petclean.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * Dados editaveis na tela de Perfil (equivalente ao perfil/atualizar.php do projeto PHP).
 * Telefone, nome do pet shop e endereco sao opcionais, como no formulario original.
 */
@Schema(description = "Dados para atualizar o perfil do usuario autenticado")
public record AtualizarPerfilRequest(

		@Schema(description = "Nome completo", example = "Helen Vitoria Silva Aclina")
		@NotBlank(message = "o nome e obrigatorio")
		@Size(min = 3, max = 120, message = "o nome deve ter entre 3 e 120 caracteres")
		String nome,

		@Schema(description = "E-mail usado como login", example = "helen@petclean.com")
		@NotBlank(message = "o e-mail e obrigatorio")
		@Email(message = "informe um e-mail valido")
		@Size(max = 120, message = "o e-mail deve ter no maximo 120 caracteres")
		String email,

		@Schema(description = "Telefone de contato", example = "(11) 98765-4321")
		@Size(max = 20, message = "o telefone deve ter no maximo 20 caracteres")
		String telefone,

		@Schema(description = "Nome do pet shop", example = "PetClean Central")
		@Size(max = 120, message = "o nome do pet shop deve ter no maximo 120 caracteres")
		String nomePetshop,

		@Schema(description = "Endereco", example = "Rua das Flores, 123 - Santo Andre/SP")
		@Size(max = 200, message = "o endereco deve ter no maximo 200 caracteres")
		String endereco) {

}
