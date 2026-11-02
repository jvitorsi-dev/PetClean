package br.com.fatecmaua.petclean.dto;

import java.time.LocalDate;
import java.time.LocalTime;

import com.fasterxml.jackson.annotation.JsonFormat;

import br.com.fatecmaua.petclean.model.ServicoEnum;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/** US-11 e US-17: dados de entrada de agendamento. */
@Schema(description = "Dados para cadastro/edicao de agendamento")
public record AgendamentoRequest(

		@Schema(description = "Id do cliente", example = "1")
		@NotNull(message = "o cliente e obrigatorio")
		Long idCliente,

		@Schema(description = "Id do pet (precisa pertencer ao cliente informado)", example = "1")
		@NotNull(message = "o pet e obrigatorio")
		Long idPet,

		@Schema(description = "Servico escolhido", example = "BANHO_E_TOSA")
		@NotNull(message = "o servico e obrigatorio")
		ServicoEnum servico,

		@Schema(description = "Data do atendimento (AAAA-MM-DD)", example = "2026-11-05")
		@NotNull(message = "a data e obrigatoria")
		@JsonFormat(pattern = "yyyy-MM-dd")
		LocalDate data,

		@Schema(description = "Horario do atendimento (HH:mm)", example = "09:00")
		@NotNull(message = "o horario e obrigatorio")
		@JsonFormat(pattern = "HH:mm")
		LocalTime hora,

		@Schema(description = "Observacoes", example = "Pet com pele sensivel")
		@Size(max = 255, message = "a observacao deve ter no maximo 255 caracteres")
		String observacao) {

}
