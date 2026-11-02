package br.com.fatecmaua.petclean.dto;

import br.com.fatecmaua.petclean.security.UsuarioSessao;
import io.swagger.v3.oas.annotations.media.Schema;

/** US-01 (1) e US-02 (2): dados devolvidos apos o login. */
@Schema(description = "Resposta do login: usuario autenticado e rota para onde voltar")
public record LoginResponse(

		@Schema(description = "Dados do usuario autenticado") UsuarioSessao usuario,

		@Schema(description = "Rota solicitada antes do login (US-02)", example = "/clientes") String rotaPendente,

		@Schema(description = "Mensagem de sucesso", example = "Login realizado com sucesso") String mensagem) {

}
