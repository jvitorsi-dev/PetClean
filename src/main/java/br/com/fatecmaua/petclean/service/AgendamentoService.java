package br.com.fatecmaua.petclean.service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.AgendamentoRequest;
import br.com.fatecmaua.petclean.dto.StatusRequest;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.Agendamento;
import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.model.Pet;
import br.com.fatecmaua.petclean.model.StatusAgendamentoEnum;
import br.com.fatecmaua.petclean.projection.AgendamentoProjection;
import br.com.fatecmaua.petclean.repository.AgendamentoRepository;
import br.com.fatecmaua.petclean.repository.ClienteRepository;
import br.com.fatecmaua.petclean.repository.PetRepository;

/**
 * Regras do EP-03 (Controle de Agendamentos):
 * US-11 (cadastrar), US-12 (listar com filtros), US-13 (atualizar status),
 * US-16 (cancelar liberando o horario) e US-17 (conflito de horario).
 */
@Service
public class AgendamentoService {

	@Autowired
	private AgendamentoRepository repA;

	@Autowired
	private ClienteRepository repC;

	@Autowired
	private PetRepository repP;

	/**
	 * US-11: cria o agendamento com status "Agendado".
	 * (2) valor e duracao vem do servico escolhido;
	 * (4)/(US-17) horario ja ocupado e bloqueado.
	 */
	@Transactional
	public Agendamento cadastrar(AgendamentoRequest dados) {
		Cliente cliente = repC.findById(dados.idCliente())
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Cliente nao encontrado."));
		Pet pet = repP.findById(dados.idPet())
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Pet nao encontrado."));

		// US-11 (1): o pet precisa pertencer ao cliente selecionado
		if (!pet.getCliente().getId().equals(cliente.getId())) {
			throw ErroNegocioException.dadosInvalidos(
					"O pet " + pet.getNome() + " nao pertence ao cliente " + cliente.getNome() + ".");
		}

		if (dados.data().isBefore(LocalDate.now())) {
			throw ErroNegocioException.dadosInvalidos("Nao e possivel agendar em data passada.");
		}

		// US-17 (1): impede duplicidade de dia + horario
		verificarConflito(dados.data(), dados.hora(), null);

		Agendamento agendamento = new Agendamento();
		agendamento.setCliente(cliente);
		agendamento.setPet(pet);
		agendamento.setServico(dados.servico());
		agendamento.setData(dados.data());
		agendamento.setHora(dados.hora().withSecond(0).withNano(0));
		agendamento.setValor(dados.servico().getValor());
		agendamento.setDuracaoMinutos(dados.servico().getDuracaoMinutos());
		agendamento.setObservacao(dados.observacao());
		agendamento.setStatus(StatusAgendamentoEnum.AGENDADO);
		agendamento.setAtualizadoEm(LocalDateTime.now());

		return repA.save(agendamento);
	}

	/** US-12: listagem com filtro opcional por data e por status. */
	@Transactional(readOnly = true)
	public List<Agendamento> listar(LocalDate data, StatusAgendamentoEnum status) {
		if (data != null && status != null) {
			return repA.findByDataAndStatusOrderByHora(data, status);
		}
		if (data != null) {
			return repA.findByDataOrderByHora(data);
		}
		if (status != null) {
			return repA.findByStatusOrderByDataAscHoraAsc(status);
		}
		return repA.findAllByOrderByDataDescHoraDesc();
	}

	/** US-12: agenda do dia em formato de projection (cliente, pet, servico, valor, status). */
	@Transactional(readOnly = true)
	public List<AgendamentoProjection> agendaDoDia(LocalDate data) {
		return repA.listarResumoDoDia(data == null ? LocalDate.now() : data);
	}

	@Transactional(readOnly = true)
	public Agendamento buscarPorId(Long id) {
		return repA.findById(id).orElseThrow(
				() -> ErroNegocioException.naoEncontrado("Agendamento com id " + id + " nao encontrado."));
	}

	/** US-05 do agendamento: edicao dos dados com nova checagem de conflito (US-17). */
	@Transactional
	public Agendamento atualizar(Long id, AgendamentoRequest dados) {
		Agendamento agendamento = buscarPorId(id);

		if (agendamento.getStatus() == StatusAgendamentoEnum.CANCELADO) {
			throw ErroNegocioException.conflito("Agendamento cancelado nao pode ser editado. Crie um novo agendamento.");
		}

		Cliente cliente = repC.findById(dados.idCliente())
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Cliente nao encontrado."));
		Pet pet = repP.findById(dados.idPet())
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Pet nao encontrado."));

		if (!pet.getCliente().getId().equals(cliente.getId())) {
			throw ErroNegocioException.dadosInvalidos("O pet informado nao pertence ao cliente selecionado.");
		}

		verificarConflito(dados.data(), dados.hora(), id);

		agendamento.setCliente(cliente);
		agendamento.setPet(pet);
		agendamento.setServico(dados.servico());
		agendamento.setValor(dados.servico().getValor());
		agendamento.setDuracaoMinutos(dados.servico().getDuracaoMinutos());
		agendamento.setData(dados.data());
		agendamento.setHora(dados.hora().withSecond(0).withNano(0));
		agendamento.setObservacao(dados.observacao());
		agendamento.setAtualizadoEm(LocalDateTime.now());

		return repA.save(agendamento);
	}

	/**
	 * US-13: atualiza o status e registra a data/hora da atualizacao (criterio 3).
	 * US-16 (2)/(3): o cancelamento libera o horario e nao e permitido para itens realizados.
	 */
	@Transactional
	public Agendamento atualizarStatus(Long id, StatusRequest dados) {
		Agendamento agendamento = buscarPorId(id);

		if (dados.status() == StatusAgendamentoEnum.CANCELADO) {
			return cancelar(id, dados.motivo());
		}

		if (agendamento.getStatus() == StatusAgendamentoEnum.CANCELADO) {
			throw ErroNegocioException.conflito("Agendamento cancelado nao pode mudar de status.");
		}

		agendamento.setStatus(dados.status());
		agendamento.setAtualizadoEm(LocalDateTime.now());
		return repA.save(agendamento);
	}

	/** US-16: cancelamento com confirmacao no cliente e liberacao do horario. */
	@Transactional
	public Agendamento cancelar(Long id, String motivo) {
		Agendamento agendamento = buscarPorId(id);

		if (!agendamento.getStatus().permiteCancelamento()) {
			throw ErroNegocioException.conflito(
					"Agendamento com status " + agendamento.getStatus().getDescricao() + " nao pode ser cancelado.");
		}

		agendamento.setStatus(StatusAgendamentoEnum.CANCELADO);
		agendamento.setMotivoCancelamento(motivo == null ? "Cancelado pelo atendente" : motivo);
		agendamento.setAtualizadoEm(LocalDateTime.now());
		// com o status CANCELADO o horario deixa de contar em contarConflitosNoHorario,
		// ou seja, volta a ficar disponivel (US-16, criterio 2)
		return repA.save(agendamento);
	}

	@Transactional
	public void excluir(Long id) {
		Agendamento agendamento = buscarPorId(id);
		repA.delete(agendamento);
	}

	/** US-17: alerta e impede duplicidade de horario no mesmo dia. */
	private void verificarConflito(LocalDate data, java.time.LocalTime hora, Long idIgnorado) {
		long conflitos = repA.contarConflitosNoHorario(data, hora, idIgnorado);
		if (conflitos > 0) {
			throw ErroNegocioException.conflito("Ja existe um agendamento em " + data + " as " + hora
					+ ". Escolha outro horario.");
		}
	}

}
