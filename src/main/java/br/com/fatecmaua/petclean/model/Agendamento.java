package br.com.fatecmaua.petclean.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/**
 * Agendamento de servico. EP-03 (Controle de Agendamentos).
 * US-11 (cadastro), US-12 (listagem/filtros), US-13 (status), US-16 (cancelamento),
 * US-17 (conflito de horario).
 */
@Schema(description = "Esta e uma entidade que representa um agendamento de servico")
@Entity
@Table(name = "agendamento")
public class Agendamento {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Cliente (tutor) do atendimento", example = "Maria da Silva")
	@ManyToOne(optional = false)
	@JoinColumn(name = "fk_cliente", nullable = false)
	private Cliente cliente;

	@Schema(description = "Pet que sera atendido", example = "Thor")
	@ManyToOne(optional = false)
	@JoinColumn(name = "fk_pet", nullable = false)
	private Pet pet;

	@Schema(description = "Servico contratado", example = "BANHO_E_TOSA")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 30)
	private ServicoEnum servico;

	@Schema(description = "Data do atendimento", example = "2026-11-05")
	@Column(nullable = false)
	private LocalDate data;

	@Schema(description = "Horario de inicio do atendimento", example = "09:00")
	@Column(nullable = false)
	private LocalTime hora;

	@Schema(description = "Valor cobrado pelo servico", example = "85.00")
	@Column(nullable = false, precision = 10, scale = 2)
	private BigDecimal valor;

	@Schema(description = "Duracao do servico em minutos", example = "75")
	@Column(nullable = false)
	private Integer duracaoMinutos;

	@Schema(description = "Status atual do agendamento", example = "AGENDADO")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 20)
	private StatusAgendamentoEnum status;

	@Schema(description = "Observacoes do atendimento", example = "Pet com pele sensivel")
	@Column(length = 255)
	private String observacao;

	/** US-13 (3): data/hora da ultima alteracao de status. */
	@Schema(description = "Data/hora da ultima atualizacao do status")
	@Column(name = "atualizado_em")
	private LocalDateTime atualizadoEm;

	/** US-16 (3): motivo registrado no cancelamento. */
	@Schema(description = "Motivo do cancelamento, quando houver", example = "Cliente desmarcou por telefone")
	@Column(name = "motivo_cancelamento", length = 255)
	private String motivoCancelamento;

	public Agendamento() {

	}

	public Agendamento(Long id, Cliente cliente, Pet pet, ServicoEnum servico, LocalDate data, LocalTime hora,
			StatusAgendamentoEnum status) {
		this.id = id;
		this.cliente = cliente;
		this.pet = pet;
		this.servico = servico;
		this.data = data;
		this.hora = hora;
		this.status = status;
		this.valor = servico.getValor();
		this.duracaoMinutos = servico.getDuracaoMinutos();
	}

	/** Horario de termino, calculado a partir da duracao do servico. */
	public LocalTime getHoraFim() {
		if (hora == null || duracaoMinutos == null) {
			return null;
		}
		return hora.plusMinutes(duracaoMinutos);
	}

	public LocalDateTime getInicio() {
		return LocalDateTime.of(data, hora);
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}

	public Pet getPet() {
		return pet;
	}

	public void setPet(Pet pet) {
		this.pet = pet;
	}

	public ServicoEnum getServico() {
		return servico;
	}

	public void setServico(ServicoEnum servico) {
		this.servico = servico;
	}

	public LocalDate getData() {
		return data;
	}

	public void setData(LocalDate data) {
		this.data = data;
	}

	public LocalTime getHora() {
		return hora;
	}

	public void setHora(LocalTime hora) {
		this.hora = hora;
	}

	public BigDecimal getValor() {
		return valor;
	}

	public void setValor(BigDecimal valor) {
		this.valor = valor;
	}

	public Integer getDuracaoMinutos() {
		return duracaoMinutos;
	}

	public void setDuracaoMinutos(Integer duracaoMinutos) {
		this.duracaoMinutos = duracaoMinutos;
	}

	public StatusAgendamentoEnum getStatus() {
		return status;
	}

	public void setStatus(StatusAgendamentoEnum status) {
		this.status = status;
	}

	public String getObservacao() {
		return observacao;
	}

	public void setObservacao(String observacao) {
		this.observacao = observacao;
	}

	public LocalDateTime getAtualizadoEm() {
		return atualizadoEm;
	}

	public void setAtualizadoEm(LocalDateTime atualizadoEm) {
		this.atualizadoEm = atualizadoEm;
	}

	public String getMotivoCancelamento() {
		return motivoCancelamento;
	}

	public void setMotivoCancelamento(String motivoCancelamento) {
		this.motivoCancelamento = motivoCancelamento;
	}

}
