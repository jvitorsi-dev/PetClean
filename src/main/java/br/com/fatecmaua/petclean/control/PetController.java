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

import br.com.fatecmaua.petclean.dto.PetRequest;
import br.com.fatecmaua.petclean.model.Pet;
import br.com.fatecmaua.petclean.projection.PetResumoProjection;
import br.com.fatecmaua.petclean.service.PetService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

/**
 * EP-02 - Gerenciamento de Pets (US-07, US-08, US-09 e US-10).
 */
@RestController
@RequestMapping("/api/pets")
@Tag(name = "02 - Pets", description = "Cadastro, consulta, edicao e exclusao de pets (EP-02)")
public class PetController {

	@Autowired
	private PetService petService;

	@Operation(description = "US-08 - Consulta e filtra pets por nome do pet ou do tutor.", tags = "02 - Pets")
	@GetMapping
	public List<Pet> listar(@RequestParam(name = "termo", required = false) String termo) {
		return petService.filtrar(termo);
	}

	@Operation(description = "US-08 - Versao otimizada (SQL nativo + projection) "
			+ "com nome do pet, especie e tutor.", tags = "02 - Pets")
	@GetMapping("/resumo")
	public List<PetResumoProjection> listarResumo(@RequestParam(name = "termo", required = false) String termo) {
		return petService.filtrarResumo(termo);
	}

	@Operation(description = "US-11 - Lista somente os pets do cliente selecionado "
			+ "(usado pelo formulario de agendamento).", tags = "02 - Pets")
	@GetMapping("/cliente/{idCliente}")
	public List<Pet> listarPorCliente(@PathVariable Long idCliente) {
		return petService.listarPorCliente(idCliente);
	}

	@Operation(description = "US-09 - Retorna um pet pelo id.", tags = "02 - Pets")
	@GetMapping("/{id}")
	public Pet buscarPorId(@PathVariable Long id) {
		return petService.buscarPorId(id);
	}

	@Operation(description = "US-07 - Cadastra um pet vinculado a um tutor. "
			+ "Tutor ausente devolve 422 e idade invalida devolve 400.", tags = "02 - Pets")
	@PostMapping
	public ResponseEntity<Pet> cadastrar(@RequestBody @Valid PetRequest dados) {
		Pet pet = petService.cadastrar(dados);
		return ResponseEntity.status(HttpStatus.CREATED).body(pet);
	}

	@Operation(description = "US-09 - Edita os dados do pet. O tutor vinculado nao e alterado por esta rota.", tags = "02 - Pets")
	@PutMapping("/{id}")
	public Pet atualizar(@PathVariable Long id, @RequestBody @Valid PetRequest dados) {
		return petService.atualizar(id, dados);
	}

	@Operation(description = "US-10 - Exclui o pet quando nao ha agendamento futuro "
			+ "nem historico de atendimento.", tags = "02 - Pets")
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> excluir(@PathVariable Long id) {
		petService.excluir(id);
		return ResponseEntity.noContent().build();
	}

}
