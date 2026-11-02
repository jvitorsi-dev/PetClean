package br.com.fatecmaua.petclean.projection;

/** US-23: quantidade de agendamentos agrupada por dia. */
public interface AgendamentosPorDiaProjection {

	public String getDia();

	public Long getTotal();

}
