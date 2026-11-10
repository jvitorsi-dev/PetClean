package br.com.fatecmaua.petclean.dto;

import java.time.LocalDate;

import br.com.fatecmaua.petclean.model.PerfilEnum;
import br.com.fatecmaua.petclean.model.Usuario;
import io.swagger.v3.oas.annotations.media.Schema;

/** Resposta da tela de perfil. Nunca expoe o hash da senha. */
@Schema(description = "Dados do perfil do usuario autenticado")
public record PerfilResponse(Long id, String nome, String email, String telefone, String nomePetshop,
		String endereco, PerfilEnum perfil, boolean temFoto, LocalDate dataAlteracaoSenha) {

	public static PerfilResponse de(Usuario usuario, boolean temFoto) {
		return new PerfilResponse(usuario.getId(), usuario.getNome(), usuario.getEmail(), usuario.getTelefone(),
				usuario.getNomePetshop(), usuario.getEndereco(), usuario.getPerfil(), temFoto,
				usuario.getDataAlteracaoSenha());
	}

}
