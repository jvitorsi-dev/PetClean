package br.com.fatecmaua.petclean.model;

import java.math.BigDecimal;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * Produto do estoque. EP-04 (Controle de Estoque): US-18, US-20, US-21, US-25.
 */
@Schema(description = "Esta e uma entidade que representa um produto do estoque")
@Entity
@Table(name = "produto")
public class Produto {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Nome do produto", example = "Racao Premium Adulto 10kg")
	@Column(nullable = false, length = 120)
	private String nome;

	@Schema(description = "Categoria do produto", example = "RACAO")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 30)
	private CategoriaProdutoEnum categoria;

	@Schema(description = "Quantidade disponivel em estoque", example = "12")
	@Column(nullable = false)
	private Integer quantidade;

	/** US-18 (3): o estoque minimo alimenta o alerta de estoque critico (US-20). */
	@Schema(description = "Nivel minimo que dispara o alerta de estoque critico", example = "5")
	@Column(name = "estoque_minimo", nullable = false)
	private Integer estoqueMinimo;

	/** US-18 (2): quantidade ou preco negativos devem ser bloqueados. */
	@Schema(description = "Preco unitario de venda", example = "189.90")
	@Column(nullable = false, precision = 10, scale = 2)
	private BigDecimal preco;

	/** US-21 (2): produto com movimentacao nao pode ser excluido, apenas inativado. */
	@Schema(description = "Indica se o produto esta ativo para venda", example = "true")
	@Column(nullable = false)
	private Boolean ativo = Boolean.TRUE;

	public Produto() {

	}

	public Produto(Long id, String nome, CategoriaProdutoEnum categoria, Integer quantidade, Integer estoqueMinimo,
			BigDecimal preco, Boolean ativo) {
		this.id = id;
		this.nome = nome;
		this.categoria = categoria;
		this.quantidade = quantidade;
		this.estoqueMinimo = estoqueMinimo;
		this.preco = preco;
		this.ativo = ativo;
	}

	/**
	 * US-20 (1): critico quando a quantidade e igual ou inferior ao estoque minimo.
	 */
	public boolean isEstoqueCritico() {
		if (quantidade == null || estoqueMinimo == null) {
			return false;
		}
		return quantidade <= estoqueMinimo;
	}

	/** Diferenca para o estoque minimo: usada para ordenar do mais critico ao menos critico (US-24). */
	public Integer getFaltamParaMinimo() {
		if (quantidade == null || estoqueMinimo == null) {
			return 0;
		}
		return Math.max(0, estoqueMinimo - quantidade);
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public CategoriaProdutoEnum getCategoria() {
		return categoria;
	}

	public void setCategoria(CategoriaProdutoEnum categoria) {
		this.categoria = categoria;
	}

	public Integer getQuantidade() {
		return quantidade;
	}

	public void setQuantidade(Integer quantidade) {
		this.quantidade = quantidade;
	}

	public Integer getEstoqueMinimo() {
		return estoqueMinimo;
	}

	public void setEstoqueMinimo(Integer estoqueMinimo) {
		this.estoqueMinimo = estoqueMinimo;
	}

	public BigDecimal getPreco() {
		return preco;
	}

	public void setPreco(BigDecimal preco) {
		this.preco = preco;
	}

	public Boolean getAtivo() {
		return ativo;
	}

	public void setAtivo(Boolean ativo) {
		this.ativo = ativo;
	}

}
