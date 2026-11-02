package br.com.fatecmaua.petclean.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

/**
 * Tutor do pet. Entidade central do EP-01 (Gerenciamento de Clientes).
 */
@Schema(description = "Esta e uma entidade que representa um cliente (tutor) do pet shop")
@Entity
@Table(name = "cliente")
public class Cliente {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Nome completo do tutor", example = "Maria da Silva")
	@Column(nullable = false, length = 120)
	private String nome;

	/**
	 * US-15 (RNF: unicidade): o CPF e gravado somente com digitos e nao pode repetir.
	 */
	@Schema(description = "CPF do tutor, somente digitos (11 caracteres)", example = "12345678901")
	@Column(nullable = false, unique = true, length = 11)
	private String cpf;

	@Schema(description = "Telefone de contato", example = "(11) 98765-4321")
	@Column(nullable = false, length = 20)
	private String telefone;

	@Schema(description = "E-mail de contato", example = "maria@email.com")
	@Column(nullable = false, length = 120)
	private String email;

	@Schema(description = "Endereco completo", example = "Rua das Flores, 100 - Santo Andre/SP")
	@Column(nullable = false, length = 200)
	private String endereco;

	/** US-03/US-06: um cliente possui varios pets (integridade referencial no delete). */
	@JsonIgnore
	@OneToMany(mappedBy = "cliente")
	private List<Pet> pets = new ArrayList<>();

	@JsonIgnore
	@OneToMany(mappedBy = "cliente")
	private List<Agendamento> agendamentos = new ArrayList<>();

	public Cliente() {

	}

	public Cliente(Long id, String nome, String cpf, String telefone, String email, String endereco) {
		this.id = id;
		this.nome = nome;
		this.cpf = cpf;
		this.telefone = telefone;
		this.email = email;
		this.endereco = endereco;
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

	public String getCpf() {
		return cpf;
	}

	public void setCpf(String cpf) {
		this.cpf = cpf;
	}

	public String getTelefone() {
		return telefone;
	}

	public void setTelefone(String telefone) {
		this.telefone = telefone;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public String getEndereco() {
		return endereco;
	}

	public void setEndereco(String endereco) {
		this.endereco = endereco;
	}

	public List<Pet> getPets() {
		return pets;
	}

	public void setPets(List<Pet> pets) {
		this.pets = pets;
	}

	public List<Agendamento> getAgendamentos() {
		return agendamentos;
	}

	public void setAgendamentos(List<Agendamento> agendamentos) {
		this.agendamentos = agendamentos;
	}

}
