package br.com.fatecmaua.petclean.control;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDate;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

/**
 * Testes de aceitacao dos criterios Dado/Quando/Entao das historias.
 * Cobrem EP-01, EP-03, EP-04 e EP-06.
 */
@SpringBootTest
@AutoConfigureMockMvc
class ApiPetCleanIntegrationTest {

	/**
	 * Datas dos testes de agendamento sao calculadas a partir de hoje: a API recusa
	 * data passada (422), portanto literais fixos quebravam o teste com o tempo.
	 */
	private static final String DATA_FUTURA = LocalDate.now().plusDays(7).toString();

	@Autowired
	private MockMvc mockMvc;

	private MockHttpSession sessao;

	@BeforeEach
	void autenticar() throws Exception {
		MvcResult resultado = mockMvc
				.perform(post("/login").contentType(MediaType.APPLICATION_JSON)
						.content("{\"email\":\"helen@petclean.com\",\"senha\":\"petclean123\"}"))
				.andExpect(status().isOk()).andReturn();
		sessao = (MockHttpSession) resultado.getRequest().getSession(false);
	}

	// -----------------------------------------------------------------
	// EP-06 - Autenticacao e Acesso
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-01 (2): senha incorreta devolve 401 'Credenciais invalidas'")
	void loginComSenhaIncorreta() throws Exception {
		mockMvc.perform(post("/login").contentType(MediaType.APPLICATION_JSON)
				.content("{\"email\":\"helen@petclean.com\",\"senha\":\"senha-errada\"}"))
				.andExpect(status().isUnauthorized())
				.andExpect(jsonPath("$.mensagem").value("Credenciais invalidas."));
	}

	@Test
	@DisplayName("US-02 (1): rota interna sem sessao devolve 401 para a API")
	void rotaProtegidaSemSessao() throws Exception {
		mockMvc.perform(get("/api/clientes").accept(MediaType.APPLICATION_JSON))
				.andExpect(status().isUnauthorized());
	}

	@Test
	@DisplayName("US-02 (1): navegacao sem sessao e redirecionada para /login")
	void navegacaoSemSessaoRedireciona() throws Exception {
		mockMvc.perform(get("/api/clientes").accept(MediaType.TEXT_HTML))
				.andExpect(status().is3xxRedirection())
				.andExpect(redirectedUrl("/login"));
	}

	@Test
	@DisplayName("US-14: apos o logout a sessao deixa de valer")
	void logoutInvalidaSessao() throws Exception {
		mockMvc.perform(post("/logout").session(sessao)).andExpect(status().isNoContent());
		mockMvc.perform(get("/api/clientes").session(sessao).accept(MediaType.APPLICATION_JSON))
				.andExpect(status().isUnauthorized());
	}

	@Test
	@DisplayName("Documentacao: /api-docs e os recursos do Swagger sao publicos, mas /api/** continua protegido")
	void documentacaoPublicaSemSessao() throws Exception {
		mockMvc.perform(get("/api-docs")).andExpect(status().isOk());
		mockMvc.perform(get("/api-docs/swagger-config")).andExpect(status().isOk());
		mockMvc.perform(get("/swagger-ui/index.html")).andExpect(status().isOk());
		// a protecao das rotas internas permanece valendo
		mockMvc.perform(get("/api/clientes").accept(MediaType.APPLICATION_JSON)).andExpect(status().isUnauthorized());
	}

	// -----------------------------------------------------------------
	// EP-01 - Clientes
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-15 (1): CPF duplicado e bloqueado com 409")
	void cpfDuplicadoBloqueado() throws Exception {
		mockMvc.perform(post("/api/clientes").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"Outra Maria\",\"cpf\":\"123.456.789-09\",\"telefone\":\"(11) 90000-0000\","
						+ "\"email\":\"outra@email.com\",\"endereco\":\"Rua X, 1\"}"))
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.mensagem").value(org.hamcrest.Matchers.containsString("CPF ja cadastrado")));
	}

	@Test
	@DisplayName("US-03 (3): campo obrigatorio vazio devolve 400 com detalhe")
	void campoObrigatorioVazio() throws Exception {
		mockMvc.perform(post("/api/clientes").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"\",\"cpf\":\"987.654.321-00\",\"telefone\":\"(11) 90000-0000\","
						+ "\"email\":\"teste@email.com\",\"endereco\":\"Rua X, 1\"}"))
				.andExpect(status().isBadRequest()).andExpect(jsonPath("$.detalhes[0]").exists());
	}

	@Test
	@DisplayName("US-06 (2): cliente com vinculos nao pode ser excluido (RNF-09)")
	void exclusaoBloqueadaPorIntegridadeReferencial() throws Exception {
		mockMvc.perform(delete("/api/clientes/1").session(sessao)).andExpect(status().isConflict());
	}

	@Test
	@DisplayName("US-04 (2): filtro por nome retorna apenas clientes correspondentes")
	void filtroDeClientes() throws Exception {
		mockMvc.perform(get("/api/clientes").param("termo", "Maria").session(sessao))
				.andExpect(status().isOk()).andExpect(jsonPath("$[0].nome").value("Maria da Silva"));
	}

	// -----------------------------------------------------------------
	// EP-02 - Pets
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-07 (1): pet sem tutor selecionado nao e salvo")
	void petSemTutor() throws Exception {
		mockMvc.perform(post("/api/pets").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"Sem Tutor\",\"especie\":\"GATO\",\"raca\":\"SRD\",\"porte\":\"MEDIO\",\"idade\":2}"))
				.andExpect(status().isBadRequest());
	}

	@Test
	@DisplayName("US-07 (3): idade negativa e recusada")
	void idadeNegativa() throws Exception {
		mockMvc.perform(post("/api/pets").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"idCliente\":1,\"nome\":\"Teste\",\"especie\":\"GATO\",\"raca\":\"SRD\","
						+ "\"porte\":\"MEDIO\",\"idade\":-1}"))
				.andExpect(status().isBadRequest());
	}

	@Test
	@DisplayName("US-08 (2): filtro por tutor encontra os pets dele")
	void filtroDePets() throws Exception {
		mockMvc.perform(get("/api/pets").param("termo", "Maria").session(sessao)).andExpect(status().isOk())
				.andExpect(jsonPath("$.length()").value(2));
	}

	// -----------------------------------------------------------------
	// EP-03 - Agendamentos
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-17 (1): horario ja ocupado impede novo agendamento")
	void conflitoDeHorario() throws Exception {
		mockMvc.perform(post("/api/agendamentos").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"idCliente\":1,\"idPet\":1,\"servico\":\"BANHO\",\"data\":\"" + DATA_FUTURA + "\",\"hora\":\"09:00\"}"))
				.andExpect(status().isCreated());

		mockMvc.perform(post("/api/agendamentos").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"idCliente\":1,\"idPet\":2,\"servico\":\"TOSA\",\"data\":\"" + DATA_FUTURA + "\",\"hora\":\"09:00\"}"))
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.mensagem").value(org.hamcrest.Matchers.containsString("Ja existe um agendamento")));
	}

	@Test
	@DisplayName("US-11 (1): pet de outro tutor e recusado")
	void petDeOutroTutor() throws Exception {
		mockMvc.perform(post("/api/agendamentos").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"idCliente\":1,\"idPet\":3,\"servico\":\"BANHO\",\"data\":\"" + DATA_FUTURA + "\",\"hora\":\"08:00\"}"))
				.andExpect(status().isUnprocessableEntity());
	}

	@Test
	@DisplayName("US-13 (3): atualizacao de status registra a data/hora")
	void atualizaStatusRegistrandoDataHora() throws Exception {
		MvcResult criado = mockMvc
				.perform(post("/api/agendamentos").session(sessao).contentType(MediaType.APPLICATION_JSON)
						.content("{\"idCliente\":2,\"idPet\":3,\"servico\":\"BANHO\",\"data\":\"" + DATA_FUTURA + "\",\"hora\":\"10:00\"}"))
				.andExpect(status().isCreated()).andReturn();
		String corpo = criado.getResponse().getContentAsString();
		String id = corpo.replaceAll(".*\"id\":(\\d+).*", "$1");

		mockMvc.perform(patch("/api/agendamentos/" + id + "/status").session(sessao)
				.contentType(MediaType.APPLICATION_JSON).content("{\"status\":\"CONFIRMADO\"}"))
				.andExpect(status().isOk()).andExpect(jsonPath("$.status").value("CONFIRMADO"))
				.andExpect(jsonPath("$.atualizadoEm").isNotEmpty());
	}

	@Test
	@DisplayName("US-16 (3): agendamento realizado nao pode ser cancelado")
	void naoCancelaRealizado() throws Exception {
		mockMvc.perform(patch("/api/agendamentos/1/cancelar").session(sessao)).andExpect(status().isConflict());
	}

	// -----------------------------------------------------------------
	// EP-04 - Estoque
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-19 (2): saida maior que o disponivel e impedida")
	void saidaMaiorQueDisponivel() throws Exception {
		mockMvc.perform(patch("/api/produtos/1/movimentar").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"tipo\":\"SAIDA\",\"quantidade\":9999}"))
				.andExpect(status().isConflict());
	}

	@Test
	@DisplayName("US-18 (2): preco negativo e bloqueado")
	void precoNegativo() throws Exception {
		mockMvc.perform(post("/api/produtos").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"Teste\",\"categoria\":\"OUTRO\",\"quantidade\":1,\"estoqueMinimo\":1,\"preco\":-10}"))
				.andExpect(status().isBadRequest());
	}

	@Test
	@DisplayName("US-20 / US-24 (1): estoque critico vem ordenado do mais critico ao menos critico")
	void estoqueCriticoOrdenado() throws Exception {
		mockMvc.perform(get("/api/produtos/estoque-critico").session(sessao)).andExpect(status().isOk())
				// ordenacao pela maior falta em relacao ao minimo: Antipulgas (2/6) > Vermifugo (0/3) > Condicionador (1/4)
				.andExpect(jsonPath("$[0].nome").value("Antipulgas Comprimido"))
				.andExpect(jsonPath("$[0].estoqueCritico").value(true));
	}

	@Test
	@DisplayName("US-21 (2): produto com movimentacao nao pode ser excluido")
	void exclusaoDeProdutoComHistorico() throws Exception {
		mockMvc.perform(delete("/api/produtos/1").session(sessao)).andExpect(status().isConflict());
	}

	// -----------------------------------------------------------------
	// EP-05 - Dashboard
	// -----------------------------------------------------------------

	@Test
	@DisplayName("US-22 / US-23 (3): dashboard devolve os 3 cards e o grafico semanal zerado quando vazio")
	void dashboardCompleto() throws Exception {
		mockMvc.perform(get("/api/dashboard").param("periodo", "semanal").session(sessao)).andExpect(status().isOk())
				.andExpect(jsonPath("$.cards.totalClientes").isNumber())
				.andExpect(jsonPath("$.cards.totalPets").isNumber())
				.andExpect(jsonPath("$.cards.agendamentosDoMes").isNumber())
				.andExpect(jsonPath("$.agendamentos.rotulos.length()").value(8))
				.andExpect(jsonPath("$.agendamentos.valores.length()").value(8))
				.andExpect(jsonPath("$.estoqueNormal").value(false));
	}

	@Test
	@DisplayName("US-23 (2): alternar para mensal altera o eixo do grafico")
	void dashboardMensal() throws Exception {
		mockMvc.perform(get("/api/dashboard").param("periodo", "mensal").session(sessao)).andExpect(status().isOk())
				.andExpect(jsonPath("$.agendamentos.periodo").value("MENSAL"))
				.andExpect(jsonPath("$.agendamentos.rotulos.length()").value(6));
	}

	// -----------------------------------------------------------------
	// Tela de Perfil (dados, senha e foto)
	// -----------------------------------------------------------------

	@Test
	@DisplayName("Perfil: GET devolve os dados do usuario autenticado, sem o hash da senha")
	void perfilDoUsuarioAutenticado() throws Exception {
		mockMvc.perform(get("/api/usuarios/1").session(sessao).accept(MediaType.APPLICATION_JSON))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.nome").value("Helen Vitoria Silva Aclina"))
				.andExpect(jsonPath("$.email").value("helen@petclean.com"))
				.andExpect(jsonPath("$.perfil").value("ATENDENTE"))
				.andExpect(jsonPath("$.senhaHash").doesNotExist());
	}

	@Test
	@DisplayName("Perfil: PUT grava telefone, nome do pet shop e endereco")
	void atualizarPerfil() throws Exception {
		mockMvc.perform(put("/api/usuarios/1").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"Helen Vitoria Silva Aclina\",\"email\":\"helen@petclean.com\","
						+ "\"telefone\":\"(11) 91234-5678\",\"nomePetshop\":\"PetClean Central\","
						+ "\"endereco\":\"Rua das Flores, 123 - Santo Andre/SP\"}"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.telefone").value("(11) 91234-5678"))
				.andExpect(jsonPath("$.nomePetshop").value("PetClean Central"));
	}

	@Test
	@DisplayName("Perfil: alterar o perfil de outro usuario devolve 403")
	void naoAlteraPerfilDeOutroUsuario() throws Exception {
		mockMvc.perform(put("/api/usuarios/2").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"nome\":\"Outro Nome\",\"email\":\"gabriel@petclean.com\"}"))
				.andExpect(status().isForbidden());
	}

	@Test
	@DisplayName("Perfil: alterar senha com a senha atual errada devolve 422")
	void alterarSenhaComSenhaAtualErrada() throws Exception {
		mockMvc.perform(put("/api/usuarios/1/senha").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"senhaAtual\":\"senha-errada\",\"novaSenha\":\"outraSenha123\"}"))
				.andExpect(status().isUnprocessableEntity())
				.andExpect(jsonPath("$.mensagem").value("Senha atual incorreta."));
	}

	@Test
	@DisplayName("Perfil: trocar a senha e devolver para a original mantem o login funcionando")
	void trocarSenhaEVoltar() throws Exception {
		mockMvc.perform(put("/api/usuarios/1/senha").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"senhaAtual\":\"petclean123\",\"novaSenha\":\"temporaria123\"}"))
				.andExpect(status().isNoContent());
		mockMvc.perform(put("/api/usuarios/1/senha").session(sessao).contentType(MediaType.APPLICATION_JSON)
				.content("{\"senhaAtual\":\"temporaria123\",\"novaSenha\":\"petclean123\"}"))
				.andExpect(status().isNoContent());
	}

	@Test
	@DisplayName("Perfil: upload de foto grava a imagem e o avatar do cabecalho passa a existir")
	void enviarFoto() throws Exception {
		MockMultipartFile arquivo = new MockMultipartFile("foto", "avatar.png", "image/png",
				new byte[] { (byte) 0x89, 'P', 'N', 'G' });
		mockMvc.perform(multipart("/api/usuarios/1/foto").file(arquivo).session(sessao))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.temFoto").value(true));
		mockMvc.perform(get("/api/usuarios/1/foto").session(sessao)).andExpect(status().isOk());
	}

}
