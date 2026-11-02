package br.com.fatecmaua.petclean.control;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.dto.AgendamentoRequest;
import br.com.fatecmaua.petclean.dto.StatusRequest;
import br.com.fatecmaua.petclean.model.Agendamento;
import br.com.fatecmaua.petclean.model.StatusAgendamentoEnum;
import br.com.fatecmaua.petclean.projection.AgendamentoProjection;
import br.com.fatecmaua.petclean.service.AgendamentoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

/**
 * EP-03 - Controle de Agendamentos (US-11, US-12, US-13, US-16 e US-17).
 */
@RestController
@RequestMapping("/api/agendamentos")
@Tag(name = "03 - Agendamentos", description = "Agenda de servicos com status e controle de conflitos (EP-03)")
public class AgendamentoController {

	@Autowired
	private AgendamentoService agendamentoService;

	@Operation(description = "US-12 - Lista agendamentos com filtro opcional por data (AAAA-MM-DD) "
			+ "e por status (AGENDADO, CONFIRMADO, REALIZADO, CANCELADO).", tags = "03 - Agendamentos")
	@GetMapping
	public List<Agendamento> listar(
			@RequestParam(name = "data", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate data,
			@RequestParam(name = "status", required = false) StatusAgendamentoEnum status) {
		return agendamentoService.listar(data, status);
	}

	@Operation(description = "US-12 - Agenda do dia em versao otimizada (SQL nativo + projection), "
			+ "ordenada por horario. Sem o parametro 'data' usa a data atual.", tags = "03 - Agendamentos")
	@GetMapping("/agenda")
	public List<AgendamentoProjection> agendaDoDia(
			@RequestParam(name = "data", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate data) {
		return agendamentoService.agendaDoDia(data);
	}

	@Operation(description = "US-11 - Retorna um agendamento pelo id.", tags = "03 - Agendamentos")
	@GetMapping("/{id}")
	public Agendamento buscarPorId(@PathVariable Long id) {
		return agendamentoService.buscarPorId(id);
	}

	@Operation(description = "US-11 - Cadastra um agendamento com status 'Agendado'. "
			+ "O valor e a duracao vem do servico escolhido. "
			+ "US-17: horario ja ocupado devolve 409 sem gravar.", tags = "03 - Agendamentos")
	@PostMapping
	public ResponseEntity<Agendamento> cadastrar(@RequestBody @Valid AgendamentoRequest dados) {
		Agendamento agendamento = agendamentoService.cadastrar(dados);
		return ResponseEntity.status(HttpStatus.CREATED).body(agendamento);
	}

	@Operation(description = "US-11/US-17 - Edita um agendamento, refazendo a checagem de conflito de horario.", tags = "03 - Agendamentos")
	@PutMapping("/{id}")
	public Agendamento atualizar(@PathVariable Long id, @RequestBody @Valid AgendamentoRequest dados) {
		return agendamentoService.atualizar(id, dados);
	}

	@Operation(description = "US-13 - Atualiza o status do agendamento e registra a data/hora da alteracao. "
			+ "Status CANCELADO aciona o fluxo de cancelamento (US-16).", tags = "03 - Agendamentos")
	@PatchMapping("/{id}/status")
	public Agendamento atualizarStatus(@PathVariable Long id, @RequestBody @Valid StatusRequest dados) {
		return agendamentoService.atualizarStatus(id, dados);
	}

	@Operation(description = "US-16 - Cancela o agendamento e libera o horario. "
			+ "Agendamento ja realizado nao pode ser cancelado (409).", tags = "03 - Agendamentos")
	@PatchMapping("/{id}/cancelar")
	public Agendamento cancelar(@PathVariable Long id,
			@RequestParam(name = "motivo", required = false) String motivo) {
		return agendamentoService.cancelar(id, motivo);
	}

	@Operation(description = "Remove um agendamento do banco (uso administrativo). "
			+ "Para o fluxo normal prefira o cancelamento.", tags = "03 - Agendamentos")
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> excluir(@PathVariable Long id) {
		agendamentoService.excluir(id);
		return ResponseEntity.noContent().build();
	}

}
