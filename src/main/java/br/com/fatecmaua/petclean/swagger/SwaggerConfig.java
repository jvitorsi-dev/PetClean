package br.com.fatecmaua.petclean.swagger;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;

/**
 * Documentacao da API PetClean.
 * O esquema de seguranca documenta a sessao por cookie usada no login (US-01/US-02).
 */
@Configuration
public class SwaggerConfig {

	@Bean
	OpenAPI configurarSwagger() {

		final String nomeEsquema = "sessaoPetClean";

		return new OpenAPI()
				.info(new Info()
						.title("PetClean - API de Gestao para Pet Shops")
						.description("API REST do projeto PetClean, construida a partir dos 6 epicos e das 25 "
								+ "historias de usuario do relatorio de Gestao Agil (Kanban + XP). "
								+ "Cobre clientes, pets, agendamentos, estoque, dashboards e autenticacao. "
								+ "Para testar rotas protegidas: execute POST /login (email e senha) e o cookie "
								+ "de sessao sera reutilizado pelo Swagger UI.")
						.version("1.0"))
				.addSecurityItem(new SecurityRequirement().addList(nomeEsquema))
				.components(new Components().addSecuritySchemes(nomeEsquema, new SecurityScheme()
						.name("PETCLEANSESSION")
						.type(SecurityScheme.Type.APIKEY)
						.in(SecurityScheme.In.COOKIE)
						.description("Cookie de sessao criado por POST /login")));
	}

}
