package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Categoria do produto no estoque")
public enum CategoriaProdutoEnum {

	RACAO("Racao"), MEDICAMENTO("Medicamento"), HIGIENE("Higiene"),
	BRINQUEDO("Brinquedo"), ACESSORIO("Acessorio"), OUTRO("Outro");

	private String descricao;

	CategoriaProdutoEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

}
