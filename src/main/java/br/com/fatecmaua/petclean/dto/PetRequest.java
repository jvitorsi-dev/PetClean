package br.com.fatecmaua.petclean.dto;

import br.com.fatecmaua.petclean.model.EspecieEnum;
import br.com.fatecmaua.petclean.model.PorteEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/**
 * US-07, US-09: dados de entrada de pet.
 * O tutor e obrigatorio no cadastro; na edicao o campo idCliente e ignorado
 * (US-09, criterio 4: o tutor vinculado nao pode ser alterado por esta tela).
 */
@Schema(description = "Dados para cadastro/edicao de pet")
public record PetRequest(

		@Schema(description = "Id do tutor (obrigatorio no cadastro)", example = "1")
		@NotNull(message = "o tutor (idCliente) e obrigatorio")
		Long idCliente,

		@Schema(description = "Nome do pet", example = "Thor")
		@NotBlank(message = "o nome do pet e obrigatorio")
		@Size(min = 2, max = 80, message = "o nome deve ter entre 2 e 80 caracteres")
		String nome,

		@Schema(description = "Especie", example = "CACHORRO")
		@NotNull(message = "a especie e obrigatoria")
		EspecieEnum especie,

		@Schema(description = "Raca", example = "Golden Retriever")
		@NotBlank(message = "a raca e obrigatoria")
		@Size(max = 80, message = "a raca deve ter no maximo 80 caracteres")
		String raca,

		@Schema(description = "Porte", example = "GRANDE")
		@NotNull(message = "o porte e obrigatorio")
		PorteEnum porte,

		@Schema(description = "Idade em anos (0 a 40)", example = "4")
		@NotNull(message = "a idade e obrigatoria")
		@Min(value = 0, message = "a idade nao pode ser negativa")
		@Max(value = 40, message = "a idade deve ser no maximo 40 anos")
		Integer idade) {

}
