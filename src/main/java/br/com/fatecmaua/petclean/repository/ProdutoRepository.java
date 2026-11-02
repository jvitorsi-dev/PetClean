package br.com.fatecmaua.petclean.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import br.com.fatecmaua.petclean.model.Produto;
import br.com.fatecmaua.petclean.projection.ProdutoProjection;

public interface ProdutoRepository extends JpaRepository<Produto, Long> {

	List<Produto> findAllByOrderByNomeAsc();

	List<Produto> findByCategoriaOrderByNomeAsc(CategoriaProdutoEnum categoria);

	/** US-25 (1): busca por parte do nome (HQL). */
	@Query("from Produto p where lower(p.nome) like lower(concat('%', :termo, '%')) order by p.nome")
	List<Produto> buscarPorNome(@Param("termo") String termo);

	/** US-25 (2): filtro combinado de nome e categoria. */
	@Query("from Produto p where lower(p.nome) like lower(concat('%', :termo, '%')) "
			+ "and p.categoria = :categoria order by p.nome")
	List<Produto> buscarPorNomeECategoria(@Param("termo") String termo,
			@Param("categoria") CategoriaProdutoEnum categoria);

	/**
	 * US-20 (1) e US-24 (1): produtos com quantidade igual ou abaixo do minimo,
	 * ordenados do mais critico (maior falta) para o menos critico.
	 */
	@Query("from Produto p where p.quantidade <= p.estoqueMinimo "
			+ "order by (p.estoqueMinimo - p.quantidade) desc, p.nome")
	List<Produto> listarEstoqueCritico();

	/** US-20 / US-24: estoque critico em consulta nativa, ja ordenado do mais critico ao menos critico. */
	@Query(nativeQuery = true, value = "select p.nome, cast(p.categoria as varchar) categoria, "
			+ "p.quantidade, p.estoque_minimo, p.preco from produto p "
			+ "where p.quantidade <= p.estoque_minimo "
			+ "order by (p.estoque_minimo - p.quantidade) desc, p.nome")
	List<ProdutoProjection> listarResumoEstoqueCritico();

	/** US-25 (3): consulta otimizada (SQL nativo) com projection. */
	@Query(nativeQuery = true, value = "select p.nome, cast(p.categoria as varchar) categoria, "
			+ "p.quantidade, p.estoque_minimo, p.preco from produto p "
			+ "where lower(p.nome) like lower(concat('%', :termo, '%')) order by p.nome")
	List<ProdutoProjection> buscarResumo(@Param("termo") String termo);

	@Query("select coalesce(sum(p.preco * p.quantidade), 0) from Produto p")
	Double valorTotalDoEstoque();

}
