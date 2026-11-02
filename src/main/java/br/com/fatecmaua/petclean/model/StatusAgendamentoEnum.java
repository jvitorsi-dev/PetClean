package br.com.fatecmaua.petclean.model;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Status do agendamento (US-11, US-12, US-13, US-16).
 */
@Schema(description = "Status do agendamento no fluxo de atendimento")
public enum StatusAgendamentoEnum {

	AGENDADO("Agendado"), CONFIRMADO("Confirmado"),
	REALIZADO("Realizado"), CANCELADO("Cancelado");

	private String descricao;

	StatusAgendamentoEnum(String descricao) {
		this.descricao = descricao;
	}

	public String getDescricao() {
		return this.descricao;
	}

	/**
	 * US-16 (2): cancelar libera o horario; (3) agendamento ja realizado nao pode ser cancelado.
	 */
	public boolean permiteCancelamento() {
		return this == AGENDADO || this == CONFIRMADO;
	}

	/**
	 * US-13 (2): um agendamento realizado nao conta mais como pendente do dia.
	 */
	public boolean estaPendente() {
		return this == AGENDADO || this == CONFIRMADO;
	}

}
