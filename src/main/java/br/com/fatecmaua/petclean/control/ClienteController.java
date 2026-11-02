package br.com.fatecmaua.petclean.control;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.dto.ClienteRequest;
import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.projection.ClienteResumoProjection;
import br.com.fatecmaua.petclean.service.ClienteService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

/**
 * EP-01 - Gerenciamento de Clientes (US-03, US-04, US-05, US-06 e US-15).
 */
@RestController
@RequestMapping("/api/clientes")
@Tag(name = "01 - Clientes", description = "Cadastro, consulta, edicao e exclusao de clientes (EP-01)")
public class ClienteController {

	@Autowired
	private ClienteService clienteService;

	@Operation(description = "US-04 - Consulta e filtra a lista de clientes por nome ou CPF. "
			+ "Sem o parametro 'termo' devolve todos os clientes.", tags = "01 - Clientes")
	@GetMapping
	public List<Cliente> listar(@RequestParam(name = "termo", required = false) String termo) {
		return clienteService.filtrar(termo);
	}

	@Operation(description = "US-04 - Versao otimizada da listagem (SQL nativo + projection) "
			+ "com nome, CPF e telefone.", tags = "01 - Clientes")
	@GetMapping("/resumo")
	public List<ClienteResumoProjection> listarResumo(@RequestParam(name = "termo", required = false) String termo) {
		return clienteService.filtrarResumo(termo);
	}

	@Operation(description = "US-05 - Retorna um cliente pelo id.", tags = "01 - Clientes")
	@GetMapping("/{id}")
	public Cliente buscarPorId(@PathVariable Long id) {
		return clienteService.buscarPorId(id);
	}

	@Operation(description = "US-03 / US-15 - Cadastra um novo cliente. Campos obrigatorios validados; "
			+ "CPF invalido devolve 422 e CPF repetido devolve 409 'CPF ja cadastrado'.", tags = "01 - Clientes")
	@PostMapping
	public ResponseEntity<Cliente> cadastrar(@RequestBody @Valid ClienteRequest dados) {
		Cliente cliente = clienteService.cadastrar(dados);
		return ResponseEntity.status(HttpStatus.CREATED).body(cliente);
	}

	@Operation(description = "US-05 - Edita os dados de um cliente; o CPF continua unico (US-15).", tags = "01 - Clientes")
	@PutMapping("/{id}")
	public Cliente atualizar(@PathVariable Long id, @RequestBody @Valid ClienteRequest dados) {
		return clienteService.atualizar(id, dados);
	}

	@Operation(description = "US-06 - Exclui um cliente sem vinculos. "
			+ "Cliente com pets ou agendamentos nao pode ser excluido (integridade referencial - RNF-09).", tags = "01 - Clientes")
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> excluir(@PathVariable Long id) {
		clienteService.excluir(id);
		return ResponseEntity.noContent().build();
	}

}
