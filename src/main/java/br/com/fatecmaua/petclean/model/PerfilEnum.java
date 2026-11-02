package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Perfil de acesso do usuario do sistema")
public enum PerfilEnum {

	ATENDENTE("Atendente"), GESTOR("Gestor/Proprietario");

	private String descricao;

	PerfilEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

}
