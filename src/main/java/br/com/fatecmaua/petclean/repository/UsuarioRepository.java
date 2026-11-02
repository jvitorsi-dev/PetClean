package br.com.fatecmaua.petclean.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import br.com.fatecmaua.petclean.model.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {

	/** US-01 (1): autenticacao por e-mail e senha. */
	Optional<Usuario> findByEmailIgnoreCase(String email);

	boolean existsByEmailIgnoreCase(String email);

}
