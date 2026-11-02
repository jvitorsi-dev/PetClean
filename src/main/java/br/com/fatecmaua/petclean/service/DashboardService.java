package br.com.fatecmaua.petclean.service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.temporal.WeekFields;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.DashboardResponse;
import br.com.fatecmaua.petclean.projection.AgendamentosPorDiaProjection;
import br.com.fatecmaua.petclean.projection.ProdutoProjection;
import br.com.fatecmaua.petclean.repository.AgendamentoRepository;
import br.com.fatecmaua.petclean.repository.ClienteRepository;
import br.com.fatecmaua.petclean.repository.PetRepository;
import br.com.fatecmaua.petclean.repository.ProdutoRepository;

/**
 * Regras do EP-05 (Dashboards Analiticos):
 * US-22 (cards de KPI), US-23 (grafico de agendamentos por periodo)
 * e US-24 (grafico de estoque critico).
 */
@Service
public class DashboardService {

	@Autowired
	private ClienteRepository repC;

	@Autowired
	private PetRepository repP;

	@Autowired
	private AgendamentoRepository repA;

	@Autowired
	private ProdutoRepository repProd;

	/**
	 * @param periodo   "SEMANAL" (padrao) ou "MENSAL"
	 * @param referencia data de referencia do periodo analisado
	 */
	@Transactional(readOnly = true)
	public DashboardResponse gerar(String periodo, LocalDate referencia) {
		LocalDate hoje = LocalDate.now();
		LocalDate dataRef = referencia == null ? hoje : referencia;
		String periodoNormalizado = normalizarPeriodo(periodo);

		Long totalClientes = repC.totalDeClientes();
		Long totalPets = repP.totalDePets();
		Long agendamentosDoMes = repA.contarPorMes(dataRef.getMonthValue(), dataRef.getYear());
		Long pendentesHoje = repA.contarPendentesDoDia(hoje);

		// US-24 (1): produtos criticos vem do banco ja ordenados do mais critico para o menos critico
		List<ProdutoProjection> criticos = repProd.listarResumoEstoqueCritico();

		Double valorEstoque = repProd.valorTotalDoEstoque();

		DashboardResponse.CardsKpi cards = new DashboardResponse.CardsKpi(
				totalClientes == null ? 0L : totalClientes,
				totalPets == null ? 0L : totalPets,
				agendamentosDoMes == null ? 0L : agendamentosDoMes,
				pendentesHoje,
				(long) criticos.size(),
				valorEstoque == null ? BigDecimal.ZERO : BigDecimal.valueOf(valorEstoque));

		DashboardResponse.GraficoAgendamentos grafico = montarGrafico(periodoNormalizado, dataRef);

		return new DashboardResponse(cards, grafico, criticos, criticos.isEmpty());
	}

	/**
	 * US-23: agrega a contagem de agendamentos por semana ou por mes.
	 * (3) periodos sem agendamento aparecem zerados, sem erro.
	 */
	private DashboardResponse.GraficoAgendamentos montarGrafico(String periodo, LocalDate referencia) {
		if ("MENSAL".equals(periodo)) {
			return montarGraficoMensal(referencia);
		}
		return montarGraficoSemanal(referencia);
	}

	private DashboardResponse.GraficoAgendamentos montarGraficoSemanal(LocalDate referencia) {
		LocalDate inicio = referencia.minusWeeks(7).with(java.time.DayOfWeek.MONDAY);
		LocalDate fim = referencia.with(java.time.DayOfWeek.SUNDAY);

		Map<String, Long> porDia = agruparPorDia(inicio, fim);
		WeekFields semana = WeekFields.ISO;

		// inicializa as 8 semanas com zero para garantir o eixo mesmo sem dados
		Map<String, Long> porSemana = new LinkedHashMap<>();
		for (int i = 0; i < 8; i++) {
			LocalDate dia = inicio.plusWeeks(i);
			porSemana.put(rotuloSemana(dia, semana), 0L);
		}

		porDia.forEach((dia, total) -> {
			LocalDate data = LocalDate.parse(dia);
			String rotulo = rotuloSemana(data, semana);
			porSemana.merge(rotulo, total, Long::sum);
		});

		return new DashboardResponse.GraficoAgendamentos("SEMANAL", new ArrayList<>(porSemana.keySet()),
				new ArrayList<>(porSemana.values()), somar(porSemana), porDia);
	}

	private DashboardResponse.GraficoAgendamentos montarGraficoMensal(LocalDate referencia) {
		YearMonth inicio = YearMonth.from(referencia).minusMonths(5);
		YearMonth fim = YearMonth.from(referencia);

		Map<String, Long> porDia = agruparPorDia(inicio.atDay(1), fim.atEndOfMonth());

		Map<String, Long> porMes = new LinkedHashMap<>();
		for (int i = 0; i < 6; i++) {
			YearMonth mes = inicio.plusMonths(i);
			porMes.put(rotuloMes(mes), 0L);
		}

		porDia.forEach((dia, total) -> porMes.merge(rotuloMes(YearMonth.from(LocalDate.parse(dia))), total, Long::sum));

		return new DashboardResponse.GraficoAgendamentos("MENSAL", new ArrayList<>(porMes.keySet()),
				new ArrayList<>(porMes.values()), somar(porMes), porDia);
	}

	/** US-23: consulta agregada no banco, agrupada por dia. */
	private Map<String, Long> agruparPorDia(LocalDate inicio, LocalDate fim) {
		Map<String, Long> porDia = new TreeMap<>();
		List<AgendamentosPorDiaProjection> linhas = repA.contarPorDiaNoPeriodo(inicio, fim);
		for (AgendamentosPorDiaProjection linha : linhas) {
			porDia.put(linha.getDia(), linha.getTotal());
		}
		return porDia;
	}

	private String rotuloSemana(LocalDate dia, WeekFields semana) {
		return dia.getYear() + "-S" + String.format("%02d", dia.get(semana.weekOfWeekBasedYear()));
	}

	private String rotuloMes(YearMonth mes) {
		return mes.getYear() + "-" + String.format("%02d", mes.getMonthValue());
	}

	private Long somar(Map<String, Long> valores) {
		return valores.values().stream().mapToLong(Long::longValue).sum();
	}

	private String normalizarPeriodo(String periodo) {
		if (periodo == null || periodo.isBlank()) {
			return "SEMANAL";
		}
		String valor = periodo.trim().toUpperCase();
		return valor.startsWith("MEN") ? "MENSAL" : "SEMANAL";
	}

}
