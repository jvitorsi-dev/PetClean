package br.com.fatecmaua.petclean.control;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.dto.DashboardResponse;
import br.com.fatecmaua.petclean.model.Produto;
import br.com.fatecmaua.petclean.service.DashboardService;
import br.com.fatecmaua.petclean.service.ProdutoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

/**
 * EP-05 - Dashboards Analiticos (US-22, US-23 e US-24).
 */
@RestController
@RequestMapping("/api/dashboard")
@Tag(name = "05 - Dashboard", description = "KPIs e graficos gerenciais (EP-05)")
public class DashboardController {

	@Autowired
	private DashboardService dashboardService;

	@Autowired
	private ProdutoService produtoService;

	@Operation(description = "US-22 - Cards de KPI (total de clientes, total de pets, agendamentos do mes). "
			+ "US-23 - Grafico de agendamentos por periodo: 'semanal' (padrao) ou 'mensal'. "
			+ "US-24 - Lista de produtos com estoque critico e o indicador 'estoqueNormal'.", tags = "05 - Dashboard")
	@GetMapping
	public DashboardResponse dashboard(
			@RequestParam(name = "periodo", required = false, defaultValue = "semanal") String periodo,
			@RequestParam(name = "referencia", required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate referencia) {
		return dashboardService.gerar(periodo, referencia);
	}

	@Operation(description = "US-24 - Somente o grafico de estoque critico, "
			+ "ordenado do mais critico para o menos critico.", tags = "05 - Dashboard")
	@GetMapping("/estoque-critico")
	public List<Produto> estoqueCritico() {
		return produtoService.estoqueCritico();
	}

}
