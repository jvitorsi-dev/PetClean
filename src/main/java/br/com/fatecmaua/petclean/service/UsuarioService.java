package br.com.fatecmaua.petclean.service;

import java.io.IOException;
import java.time.LocalDate;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import br.com.fatecmaua.petclean.dto.AlterarSenhaRequest;
import br.com.fatecmaua.petclean.dto.AtualizarPerfilRequest;
import br.com.fatecmaua.petclean.dto.PerfilResponse;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.Usuario;
import br.com.fatecmaua.petclean.repository.UsuarioRepository;

/**
 * Tela de Perfil: dados do usuario autenticado, troca de senha e foto.
 * Substitui perfil/atualizar.php, perfil/alterar_senha.php e o upload de avatar do PHP.
 */
@Service
public class UsuarioService {

	/** Avatar: limite proprio de 2 MB (o formulario original nao limitava). */
	private static final long TAMANHO_MAXIMO_FOTO = 2L * 1024 * 1024;

	@Autowired
	private UsuarioRepository repU;

	@Autowired
	private AutenticacaoService autenticacaoService;

	@Transactional(readOnly = true)
	public Usuario buscar(Long id) {
		return repU.findById(id).orElseThrow(() -> ErroNegocioException.naoEncontrado("Usuario nao encontrado."));
	}

	@Transactional(readOnly = true)
	public PerfilResponse perfil(Long id) {
		Usuario usuario = buscar(id);
		return PerfilResponse.de(usuario, usuario.getFoto() != null);
	}

	/** Perfil -> "Salvar": nome, e-mail, telefone, pet shop e endereco. */
	@Transactional
	public PerfilResponse atualizar(Long id, AtualizarPerfilRequest dados) {
		Usuario usuario = buscar(id);
		String email = dados.email().trim();

		if (!email.equalsIgnoreCase(usuario.getEmail()) && repU.existsByEmailIgnoreCase(email)) {
			throw ErroNegocioException.conflito("Ja existe um usuario com o e-mail " + email + ".");
		}

		usuario.setNome(dados.nome().trim());
		usuario.setEmail(email);
		usuario.setTelefone(vazioParaNulo(dados.telefone()));
		usuario.setNomePetshop(vazioParaNulo(dados.nomePetshop()));
		usuario.setEndereco(vazioParaNulo(dados.endereco()));

		Usuario salvo = repU.save(usuario);
		return PerfilResponse.de(salvo, salvo.getFoto() != null);
	}

	/** Perfil -> "Alterar senha": exige a senha atual, como no PHP (RNF-04, bcrypt). */
	@Transactional
	public void alterarSenha(Long id, AlterarSenhaRequest dados) {
		Usuario usuario = buscar(id);

		if (!autenticacaoService.confere(dados.senhaAtual(), usuario.getSenhaHash())) {
			throw ErroNegocioException.dadosInvalidos("Senha atual incorreta.");
		}
		if (dados.senhaAtual().equals(dados.novaSenha())) {
			throw ErroNegocioException.dadosInvalidos("A nova senha deve ser diferente da senha atual.");
		}

		usuario.setSenhaHash(autenticacaoService.gerarHash(dados.novaSenha()));
		usuario.setDataAlteracaoSenha(LocalDate.now());
		repU.save(usuario);
	}

	/** Perfil -> botao da camera: grava a imagem no proprio banco. */
	@Transactional
	public PerfilResponse salvarFoto(Long id, MultipartFile arquivo) {
		Usuario usuario = buscar(id);

		if (arquivo == null || arquivo.isEmpty()) {
			throw ErroNegocioException.dadosInvalidos("Selecione uma imagem para enviar.");
		}
		if (arquivo.getSize() > TAMANHO_MAXIMO_FOTO) {
			throw ErroNegocioException.dadosInvalidos("A imagem deve ter no maximo 2 MB.");
		}
		String tipo = arquivo.getContentType() == null ? "" : arquivo.getContentType().toLowerCase();
		if (!tipo.startsWith("image/")) {
			throw ErroNegocioException.dadosInvalidos("O arquivo enviado precisa ser uma imagem.");
		}

		byte[] conteudo;
		try {
			conteudo = arquivo.getBytes();
		} catch (IOException e) {
			throw ErroNegocioException.dadosInvalidos("Nao foi possivel ler a imagem enviada.");
		}

		usuario.setFoto(conteudo);
		usuario.setFotoContentType(tipo);
		Usuario salvo = repU.save(usuario);
		return PerfilResponse.de(salvo, true);
	}

	@Transactional(readOnly = true)
	public boolean temFoto(Long id) {
		return id != null && repU.existsByIdAndFotoIsNotNull(id);
	}

	/** Bytes + content-type da foto, para GET /api/usuarios/{id}/foto. */
	public record Foto(byte[] conteudo, String tipo) {
	}

	@Transactional(readOnly = true)
	public Foto buscarFoto(Long id) {
		Usuario usuario = buscar(id);
		if (usuario.getFoto() == null || usuario.getFoto().length == 0) {
			throw ErroNegocioException.naoEncontrado("Este usuario nao possui foto de perfil.");
		}
		String tipo = usuario.getFotoContentType() == null ? "image/png" : usuario.getFotoContentType();
		return new Foto(usuario.getFoto(), tipo);
	}

	private String vazioParaNulo(String valor) {
		if (valor == null) {
			return null;
		}
		String limpo = valor.trim();
		return limpo.isEmpty() ? null : limpo;
	}

}
