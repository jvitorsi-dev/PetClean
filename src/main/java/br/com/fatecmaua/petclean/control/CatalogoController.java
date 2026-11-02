package br.com.fatecmaua.petclean.control;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import br.com.fatecmaua.petclean.model.EspecieEnum;
import br.com.fatecmaua.petclean.model.PorteEnum;
import br.com.fatecmaua.petclean.model.ServicoEnum;
import br.com.fatecmaua.petclean.model.StatusAgendamentoEnum;
import br.com.fatecmaua.petclean.model.TipoMovimentacaoEnum;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

/**
 * Apoio ao front-end: devolve os dominios usados nos formularios.
 * US-11 (2): permite exibir valor e duracao de cada servico antes de agendar.
 */
@RestController
@RequestMapping("/api/catalogos")
@Tag(name = "07 - Catalogos", description = "Dominios e listas de apoio para os formularios")
public class CatalogoController {

	@Operation(description = "Servicos disponiveis com valor e duracao (US-11, criterio 2).", tags = "07 - Catalogos")
	@GetMapping("/servicos")
	public List<ServicoInfo> servicos() {
		return java.util.Arrays.stream(ServicoEnum.values())
				.map(s -> new ServicoInfo(s.name(), s.getDescricao(), s.getValor(), s.getDuracaoMinutos())).toList();
	}

	@Operation(description = "Especies de pets aceitas no cadastro.", tags = "07 - Catalogos")
	@GetMapping("/especies")
	public EspecieEnum[] especies() {
		return EspecieEnum.values();
	}

	@Operation(description = "Portes de pets aceitos no cadastro.", tags = "07 - Catalogos")
	@GetMapping("/portes")
	public PorteEnum[] portes() {
		return PorteEnum.values();
	}

	@Operation(description = "Status possiveis de um agendamento.", tags = "07 - Catalogos")
	@GetMapping("/status-agendamento")
	public StatusAgendamentoEnum[] statusAgendamento() {
		return StatusAgendamentoEnum.values();
	}

	@Operation(description = "Categorias de produto do estoque.", tags = "07 - Catalogos")
	@GetMapping("/categorias-produto")
	public CategoriaProdutoEnum[] categoriasProduto() {
		return CategoriaProdutoEnum.values();
	}

	@Operation(description = "Tipos de movimentacao de estoque.", tags = "07 - Catalogos")
	@GetMapping("/tipos-movimentacao")
	public TipoMovimentacaoEnum[] tiposMovimentacao() {
		return TipoMovimentacaoEnum.values();
	}

	/** DTO simples de servico, com valor e duracao. */
	public record ServicoInfo(String codigo, String descricao, java.math.BigDecimal valor, Integer duracaoMinutos) {
	}

}
