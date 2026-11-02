package br.com.fatecmaua.petclean.model;

import java.math.BigDecimal;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Catalogo de servicos do pet shop (US-11, criterio 2: ao selecionar o servico
 * o sistema deve exibir valor e duracao).
 */
@Schema(description = "Servico oferecido pelo pet shop, com valor e duracao padrao")
public enum ServicoEnum {

	BANHO("Banho", 45, "45.00"),
	TOSA("Tosa", 40, "50.00"),
	BANHO_E_TOSA("Banho e Tosa", 75, "85.00"),
	HIDRATACAO("Hidratacao", 50, "60.00"),
	CONSULTA_VETERINARIA("Consulta Veterinaria", 30, "120.00");

	private final String descricao;
	private final Integer duracaoMinutos;
	private final BigDecimal valor;

	ServicoEnum(String descricao, Integer duracaoMinutos, String valor) {
		this.descricao = descricao;
		this.duracaoMinutos = duracaoMinutos;
		this.valor = new BigDecimal(valor);
	}

	public String getDescricao() {
		return descricao;
	}

	public Integer getDuracaoMinutos() {
		return duracaoMinutos;
	}

	public BigDecimal getValor() {
		return valor;
	}

}
