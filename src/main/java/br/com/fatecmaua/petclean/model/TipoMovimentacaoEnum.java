package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Tipo de movimentacao de estoque (US-19).
 */
@Schema(description = "Tipo de movimentacao de estoque: entrada ou saida")
public enum TipoMovimentacaoEnum {

	ENTRADA("Entrada"), SAIDA("Saida");

	private String descricao;

	TipoMovimentacaoEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

}
