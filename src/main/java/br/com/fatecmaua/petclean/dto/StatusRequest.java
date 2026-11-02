package br.com.fatecmaua.petclean.dto;

import br.com.fatecmaua.petclean.model.StatusAgendamentoEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;

/** US-13 / US-16: alteracao de status do agendamento. */
@Schema(description = "Novo status do agendamento")
public record StatusRequest(

		@Schema(description = "Status desejado", example = "CONFIRMADO")
		@NotNull(message = "o status e obrigatorio")
		StatusAgendamentoEnum status,

		@Schema(description = "Motivo (usado no cancelamento - US-16)", example = "Cliente desmarcou por telefone")
		String motivo) {

}
