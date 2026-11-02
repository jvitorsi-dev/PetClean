package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Especie do pet atendido pelo pet shop")
public enum EspecieEnum {

	CACHORRO("Cachorro"), GATO("Gato"), AVE("Ave"),
	ROEDOR("Roedor"), REPTIL("Reptil"), OUTRO("Outro");

	private String descricao;

	EspecieEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

}
