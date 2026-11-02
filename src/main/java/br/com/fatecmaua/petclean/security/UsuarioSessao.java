package br.com.fatecmaua.petclean.security;

import java.io.Serializable;

import br.com.fatecmaua.petclean.model.PerfilEnum;
import io.swagger.v3.oas.annotations.media.Schema;

/**
 * Dados do usuario autenticado guardados na HttpSession (US-01).
 * A senha/hash nunca e colocada na sessao.
 */
@Schema(description = "Usuario autenticado na sessao atual")
public record UsuarioSessao(Long id, String nome, String email, PerfilEnum perfil) implements Serializable {

	private static final long serialVersionUID = 1L;

}
