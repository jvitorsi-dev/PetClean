package br.com.fatecmaua.petclean.model;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

/**
 * Animal atendido, sempre vinculado a um tutor. EP-02 (Gerenciamento de Pets).
 */
@Schema(description = "Esta e uma entidade que representa um pet vinculado a um cliente")
@Entity
@Table(name = "pet")
public class Pet {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Schema(description = "Tutor responsavel pelo pet (obrigatorio)", example = "Maria da Silva")
	@ManyToOne(optional = false)
	@JoinColumn(name = "fk_cliente", nullable = false)
	private Cliente cliente;

	@Schema(description = "Nome do pet", example = "Thor")
	@Column(nullable = false, length = 80)
	private String nome;

	@Schema(description = "Especie do pet", example = "CACHORRO")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 20)
	private EspecieEnum especie;

	@Schema(description = "Raca do pet", example = "Golden Retriever")
	@Column(nullable = false, length = 80)
	private String raca;

	@Schema(description = "Porte do pet", example = "GRANDE")
	@Enumerated(EnumType.STRING)
	@Column(nullable = false, length = 20)
	private PorteEnum porte;

	/** US-07 (3): idade invalida (texto/negativa) e barrada na validacao do DTO. */
	@Schema(description = "Idade do pet em anos", example = "4")
	@Column(nullable = false)
	private Integer idade;

	@JsonIgnore
	@OneToMany(mappedBy = "pet")
	private List<Agendamento> agendamentos = new ArrayList<>();

	public Pet() {

	}

	public Pet(Long id, Cliente cliente, String nome, EspecieEnum especie, String raca, PorteEnum porte,
			Integer idade) {
		this.id = id;
		this.cliente = cliente;
		this.nome = nome;
		this.especie = especie;
		this.raca = raca;
		this.porte = porte;
		this.idade = idade;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public EspecieEnum getEspecie() {
		return especie;
	}

	public void setEspecie(EspecieEnum especie) {
		this.especie = especie;
	}

	public String getRaca() {
		return raca;
	}

	public void setRaca(String raca) {
		this.raca = raca;
	}

	public PorteEnum getPorte() {
		return porte;
	}

	public void setPorte(PorteEnum porte) {
		this.porte = porte;
	}

	public Integer getIdade() {
		return idade;
	}

	public void setIdade(Integer idade) {
		this.idade = idade;
	}

	public List<Agendamento> getAgendamentos() {
		return agendamentos;
	}

	public void setAgendamentos(List<Agendamento> agendamentos) {
		this.agendamentos = agendamentos;
	}

}
