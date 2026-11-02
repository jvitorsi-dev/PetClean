package br.com.fatecmaua.petclean.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.MovimentacaoRequest;
import br.com.fatecmaua.petclean.dto.ProdutoRequest;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import br.com.fatecmaua.petclean.model.MovimentacaoEstoque;
import br.com.fatecmaua.petclean.model.Produto;
import br.com.fatecmaua.petclean.model.TipoMovimentacaoEnum;
import br.com.fatecmaua.petclean.projection.ProdutoProjection;
import br.com.fatecmaua.petclean.repository.MovimentacaoEstoqueRepository;
import br.com.fatecmaua.petclean.repository.ProdutoRepository;

/**
 * Regras do EP-04 (Controle de Estoque):
 * US-18 (cadastrar), US-19 (movimentar quantidade), US-20 (alerta critico),
 * US-21 (excluir x inativar) e US-25 (buscar por nome/categoria).
 */
@Service
public class ProdutoService {

	@Autowired
	private ProdutoRepository repProd;

	@Autowired
	private MovimentacaoEstoqueRepository repMov;

	/** US-18: cadastra com validacao de quantidade/preco (criterio 2). */
	@Transactional
	public Produto cadastrar(ProdutoRequest dados) {
		validarValores(dados);

		Produto produto = new Produto(null, dados.nome().trim(), dados.categoria(), dados.quantidade(),
				dados.estoqueMinimo(), dados.preco(), Boolean.TRUE);

		produto = repProd.save(produto);

		// US-19: a quantidade inicial tambem entra no historico de movimentacao
		if (dados.quantidade() > 0) {
			repMov.save(new MovimentacaoEstoque(null, produto, TipoMovimentacaoEnum.ENTRADA, dados.quantidade(),
					"Saldo inicial do cadastro"));
		}
		return produto;
	}

	@Transactional(readOnly = true)
	public List<Produto> listar() {
		return repProd.findAllByOrderByNomeAsc();
	}

	/** US-25: busca por nome e, opcionalmente, por categoria. */
	@Transactional(readOnly = true)
	public List<Produto> buscar(String termo, CategoriaProdutoEnum categoria) {
		boolean semTermo = termo == null || termo.isBlank();

		if (semTermo && categoria == null) {
			return repProd.findAllByOrderByNomeAsc();
		}
		if (semTermo) {
			return repProd.findByCategoriaOrderByNomeAsc(categoria);
		}
		if (categoria == null) {
			return repProd.buscarPorNome(termo.trim());
		}
		return repProd.buscarPorNomeECategoria(termo.trim(), categoria);
	}

	/** US-25: busca otimizada com projection. */
	@Transactional(readOnly = true)
	public List<ProdutoProjection> buscarResumo(String termo) {
		return repProd.buscarResumo(termo == null ? "" : termo.trim());
	}

	/** US-20 (1) e US-24 (1): do mais critico para o menos critico. */
	@Transactional(readOnly = true)
	public List<Produto> estoqueCritico() {
		return repProd.listarEstoqueCritico();
	}

	@Transactional(readOnly = true)
	public Produto buscarPorId(Long id) {
		return repProd.findById(id)
				.orElseThrow(() -> ErroNegocioException.naoEncontrado("Produto com id " + id + " nao encontrado."));
	}

	@Transactional
	public Produto atualizar(Long id, ProdutoRequest dados) {
		validarValores(dados);
		Produto produto = buscarPorId(id);

		produto.setNome(dados.nome().trim());
		produto.setCategoria(dados.categoria());
		produto.setEstoqueMinimo(dados.estoqueMinimo());
		produto.setPreco(dados.preco());

		// ajuste direto de quantidade gera movimentacao (US-19)
		int diferenca = dados.quantidade() - produto.getQuantidade();
		if (diferenca != 0) {
			TipoMovimentacaoEnum tipo = diferenca > 0 ? TipoMovimentacaoEnum.ENTRADA : TipoMovimentacaoEnum.SAIDA;
			repMov.save(new MovimentacaoEstoque(null, produto, tipo, Math.abs(diferenca), "Ajuste pela edicao"));
			produto.setQuantidade(dados.quantidade());
		}
		return repProd.save(produto);
	}

	/**
	 * US-19: registra entrada ou saida.
	 * (2) saida maior que o disponivel e impedida;
	 * (3) ao ficar igual/abaixo do minimo o alerta critico passa a valer.
	 */
	@Transactional
	public Produto movimentar(Long id, MovimentacaoRequest dados) {
		Produto produto = buscarPorId(id);

		if (dados.tipo() == TipoMovimentacaoEnum.SAIDA && dados.quantidade() > produto.getQuantidade()) {
			throw ErroNegocioException.conflito("Saida de " + dados.quantidade() + " unidade(s) nao permitida: "
					+ "disponivel em estoque: " + produto.getQuantidade() + ".");
		}

		int novaQuantidade = dados.tipo() == TipoMovimentacaoEnum.ENTRADA
				? produto.getQuantidade() + dados.quantidade()
				: produto.getQuantidade() - dados.quantidade();

		produto.setQuantidade(novaQuantidade);
		repProd.save(produto);
		repMov.save(new MovimentacaoEstoque(null, produto, dados.tipo(), dados.quantidade(),
				dados.observacao() == null ? "Movimentacao manual" : dados.observacao()));

		return produto;
	}

	/**
	 * US-21: produto sem movimentacao pode ser excluido; com historico a exclusao e
	 * impedida e o sistema sugere inativar o item.
	 */
	@Transactional
	public void excluir(Long id) {
		Produto produto = buscarPorId(id);

		if (repMov.existsByProduto(produto)) {
			throw ErroNegocioException.conflito("O produto " + produto.getNome()
					+ " possui historico de movimentacao e nao pode ser excluido. "
					+ "Sugestao: inative o produto (PATCH /produtos/" + id + "/inativar).");
		}
		repProd.delete(produto);
	}

	/** US-21 (2): alternativa a exclusao para itens com historico. */
	@Transactional
	public Produto inativar(Long id, boolean ativo) {
		Produto produto = buscarPorId(id);
		produto.setAtivo(ativo);
		return repProd.save(produto);
	}

	@Transactional(readOnly = true)
	public List<MovimentacaoEstoque> movimentacoes(Long idProduto) {
		if (idProduto == null) {
			return repMov.findAllByOrderByRegistradoEmDesc();
		}
		buscarPorId(idProduto);
		return repMov.findByProdutoIdOrderByRegistradoEmDesc(idProduto);
	}

	private void validarValores(ProdutoRequest dados) {
		if (dados.quantidade() < 0 || dados.estoqueMinimo() < 0) {
			throw ErroNegocioException.dadosInvalidos("Quantidade e estoque minimo nao podem ser negativos.");
		}
		if (dados.preco() == null || dados.preco().signum() < 0) {
			throw ErroNegocioException.dadosInvalidos("O preco nao pode ser negativo.");
		}
	}

}
