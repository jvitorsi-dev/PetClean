package br.com.fatecmaua.petclean.dto;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

import br.com.fatecmaua.petclean.projection.ProdutoProjection;
import io.swagger.v3.oas.annotations.media.Schema;

/**
 * EP-05: resposta consolidada do dashboard.
 * US-22 (cards de KPI), US-23 (grafico por periodo) e US-24 (estoque critico).
 */
@Schema(description = "Dados do dashboard gerencial")
public record DashboardResponse(

		@Schema(description = "US-22: totais exibidos nos cards") CardsKpi cards,

		@Schema(description = "US-23: quantidade de agendamentos agrupada por periodo") GraficoAgendamentos agendamentos,

		@Schema(description = "US-24: produtos com estoque critico, do mais para o menos critico") List<ProdutoProjection> estoqueCritico,

		@Schema(description = "US-24 (2): true quando nao ha nenhum produto critico") Boolean estoqueNormal) {

	@Schema(description = "Cards de KPI do dashboard")
	public record CardsKpi(

			@Schema(description = "US-22 (1): total de clientes", example = "12") Long totalClientes,

			@Schema(description = "US-22 (1): total de pets", example = "18") Long totalPets,

			@Schema(description = "US-22 (1): agendamentos do mes corrente", example = "34") Long agendamentosDoMes,

			@Schema(description = "Agendamentos pendentes hoje") Long agendamentosHojePendentes,

			@Schema(description = "Produtos com estoque critico") Long produtosCriticos,

			@Schema(description = "Valor total do estoque (preco x quantidade)") BigDecimal valorEstoque) {
	}

	@Schema(description = "Grafico de agendamentos por periodo")
	public record GraficoAgendamentos(

			@Schema(description = "Periodo usado na agregacao: SEMANAL ou MENSAL", example = "SEMANAL") String periodo,

			@Schema(description = "Rotulos do eixo X (semanas ou meses)", example = "[\"2026-W44\", \"2026-W45\"]") List<String> rotulos,

			@Schema(description = "Valores do eixo Y na mesma ordem dos rotulos", example = "[8, 12]") List<Long> valores,

			@Schema(description = "Total de agendamentos no periodo analisado") Long total,

			@Schema(description = "Detalhamento por dia, quando solicitado") Map<String, Long> porDia) {
	}

}
