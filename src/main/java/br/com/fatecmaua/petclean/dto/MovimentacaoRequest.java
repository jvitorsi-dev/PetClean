package br.com.fatecmaua.petclean.dto;

import br.com.fatecmaua.petclean.model.TipoMovimentacaoEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

/** US-19: registro de entrada/saida de estoque. */
@Schema(description = "Movimentacao de estoque (entrada ou saida)")
public record MovimentacaoRequest(

		@Schema(description = "Tipo da movimentacao", example = "SAIDA")
		@NotNull(message = "o tipo da movimentacao e obrigatorio")
		TipoMovimentacaoEnum tipo,

		@Schema(description = "Quantidade movimentada (maior que zero)", example = "2")
		@NotNull(message = "a quantidade e obrigatoria")
		@Min(value = 1, message = "a quantidade deve ser maior que zero")
		Integer quantidade,

		@Schema(description = "Observacao", example = "Venda no balcao")
		String observacao) {

}
