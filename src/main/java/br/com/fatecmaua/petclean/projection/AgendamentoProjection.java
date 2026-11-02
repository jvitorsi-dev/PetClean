package br.com.fatecmaua.petclean.projection;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalTime;

/** US-12: projection da agenda do dia. */
public interface AgendamentoProjection {

	public Long getId();

	public String getCliente();

	public String getPet();

	public String getServico();

	public LocalDate getData();

	public LocalTime getHora();

	public BigDecimal getValor();

	public String getStatus();

}
