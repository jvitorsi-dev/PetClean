package br.com.fatecmaua.petclean.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.fatecmaua.petclean.dto.LoginRequest;
import br.com.fatecmaua.petclean.exception.ErroNegocioException;
import br.com.fatecmaua.petclean.model.Usuario;
import br.com.fatecmaua.petclean.repository.UsuarioRepository;
import br.com.fatecmaua.petclean.security.UsuarioSessao;

/**
 * EP-06 (Autenticacao e Acesso): US-01 (login com e-mail e senha, senha em bcrypt - RNF-04).
 */
@Service
public class AutenticacaoService {

	/** RNF-04: as senhas sao armazenadas e conferidas com bcrypt. */
	private final BCryptPasswordEncoder codificador = new BCryptPasswordEncoder();

	@Autowired
	private UsuarioRepository repU;

	/**
	 * US-01 (1) credenciais validas => usuario de sessao; (2) senha incorreta =>
	 * "credenciais invalidas".
	 */
	@Transactional(readOnly = true)
	public UsuarioSessao autenticar(LoginRequest dados) {
		Usuario usuario = repU.findByEmailIgnoreCase(dados.email().trim())
				.orElseThrow(() -> ErroNegocioException.naoAutorizado("Credenciais invalidas."));

		if (!codificador.matches(dados.senha(), usuario.getSenhaHash())) {
			throw ErroNegocioException.naoAutorizado("Credenciais invalidas.");
		}

		return new UsuarioSessao(usuario.getId(), usuario.getNome(), usuario.getEmail(), usuario.getPerfil());
	}

	/** Utilitario usado na carga inicial e em testes: gera o hash bcrypt da senha. */
	public String gerarHash(String senhaPura) {
		return codificador.encode(senhaPura);
	}

	public boolean confere(String senhaPura, String hash) {
		return codificador.matches(senhaPura, hash);
	}

}
