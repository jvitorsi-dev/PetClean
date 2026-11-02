package br.com.fatecmaua.petclean.projection;

import java.math.BigDecimal;

/** US-25: projection do estoque. */
public interface ProdutoProjection {

	public String getNome();

	public String getCategoria();

	public Integer getQuantidade();

	public Integer getEstoqueMinimo();

	public BigDecimal getPreco();

}
