package br.com.fatecmaua.petclean.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.projection.ClienteResumoProjection;

public interface ClienteRepository extends JpaRepository<Cliente, Long> {

	/** US-01: busca o usuario pelo e-mail informado no login. */
	Optional<Cliente> findByCpf(String cpf);

	boolean existsByCpf(String cpf);

	/** US-15 (3): usado para impedir CPF duplicado na edicao (ignora o proprio registro). */
	boolean existsByCpfAndIdNot(String cpf, Long id);

	/** US-04 (2): filtro por parte do nome ou do CPF (HQL). */
	@Query("from Cliente c where lower(c.nome) like lower(concat('%', :termo, '%')) "
			+ "or c.cpf like concat('%', :termo, '%') order by c.nome")
	List<Cliente> filtrarPorNomeOuCpf(@Param("termo") String termo);

	/** US-04 (1)/(2): consulta otimizada (SQL nativo) com projection. */
	@Query(nativeQuery = true, value = "select c.nome, c.cpf, c.telefone from cliente c "
			+ "where lower(c.nome) like lower(concat('%', :termo, '%')) "
			+ "or c.cpf like concat('%', :termo, '%') order by c.nome")
	List<ClienteResumoProjection> filtrarResumo(@Param("termo") String termo);

	@Query("select count(c) from Cliente c")
	Long totalDeClientes();

}
