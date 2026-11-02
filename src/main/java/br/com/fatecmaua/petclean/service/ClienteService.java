package br.com.fatecmaua.petclean.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.ClienteRequest;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.projection.ClienteResumoProjection;
import br.com.fatecmaua.petclean.repository.AgendamentoRepository;
import br.com.fatecmaua.petclean.repository.ClienteRepository;
import br.com.fatecmaua.petclean.repository.PetRepository;

/**
 * Regras do EP-01 (Gerenciamento de Clientes):
 * US-03 (cadastrar), US-04 (consultar/filtrar), US-05 (editar),
 * US-06 (excluir com integridade referencial) e US-15 (CPF unico e valido).
 */
@Service
public class ClienteService {

	@Autowired
	private ClienteRepository repC;

	@Autowired
	private PetRepository repP;

	@Autowired
	private AgendamentoRepository repA;

	/** US-03 (2): salva e devolve o cliente criado com id. */
	@Transactional
	public Cliente cadastrar(ClienteRequest dados) {
		String cpf = ValidacaoCpf.normalizar(dados.cpf());
		validarCpf(cpf, null);

		Cliente cliente = new Cliente(null, dados.nome().trim(), cpf, dados.telefone().trim(), dados.email().trim(),
				dados.endereco().trim());
		return repC.save(cliente);
	}

	/** US-04 (1): lista completa para a tela de clientes. */
	@Transactional(readOnly = true)
	public List<Cliente> listar() {
		return repC.findAll();
	}

	/** US-04 (2): filtro por parte do nome ou do CPF. Termo vazio devolve a lista completa. */
	@Transactional(readOnly = true)
	public List<Cliente> filtrar(String termo) {
		if (termo == null || termo.isBlank()) {
			return repC.findAll();
		}
		return repC.filtrarPorNomeOuCpf(termo.trim());
	}

	/** US-04 (1) com projection otimizada: nome, CPF e telefone. */
	@Transactional(readOnly = true)
	public List<ClienteResumoProjection> filtrarResumo(String termo) {
		return repC.filtrarResumo(termo == null ? "" : termo.trim());
	}

	@Transactional(readOnly = true)
	public Cliente buscarPorId(Long id) {
		return repC.findById(id).orElseThrow(() -> ErroNegocioException.naoEncontrado(
				"Cliente com id " + id + " nao encontrado."));
	}

	/** US-05 (1)/(2): edita mantendo o CPF unico (US-05, criterio 3). */
	@Transactional
	public Cliente atualizar(Long id, ClienteRequest dados) {
		Cliente cliente = buscarPorId(id);
		String cpf = ValidacaoCpf.normalizar(dados.cpf());
		validarCpf(cpf, id);

		cliente.setNome(dados.nome().trim());
		cliente.setCpf(cpf);
		cliente.setTelefone(dados.telefone().trim());
		cliente.setEmail(dados.email().trim());
		cliente.setEndereco(dados.endereco().trim());
		return repC.save(cliente);
	}

	/**
	 * US-06 (2): cliente com pets ou agendamentos vinculados nao pode ser excluido
	 * (integridade referencial - RNF-09). A mensagem explica o motivo.
	 */
	@Transactional
	public void excluir(Long id) {
		Cliente cliente = buscarPorId(id);

		long pets = repP.countByClienteId(id);
		long agendamentos = repA.contarPorCliente(id);

		if (pets > 0 || agendamentos > 0) {
			throw ErroNegocioException.conflito("Nao e possivel excluir o cliente " + cliente.getNome()
					+ ": existem " + pets + " pet(s) e " + agendamentos
					+ " agendamento(s) vinculados. Remova ou transfira os vinculos primeiro (integridade referencial).");
		}

		repC.delete(cliente);
	}

	/** US-15 (1): bloqueia CPF ja existente. US-15 (3): valida o formato/digitos. */
	private void validarCpf(String cpf, Long idAtual) {
		if (!ValidacaoCpf.isValido(cpf)) {
			throw ErroNegocioException.dadosInvalidos("CPF invalido. Informe 11 digitos validos.");
		}
		boolean duplicado = idAtual == null ? repC.existsByCpf(cpf) : repC.existsByCpfAndIdNot(cpf, idAtual);
		if (duplicado) {
			throw ErroNegocioException.conflito("CPF ja cadastrado: " + ValidacaoCpf.formatar(cpf) + ".");
		}
	}

}
