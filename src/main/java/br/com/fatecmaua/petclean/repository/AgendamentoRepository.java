package br.com.fatecmaua.petclean.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.fatecmaua.petclean.model.Agendamento;
import br.com.fatecmaua.petclean.model.StatusAgendamentoEnum;
import br.com.fatecmaua.petclean.projection.AgendamentoProjection;
import br.com.fatecmaua.petclean.projection.AgendamentosPorDiaProjection;

public interface AgendamentoRepository extends JpaRepository<Agendamento, Long> {

	/** US-12 (1): agendamentos do dia ordenados por horario. */
	List<Agendamento> findByDataOrderByHora(LocalDate data);

	/** US-12 (2): filtro por status. */
	List<Agendamento> findByStatusOrderByDataAscHoraAsc(StatusAgendamentoEnum status);

	/** US-12 (1)/(3): filtro por data e status. */
	List<Agendamento> findByDataAndStatusOrderByHora(LocalDate data, StatusAgendamentoEnum status);

	List<Agendamento> findAllByOrderByDataDescHoraDesc();

	List<Agendamento> findByPetIdOrderByDataDescHoraDesc(Long idPet);

	/** US-17: existe agendamento ativo no mesmo dia e horario? */
	@Query("select count(a) from Agendamento a where a.data = :data and a.hora = :hora "
			+ "and a.status <> 'CANCELADO' and (:idIgnorado is null or a.id <> :idIgnorado)")
	long contarConflitosNoHorario(@Param("data") LocalDate data, @Param("hora") java.time.LocalTime hora,
			@Param("idIgnorado") Long idIgnorado);

	/** US-10 (2): pet com agendamento futuro impede a exclusao. */
	@Query("select count(a) from Agendamento a where a.pet.id = :idPet "
			+ "and a.data >= :hoje and a.status <> 'CANCELADO'")
	long contarAgendamentosFuturosDoPet(@Param("idPet") Long idPet, @Param("hoje") LocalDate hoje);

	@Query("select count(a) from Agendamento a where a.cliente.id = :idCliente")
	long contarPorCliente(@Param("idCliente") Long idCliente);

	/** US-22 (1): agendamentos do mes corrente. */
	@Query("select count(a) from Agendamento a where month(a.data) = :mes and year(a.data) = :ano")
	Long contarPorMes(@Param("mes") int mes, @Param("ano") int ano);

	/** US-12 (2): status aceitos e pendentes do dia. */
	@Query("select count(a) from Agendamento a where a.data = :data and a.status in ('AGENDADO','CONFIRMADO')")
	long contarPendentesDoDia(@Param("data") LocalDate data);

	/**
	 * US-23: quantidade de agendamentos por dia dentro de um periodo. A agregacao semanal
	 * e mensal e montada no service a partir desta projection.
	 */
	@Query(nativeQuery = true, value = "select cast(a.data as varchar) dia, count(*) total "
			+ "from agendamento a where a.data between :inicio and :fim "
			+ "group by a.data order by a.data")
	List<AgendamentosPorDiaProjection> contarPorDiaNoPeriodo(@Param("inicio") LocalDate inicio,
			@Param("fim") LocalDate fim);

	/** US-12: listagem otimizada (SQL nativo) com nomes de cliente, pet e servico. */
	@Query(nativeQuery = true, value = "select a.id, c.nome cliente, p.nome pet, a.servico, "
			+ "a.data, a.hora, a.valor, a.status from agendamento a "
			+ "inner join cliente c on (a.fk_cliente = c.id) "
			+ "inner join pet p on (a.fk_pet = p.id) "
			+ "where a.data = :data order by a.hora")
	List<AgendamentoProjection> listarResumoDoDia(@Param("data") LocalDate data);

}
