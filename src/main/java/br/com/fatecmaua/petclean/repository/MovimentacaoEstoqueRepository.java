package br.com.fatecmaua.petclean.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.fatecmaua.petclean.model.MovimentacaoEstoque;
import br.com.fatecmaua.petclean.model.Produto;

public interface MovimentacaoEstoqueRepository extends JpaRepository<MovimentacaoEstoque, Long> {

	/** US-21 (2): produto com historico de movimentacao nao pode ser excluido. */
	boolean existsByProduto(Produto produto);

	long countByProdutoId(Long idProduto);

	List<MovimentacaoEstoque> findByProdutoIdOrderByRegistradoEmDesc(Long idProduto);

	List<MovimentacaoEstoque> findAllByOrderByRegistradoEmDesc();

}
