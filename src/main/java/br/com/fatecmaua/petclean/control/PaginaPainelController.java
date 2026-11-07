package br.com.fatecmaua.petclean.control;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.fasterxml.jackson.databind.ObjectMapper;

import br.com.fatecmaua.petclean.model.Agendamento;
import br.com.fatecmaua.petclean.model.CategoriaProdutoEnum;
import br.com.fatecmaua.petclean.model.Cliente;
import br.com.fatecmaua.petclean.model.EspecieEnum;
import br.com.fatecmaua.petclean.model.Pet;
import br.com.fatecmaua.petclean.model.PorteEnum;
import br.com.fatecmaua.petclean.model.Produto;
import br.com.fatecmaua.petclean.model.ServicoEnum;
import br.com.fatecmaua.petclean.model.Usuario;
import br.com.fatecmaua.petclean.security.SessaoService;
import br.com.fatecmaua.petclean.security.UsuarioSessao;
import br.com.fatecmaua.petclean.service.AgendamentoService;
import br.com.fatecmaua.petclean.service.ClienteService;
import br.com.fatecmaua.petclean.service.PetService;
import br.com.fatecmaua.petclean.service.ProdutoService;
import br.com.fatecmaua.petclean.service.UsuarioService;
import jakarta.servlet.http.HttpServletRequest;

/**
 * Paginas do painel (antigas paginas/*.php). A renderizacao continua no servidor,
 * como no projeto PHP: o HTML enviado ao navegador e o mesmo, mudando apenas a
 * origem dos dados (services Java no lugar das consultas PDO).
 */
@Controller
@RequestMapping("/paginas")
public class PaginaPainelController {

	private static final DateTimeFormatter DIA_MES = DateTimeFormatter.ofPattern("dd/MM");
	private static final DateTimeFormatter DIA_MES_ANO = DateTimeFormatter.ofPattern("dd/MM/yyyy");
	private static final java.util.Map<String, String> SERVICOS_LABEL = java.util.Map.of(
			"BANHO", "Banho", "TOSA", "Tosa", "BANHO_E_TOSA", "Banho e Tosa",
			"HIDRATACAO", "Hidratação", "CONSULTA_VETERINARIA", "Consulta");
	private static final java.util.Map<String, String> PORTES_LABEL = java.util.Map.of(
			"PEQUENO", "Pequeno", "MEDIO", "Médio", "GRANDE", "Grande");
	private static final java.util.Map<String, String> CATEGORIAS_LABEL = java.util.Map.of(
			"RACAO", "Ração", "MEDICAMENTO", "Medicamento", "HIGIENE", "Higiene",
			"BRINQUEDO", "Brinquedo", "ACESSORIO", "Acessório", "OUTRO", "Outro");

	private static final String[] MESES = { "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out",
			"Nov", "Dez" };

	@Autowired
	private SessaoService sessaoService;
	@Autowired
	private ClienteService clienteService;
	@Autowired
	private PetService petService;
	@Autowired
	private AgendamentoService agendamentoService;
	@Autowired
	private ProdutoService produtoService;
	@Autowired
	private ObjectMapper objectMapper;
	@Autowired
	private UsuarioService usuarioService;

	// =====================================================================
	// Cabecalho comum (nome, e-mail, cargo e avatar do usuario logado)
	// =====================================================================
	private void cabecalho(Model model, HttpServletRequest request) {
		UsuarioSessao usuario = sessaoService.usuarioAtual(request);
		String nome = usuario != null ? usuario.nome() : "Usuário";
		model.addAttribute("nomeUsuario", nome);
		model.addAttribute("emailUsuario", usuario != null ? usuario.email() : "");
		model.addAttribute("cargoUsuario", cargo(usuario));
		model.addAttribute("inicialAvatar", nome.isEmpty() ? "" : nome.substring(0, 1).toUpperCase(new Locale("pt", "BR")));
		// rotulos com a mesma grafia do banco original (o enum da API e sem acento)
		model.addAttribute("servicosLabel", SERVICOS_LABEL);
		model.addAttribute("categoriasLabel", CATEGORIAS_LABEL);
		model.addAttribute("portesLabel", PORTES_LABEL);
		// avatar: quando o usuario tem foto, todas as paginas passam a exibir a imagem
		// (/api/usuarios/{id}/foto); sem foto, cai na inicial, como no PHP.
		String fotoPerfil = null;
		if (usuario != null && usuarioService.temFoto(usuario.id())) {
			fotoPerfil = "/api/usuarios/" + usuario.id() + "/foto";
		}
		model.addAttribute("fotoPerfil", fotoPerfil);
	}

	private String cargo(UsuarioSessao usuario) {
		if (usuario == null || usuario.perfil() == null) {
			return "Usuário";
		}
		return usuario.perfil().getDescricao();
	}

	// =====================================================================
	// 1. Dashboard
	// =====================================================================
	@GetMapping("/dashboard.html")
	public String dashboard(HttpServletRequest request, Model model) {
		cabecalho(model, request);

		LocalDate hoje = LocalDate.now();
		List<Agendamento> todos = agendamentoService.listar(null, null);

		long totalClientes = clienteService.listar().size();
		long totalPets = petService.listar().size();
		long agendamentosHoje = todos.stream().filter(a -> hoje.equals(a.getData())).count();

		// faturamento acumulado (o PHP estimava por tabela fixa de precos; aqui usa o
		// valor real gravado em cada agendamento)
		BigDecimal faturamento = todos.stream().map(Agendamento::getValor).filter(v -> v != null)
				.reduce(BigDecimal.ZERO, BigDecimal::add);

		model.addAttribute("totalClientes", totalClientes);
		model.addAttribute("totalPets", totalPets);
		model.addAttribute("totalAgendamentosHoje", agendamentosHoje);
		model.addAttribute("faturamentoValor", faturamento);

		// grafico de barras: ultimos 7 dias
		List<String> labelsDias = new ArrayList<>();
		List<Long> agendamentosDias = new ArrayList<>();
		for (int i = 6; i >= 0; i--) {
			LocalDate dia = hoje.minusDays(i);
			labelsDias.add(dia.format(DIA_MES));
			agendamentosDias.add(todos.stream().filter(a -> dia.equals(a.getData())).count());
		}
		model.addAttribute("labelsDias", labelsDias);
		model.addAttribute("agendamentosDias", agendamentosDias);

		// grafico de linha: faturamento dos ultimos 6 meses
		List<String> labelsMeses = new ArrayList<>();
		List<BigDecimal> faturamentoMeses = new ArrayList<>();
		for (int i = 5; i >= 0; i--) {
			LocalDate mes = hoje.minusMonths(i);
			labelsMeses.add(MESES[mes.getMonthValue() - 1]);
			BigDecimal soma = todos.stream()
					.filter(a -> a.getData() != null && a.getData().getYear() == mes.getYear()
							&& a.getData().getMonthValue() == mes.getMonthValue())
					.map(Agendamento::getValor).filter(v -> v != null)
					.reduce(BigDecimal.ZERO, BigDecimal::add);
			faturamentoMeses.add(soma);
		}
		model.addAttribute("labelsMeses", labelsMeses);
		model.addAttribute("faturamentoMeses", faturamentoMeses);

		// grafico de pizza: as 4 fatias do projeto original
		List<Long> pizzaDados = List.of(
				contarServico(todos, ServicoEnum.BANHO),
				contarServico(todos, ServicoEnum.TOSA),
				contarServico(todos, ServicoEnum.BANHO_E_TOSA),
				contarServico(todos, ServicoEnum.CONSULTA_VETERINARIA));
		model.addAttribute("pizzaDados", pizzaDados);

		// graficos: os arrays vao serializados em atributos data-* (sem th:inline="javascript")
		try {
			model.addAttribute("labelsDiasJson", objectMapper.writeValueAsString(labelsDias));
			model.addAttribute("agendamentosDiasJson", objectMapper.writeValueAsString(agendamentosDias));
			model.addAttribute("labelsMesesJson", objectMapper.writeValueAsString(labelsMeses));
			model.addAttribute("faturamentoMesesJson", objectMapper.writeValueAsString(faturamentoMeses));
			model.addAttribute("pizzaDadosJson", objectMapper.writeValueAsString(pizzaDados));
		} catch (com.fasterxml.jackson.core.JsonProcessingException e) {
			throw new IllegalStateException("Falha ao serializar os dados dos graficos", e);
		}

		// agendamentos de hoje (no maximo 4, por horario)
		List<Agendamento> proximos = todos.stream().filter(a -> hoje.equals(a.getData()))
				.sorted((a, b) -> a.getHora().compareTo(b.getHora())).limit(4).toList();
		model.addAttribute("proximos", proximos);
		return "paginas/dashboard";
	}

	private long contarServico(List<Agendamento> lista, ServicoEnum servico) {
		return lista.stream().filter(a -> servico.equals(a.getServico())).count();
	}

	// =====================================================================
	// 2. Relatorios
	// =====================================================================
	@GetMapping("/relatorios.html")
	public String relatorios(@RequestParam(name = "busca", required = false) String busca,
			HttpServletRequest request, Model model) {
		cabecalho(model, request);
		model.addAttribute("busca", busca == null ? "" : busca);

		long totalTutores = clienteService.listar().size();
		long totalPets = petService.listar().size();
		long totalAgendamentos = agendamentoService.listar(null, null).size();

		model.addAttribute("totalTutores", totalTutores);
		model.addAttribute("totalPets", totalPets);
		model.addAttribute("totalAgendamentos", totalAgendamentos);
		model.addAttribute("mediaPetTutor", totalTutores > 0
				? String.format(Locale.US, "%.1f", (double) totalPets / totalTutores)
				: "0.0");
		return "paginas/relatorios";
	}

	// =====================================================================
	// 3. Clientes
	// =====================================================================
	@GetMapping("/clientes.html")
	public String clientes(@RequestParam(name = "busca", required = false) String busca,
			HttpServletRequest request, Model model) {
		cabecalho(model, request);
		model.addAttribute("busca", busca == null ? "" : busca);

		List<Cliente> lista = clienteService.listar();
		if (busca != null && !busca.isBlank()) {
			String termo = busca.trim().toLowerCase(new Locale("pt", "BR"));
			lista = lista.stream().filter(c -> contem(c.getNome(), termo) || contem(c.getEmail(), termo)
					|| contem(c.getTelefone(), termo)).toList();
		}
		model.addAttribute("clientes", lista);
		return "paginas/clientes";
	}

	// =====================================================================
	// 4. Pets
	// =====================================================================
	@GetMapping("/pets.html")
	public String pets(@RequestParam(name = "busca", required = false) String busca,
			HttpServletRequest request, Model model) {
		cabecalho(model, request);
		model.addAttribute("busca", busca == null ? "" : busca);

		List<Pet> lista = petService.listar();
		if (busca != null && !busca.isBlank()) {
			String termo = busca.trim().toLowerCase(new Locale("pt", "BR"));
			lista = lista.stream().filter(p -> contem(p.getNome(), termo) || contem(p.getRaca(), termo)
					|| (p.getCliente() != null && contem(p.getCliente().getNome(), termo))).toList();
		}
		model.addAttribute("pets", lista);
		model.addAttribute("clientes", clienteService.listar());
		// catalogos usados no modal de cadastro (especie e porte sao obrigatorios na API)
		model.addAttribute("especies", EspecieEnum.values());
		model.addAttribute("portes", PorteEnum.values());
		model.addAttribute("portesLabel", PORTES_LABEL);
		return "paginas/pets";
	}

	// =====================================================================
	// 5. Estoque
	// =====================================================================
	@GetMapping("/estoque.html")
	public String estoque(@RequestParam(name = "busca", required = false) String busca,
			HttpServletRequest request, Model model) {
		cabecalho(model, request);
		model.addAttribute("busca", busca == null ? "" : busca);

		List<Produto> lista = produtoService.listar();
		if (busca != null && !busca.isBlank()) {
			String termo = busca.trim().toLowerCase(new Locale("pt", "BR"));
			lista = lista.stream().filter(p -> contem(p.getNome(), termo)
					|| (p.getCategoria() != null && (contem(p.getCategoria().name(), termo)
							|| contem(p.getCategoria().getDescricao(), termo)))).toList();
		}
		model.addAttribute("produtos", lista);
		// a categoria e um enum na API: o campo do modal e uma lista fixa de opcoes
		model.addAttribute("categorias", CategoriaProdutoEnum.values());
		return "paginas/estoque";
	}

	// =====================================================================
	// 6. Agendamentos
	// =====================================================================
	@GetMapping("/agendamentos.html")
	public String agendamentos(@RequestParam(name = "busca", required = false) String busca,
			HttpServletRequest request, Model model) {
		cabecalho(model, request);
		model.addAttribute("busca", busca == null ? "" : busca);

		List<Agendamento> lista = agendamentoService.listar(null, null);
		if (busca != null && !busca.isBlank()) {
			String termo = busca.trim().toLowerCase(new Locale("pt", "BR"));
			lista = lista.stream().filter(a -> (a.getPet() != null && contem(a.getPet().getNome(), termo))
					|| (a.getCliente() != null && contem(a.getCliente().getNome(), termo))
					|| (a.getServico() != null && (contem(a.getServico().name(), termo)
							|| contem(a.getServico().getDescricao(), termo)))).toList();
		}
		model.addAttribute("agendamentos", lista);
		model.addAttribute("pets", petService.listar());
		return "paginas/agendamentos";
	}

	// =====================================================================
	// 7. Perfil
	// =====================================================================
	@GetMapping("/perfil.html")
	public String perfil(HttpServletRequest request, Model model) {
		cabecalho(model, request);

		// dados do perfil gravados no usuario (tela de Perfil: salvar e alterar senha)
		UsuarioSessao sessao = sessaoService.usuarioAtual(request);
		if (sessao != null) {
			Usuario conta = usuarioService.buscar(sessao.id());
			model.addAttribute("usuarioId", conta.getId());
			model.addAttribute("telefone", conta.getTelefone());
			model.addAttribute("nomePetshop", conta.getNomePetshop());
			model.addAttribute("endereco", conta.getEndereco());
			model.addAttribute("dataAlteracaoSenha",
					conta.getDataAlteracaoSenha() == null ? "" : conta.getDataAlteracaoSenha().format(DIA_MES_ANO));
		} else {
			model.addAttribute("usuarioId", null);
			model.addAttribute("telefone", null);
			model.addAttribute("nomePetshop", null);
			model.addAttribute("endereco", null);
			model.addAttribute("dataAlteracaoSenha", "");
		}
		model.addAttribute("diasMembro", 0);
		return "paginas/perfil";
	}

	// =====================================================================
	// 8. Configuracoes
	// =====================================================================
	@GetMapping("/configuracoes.html")
	public String configuracoes(HttpServletRequest request, Model model) {
		cabecalho(model, request);
		return "paginas/configuracoes";
	}

	private boolean contem(String valor, String termo) {
		return valor != null && valor.toLowerCase(new Locale("pt", "BR")).contains(termo);
	}
}
