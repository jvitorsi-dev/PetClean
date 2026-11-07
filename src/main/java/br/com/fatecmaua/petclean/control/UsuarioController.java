package br.com.fatecmaua.petclean.control;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import br.com.fatecmaua.petclean.dto.AlterarSenhaRequest;
import br.com.fatecmaua.petclean.dto.AtualizarPerfilRequest;
import br.com.fatecmaua.petclean.dto.ErroResposta;
import br.com.fatecmaua.petclean.dto.PerfilResponse;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.security.SessaoService;
import br.com.fatecmaua.petclean.security.UsuarioSessao;
import br.com.fatecmaua.petclean.service.UsuarioService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;

/**
 * Tela de Perfil: dados do usuario autenticado, troca de senha e foto.
 * Cobre o que o PHP fazia em perfil/atualizar.php e perfil/alterar_senha.php.
 */
@RestController
@Tag(name = "07 - Perfil do Usuario", description = "Dados do perfil, troca de senha e foto do usuario")
public class UsuarioController {

	@Autowired
	private UsuarioService usuarioService;

	@Autowired
	private SessaoService sessaoService;

	/**
	 * US-25 (tela de perfil): cada usuario so altera os proprios dados.
	 * Sem sessao a API ja responde 401 pelo interceptor; aqui tratamos o id de outro usuario.
	 */
	private void exigirProprio(HttpServletRequest request, Long id) {
		UsuarioSessao atual = sessaoService.usuarioAtual(request);
		if (atual == null) {
			throw ErroNegocioException.naoAutorizado("Acesso nao autenticado.");
		}
		if (!atual.id().equals(id)) {
			throw ErroNegocioException.proibido("Voce so pode alterar o proprio perfil.");
		}
	}

	@Operation(description = "Dados do perfil do usuario informado (sem o hash da senha).", tags = "07 - Perfil do Usuario")
	@GetMapping("/api/usuarios/{id}")
	public PerfilResponse perfil(@PathVariable Long id) {
		return usuarioService.perfil(id);
	}

	@Operation(description = "Atualiza nome, e-mail, telefone, nome do pet shop e endereco. "
			+ "Atualiza tambem o usuario guardado na sessao, para o cabecalho refletir a mudanca.", tags = "07 - Perfil do Usuario", responses = {
					@ApiResponse(responseCode = "200", description = "Perfil atualizado"),
					@ApiResponse(responseCode = "400", description = "Campos invalidos", content = @Content(schema = @Schema(implementation = ErroResposta.class))),
					@ApiResponse(responseCode = "403", description = "Perfil de outro usuario", content = @Content(schema = @Schema(implementation = ErroResposta.class))),
					@ApiResponse(responseCode = "409", description = "E-mail ja usado por outro usuario", content = @Content(schema = @Schema(implementation = ErroResposta.class))) })
	@PutMapping("/api/usuarios/{id}")
	public PerfilResponse atualizar(@PathVariable Long id, @RequestBody @Valid AtualizarPerfilRequest dados,
			HttpServletRequest request) {
		exigirProprio(request, id);
		PerfilResponse perfil = usuarioService.atualizar(id, dados);
		// mantem o cabecalho das paginas coerente sem exigir novo login
		sessaoService.autenticar(request,
				new UsuarioSessao(perfil.id(), perfil.nome(), perfil.email(), perfil.perfil()));
		return perfil;
	}

	@Operation(description = "Troca a senha exigindo a senha atual. A nova senha e gravada em bcrypt.", tags = "07 - Perfil do Usuario", responses = {
			@ApiResponse(responseCode = "204", description = "Senha alterada"),
			@ApiResponse(responseCode = "422", description = "Senha atual incorreta", content = @Content(schema = @Schema(implementation = ErroResposta.class))) })
	@PutMapping("/api/usuarios/{id}/senha")
	public ResponseEntity<Void> alterarSenha(@PathVariable Long id, @RequestBody @Valid AlterarSenhaRequest dados,
			HttpServletRequest request) {
		exigirProprio(request, id);
		usuarioService.alterarSenha(id, dados);
		return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
	}

	@Operation(description = "Envia a foto de perfil (multipart, campo 'foto'). Aceita apenas imagens de ate 2 MB.", tags = "07 - Perfil do Usuario", responses = {
			@ApiResponse(responseCode = "200", description = "Foto gravada"),
			@ApiResponse(responseCode = "422", description = "Arquivo invalido", content = @Content(schema = @Schema(implementation = ErroResposta.class))) })
	@PostMapping(value = "/api/usuarios/{id}/foto", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
	public PerfilResponse enviarFoto(@PathVariable Long id, @RequestPart("foto") MultipartFile arquivo,
			HttpServletRequest request) {
		exigirProprio(request, id);
		return usuarioService.salvarFoto(id, arquivo);
	}

	@Operation(description = "Devolve a foto de perfil do usuario (usada pelo avatar de todas as paginas).", tags = "07 - Perfil do Usuario")
	@GetMapping("/api/usuarios/{id}/foto")
	public ResponseEntity<byte[]> foto(@PathVariable Long id) {
		UsuarioService.Foto foto = usuarioService.buscarFoto(id);
		return ResponseEntity.ok().contentType(MediaType.parseMediaType(foto.tipo()))
				.cacheControl(CacheControl.noStore()).body(foto.conteudo());
	}

}
