package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Porte fisico do pet (usado na escolha do servico)")
public enum PorteEnum {

	PEQUENO("Pequeno"), MEDIO("Medio"), GRANDE("Grande");

	private String descricao;

	PorteEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

}
