package br.com.fatecmaua.petclean.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.fatecmaua.petclean.model.Pet;
import br.com.fatecmaua.petclean.projection.PetResumoProjection;

public interface PetRepository extends JpaRepository<Pet, Long> {

	List<Pet> findByClienteIdOrderByNome(Long idCliente);

	long countByClienteId(Long idCliente);

	/** US-11 (1): ao selecionar o cliente, somente os pets dele sao listados. */
	@Query("from Pet p where p.cliente.id = :idCliente order by p.nome")
	List<Pet> listarPorCliente(@Param("idCliente") Long idCliente);

	/** US-08 (2): filtro em tempo real por parte do nome do pet ou do tutor (HQL). */
	@Query("from Pet p where lower(p.nome) like lower(concat('%', :termo, '%')) "
			+ "or lower(p.cliente.nome) like lower(concat('%', :termo, '%')) order by p.nome")
	List<Pet> filtrarPorNomePetOuTutor(@Param("termo") String termo);

	/** US-08 (1): consulta otimizada (SQL nativo) mostrando nome do pet, especie e tutor. */
	@Query(nativeQuery = true, value = "select p.nome pet, cast(p.especie as varchar) especie, "
			+ "c.nome tutor from pet p inner join cliente c on (p.fk_cliente = c.id) "
			+ "where lower(p.nome) like lower(concat('%', :termo, '%')) "
			+ "or lower(c.nome) like lower(concat('%', :termo, '%')) order by p.nome")
	List<PetResumoProjection> filtrarResumo(@Param("termo") String termo);

	@Query("select count(p) from Pet p")
	Long totalDePets();

}
