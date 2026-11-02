package br.com.fatecmaua.petclean.service;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.PetRequest;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.model.Pet;
import br.com.fatecmaua.petclean.projection.PetResumoProjection;
import br.com.fatecmaua.petclean.repository.AgendamentoRepository;
import br.com.fatecmaua.petclean.repository.ClienteRepository;
import br.com.fatecmaua.petclean.repository.PetRepository;

/**
 * Regras do EP-02 (Gerenciamento de Pets):
 * US-07 (cadastrar vinculado ao tutor), US-08 (consultar/filtrar),
 * US-09 (editar sem trocar o tutor) e US-10 (excluir com alerta de vinculo futuro).
 */
@Service
public class PetService {

	@Autowired
	private PetRepository repP;

	@Autowired
	private ClienteRepository repC;

	@Autowired
	private AgendamentoRepository repA;

	/** US-07 (1): sem tutor selecionado o salvamento e impedido. */
	@Transactional
	public Pet cadastrar(PetRequest dados) {
		Cliente tutor = repC.findById(dados.idCliente())
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Tutor nao encontrado para o id informado."));

		Pet pet = new Pet(null, tutor, dados.nome().trim(), dados.especie(), dados.raca().trim(), dados.porte(),
				dados.idade());
		return repP.save(pet);
	}

	/** US-08 (1): lista de pets com tutor. */
	@Transactional(readOnly = true)
	public List<Pet> listar() {
		return repP.findAll();
	}

	/** US-08 (2): filtro por parte do nome do pet ou do tutor. */
	@Transactional(readOnly = true)
	public List<Pet> filtrar(String termo) {
		if (termo == null || termo.isBlank()) {
			return repP.findAll();
		}
		return repP.filtrarPorNomePetOuTutor(termo.trim());
	}

	/** US-08 (1) via projection: nome do pet, especie e tutor. */
	@Transactional(readOnly = true)
	public List<PetResumoProjection> filtrarResumo(String termo) {
		return repP.filtrarResumo(termo == null ? "" : termo.trim());
	}

	/** US-11 (1): pets de um cliente especifico. */
	@Transactional(readOnly = true)
	public List<Pet> listarPorCliente(Long idCliente) {
		return repP.listarPorCliente(idCliente);
	}

	@Transactional(readOnly = true)
	public Pet buscarPorId(Long id) {
		return repP.findById(id)
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Pet com id " + id + " nao encontrado."));
	}

	/**
	 * US-09: edita os dados do pet. O tutor vinculado nao e alterado por esta tela
	 * (criterio 4), mesmo que um idCliente diferente seja enviado.
	 */
	@Transactional
	public Pet atualizar(Long id, PetRequest dados) {
		Pet pet = buscarPorId(id);

		pet.setNome(dados.nome().trim());
		pet.setEspecie(dados.especie());
		pet.setRaca(dados.raca().trim());
		pet.setPorte(dados.porte());
		pet.setIdade(dados.idade());
		return repP.save(pet);
	}

	/** US-10 (2): pet com agendamento futuro nao pode ser excluido. */
	@Transactional
	public void excluir(Long id) {
		Pet pet = buscarPorId(id);

		long futuros = repA.contarAgendamentosFuturosDoPet(id, LocalDate.now());
		if (futuros > 0) {
			throw ErroNegocioException.conflito("Nao e possivel excluir o pet " + pet.getNome() + ": existe(m) "
					+ futuros + " agendamento(s) futuro(s). Cancele os agendamentos antes de excluir.");
		}

		long historico = repA.findByPetIdOrderByDataDescHoraDesc(id).size();
		if (historico > 0) {
			throw ErroNegocioException.conflito("O pet " + pet.getNome() + " possui historico de "
					+ historico + " agendamento(s) e nao pode ser excluido para preservar o historico.");
		}

		repP.delete(pet);
	}

}
