package br.com.fatecmaua.petclean.model;

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
 * Usuario do sistema. EP-06 (Autenticacao e Acesso): US-01, US-02, US-14.
 * RNF-04: a senha nunca e gravada em texto puro, e sim em hash bcrypt.
 */
@Schema(description = "Esta e uma entidade que representa um usuario do sistema")
@Entity
@Table(name = "usuario")
public class Usuario {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Nome do usuario", example = "Helen Aclina")
	@Column(nullable = false, length = 120)
	private String nome;

	/** US-01: o login e feito por e-mail. */
	@Schema(description = "E-mail usado como login (unico)", example = "helen@petclean.com")
	@Column(nullable = false, unique = true, length = 120)
	private String email;

	/** RNF-04: hash bcrypt da senha (nunca exposto nas respostas). */
	@Schema(description = "Hash bcrypt da senha", example = "$2a$10$...")
	@Column(name = "senha_hash", nullable = false, length = 100)
	private String senhaHash;

	@Schema(description = "Perfil de acesso", example = "ATENDENTE")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 20)
	private PerfilEnum perfil;

	public Usuario() {

	}

	public Usuario(Long id, String nome, String email, String senhaHash, PerfilEnum perfil) {
		this.id = id;
		this.nome = nome;
		this.email = email;
		this.senhaHash = senhaHash;
		this.perfil = perfil;
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

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getSenhaHash() {
		return senhaHash;
	}

	public void setSenhaHash(String senhaHash) {
		this.senhaHash = senhaHash;
	}

	public PerfilEnum getPerfil() {
		return perfil;
	}

	public void setPerfil(PerfilEnum perfil) {
		this.perfil = perfil;
	}

}
