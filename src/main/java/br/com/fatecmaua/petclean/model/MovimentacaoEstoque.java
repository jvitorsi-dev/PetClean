package br.com.fatecmaua.petclean.model;

import java.time.LocalDateTime;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/**
 * Historico de entradas e saidas de estoque (US-19). Tambem e a evidencia usada em
 * US-21 para impedir a exclusao de produto com movimentacao.
 */
@Schema(description = "Esta e uma entidade que registra uma movimentacao de estoque")
@Entity
@Table(name = "movimentacao_estoque")
public class MovimentacaoEstoque {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Produto movimentado")
	@ManyToOne(optional = false)
	@JoinColumn(name = "fk_produto", nullable = false)
	private Produto produto;

	@Schema(description = "Tipo da movimentacao", example = "ENTRADA")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 20)
	private TipoMovimentacaoEnum tipo;

	@Schema(description = "Quantidade movimentada", example = "10")
	@Column(nullable = false)
	private Integer quantidade;

	@Schema(description = "Observacao da movimentacao", example = "Compra do fornecedor")
	@Column(length = 255)
	private String observacao;

	@Schema(description = "Data/hora em que a movimentacao foi registrada")
	@Column(name = "registrado_em", nullable = false)
	private LocalDateTime registradoEm;

	public MovimentacaoEstoque() {

	}

	public MovimentacaoEstoque(Long id, Produto produto, TipoMovimentacaoEnum tipo, Integer quantidade,
			String observacao) {
		this.id = id;
		this.produto = produto;
		this.tipo = tipo;
		this.quantidade = quantidade;
		this.observacao = observacao;
		this.registradoEm = LocalDateTime.now();
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Produto getProduto() {
		return produto;
	}

	public void setProduto(Produto produto) {
		this.produto = produto;
	}

	public TipoMovimentacaoEnum getTipo() {
		return tipo;
	}

	public void setTipo(TipoMovimentacaoEnum tipo) {
		this.tipo = tipo;
	}

	public Integer getQuantidade() {
		return quantidade;
	}

	public void setQuantidade(Integer quantidade) {
		this.quantidade = quantidade;
	}

	public String getObservacao() {
		return observacao;
	}

	public void setObservacao(String observacao) {
		this.observacao = observacao;
	}

	public LocalDateTime getRegistradoEm() {
		return registradoEm;
	}

	public void setRegistradoEm(LocalDateTime registradoEm) {
		this.registradoEm = registradoEm;
	}

}
