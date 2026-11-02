package br.com.fatecmaua.petclean.dto;

import java.math.BigDecimal;

import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/** US-18: dados de entrada de produto. */
@Schema(description = "Dados para cadastro/edicao de produto do estoque")
public record ProdutoRequest(

		@Schema(description = "Nome do produto", example = "Racao Premium Adulto 10kg")
		@NotBlank(message = "o nome do produto e obrigatorio")
		@Size(max = 120, message = "o nome deve ter no maximo 120 caracteres")
		String nome,

		@Schema(description = "Categoria", example = "RACAO")
		@NotNull(message = "a categoria e obrigatoria")
		CategoriaProdutoEnum categoria,

		@Schema(description = "Quantidade inicial em estoque (nao pode ser negativa)", example = "12")
		@NotNull(message = "a quantidade e obrigatoria")
		@Min(value = 0, message = "a quantidade nao pode ser negativa")
		Integer quantidade,

		@Schema(description = "Estoque minimo para o alerta de estoque critico", example = "5")
		@NotNull(message = "o estoque minimo e obrigatorio")
		@Min(value = 0, message = "o estoque minimo nao pode ser negativo")
		Integer estoqueMinimo,

		@Schema(description = "Preco unitario (nao pode ser negativo)", example = "189.90")
		@NotNull(message = "o preco e obrigatorio")
		@DecimalMin(value = "0.0", inclusive = true, message = "o preco nao pode ser negativo")
		BigDecimal preco) {

}
