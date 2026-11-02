package br.com.fatecmaua.petclean.control;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.fatecmaua.petclean.dto.MovimentacaoRequest;
import br.com.fatecmaua.petclean.dto.ProdutoRequest;
import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import br.com.fatecmaua.petclean.model.MovimentacaoEstoque;
import br.com.fatecmaua.petclean.model.Produto;
import br.com.fatecmaua.petclean.projection.ProdutoProjection;
import br.com.fatecmaua.petclean.service.ProdutoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;

/**
 * EP-04 - Controle de Estoque (US-18, US-19, US-20, US-21 e US-25).
 */
@RestController
@RequestMapping("/api/produtos")
@Tag(name = "04 - Estoque", description = "Produtos, movimentacoes e alerta de estoque critico (EP-04)")
public class ProdutoController {

	@Autowired
	private ProdutoService produtoService;

	@Operation(description = "US-25 - Lista e filtra produtos por nome e/ou categoria. "
			+ "Cada item traz o campo 'estoqueCritico' (US-20).", tags = "04 - Estoque")
	@GetMapping
	public List<Produto> listar(@RequestParam(name = "termo", required = false) String termo,
			@RequestParam(name = "categoria", required = false) CategoriaProdutoEnum categoria) {
		return produtoService.buscar(termo, categoria);
	}

	@Operation(description = "US-25 - Versao otimizada (SQL nativo + projection) da busca de produtos.", tags = "04 - Estoque")
	@GetMapping("/resumo")
	public List<ProdutoProjection> listarResumo(@RequestParam(name = "termo", required = false) String termo) {
		return produtoService.buscarResumo(termo);
	}

	@Operation(description = "US-20 / US-24 - Lista somente os produtos com estoque critico, "
			+ "ordenados do mais critico para o menos critico.", tags = "04 - Estoque")
	@GetMapping("/estoque-critico")
	public List<Produto> estoqueCritico() {
		return produtoService.estoqueCritico();
	}

	@Operation(description = "US-18 - Retorna um produto pelo id.", tags = "04 - Estoque")
	@GetMapping("/{id}")
	public Produto buscarPorId(@PathVariable Long id) {
		return produtoService.buscarPorId(id);
	}

	@Operation(description = "US-18 - Cadastra produto no estoque. Quantidade ou preco negativos devolvem 422.", tags = "04 - Estoque")
	@PostMapping
	public ResponseEntity<Produto> cadastrar(@RequestBody @Valid ProdutoRequest dados) {
		Produto produto = produtoService.cadastrar(dados);
		return ResponseEntity.status(HttpStatus.CREATED).body(produto);
	}

	@Operation(description = "Edita os dados do produto, registrando a diferenca de quantidade como movimentacao.", tags = "04 - Estoque")
	@PutMapping("/{id}")
	public Produto atualizar(@PathVariable Long id, @RequestBody @Valid ProdutoRequest dados) {
		return produtoService.atualizar(id, dados);
	}

	@Operation(description = "US-19 - Registra entrada ou saida de estoque. "
			+ "Saida maior que o disponivel devolve 409 com aviso.", tags = "04 - Estoque")
	@PatchMapping("/{id}/movimentar")
	public Produto movimentar(@PathVariable Long id, @RequestBody @Valid MovimentacaoRequest dados) {
		return produtoService.movimentar(id, dados);
	}

	@Operation(description = "US-21 - Inativa (ou reativa) o produto. Alternativa a exclusao "
			+ "para itens com historico de movimentacao.", tags = "04 - Estoque")
	@PatchMapping("/{id}/inativar")
	public Produto inativar(@PathVariable Long id, @RequestParam(name = "ativo", defaultValue = "false") boolean ativo) {
		return produtoService.inativar(id, ativo);
	}

	@Operation(description = "US-21 - Exclui um produto sem movimentacao. "
			+ "Produto com historico devolve 409 e a sugestao de inativar.", tags = "04 - Estoque")
	@DeleteMapping("/{id}")
	public ResponseEntity<Void> excluir(@PathVariable Long id) {
		produtoService.excluir(id);
		return ResponseEntity.noContent().build();
	}

	@Operation(description = "US-19 - Historico de movimentacoes. Com 'idProduto' filtra por produto.", tags = "04 - Estoque")
	@GetMapping("/movimentacoes")
	public List<MovimentacaoEstoque> movimentacoes(
			@RequestParam(name = "idProduto", required = false) Long idProduto) {
		return produtoService.movimentacoes(idProduto);
	}

}
