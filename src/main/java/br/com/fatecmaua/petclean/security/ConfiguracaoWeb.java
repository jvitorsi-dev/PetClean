package br.com.fatecmaua.petclean.security;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Registro das regras de acesso (US-02) e permissao de CORS para um eventual
 * front-end separado. Rotas publicas: login, logout, Swagger/OpenAPI, console do H2
 * e a raiz da API.
 */
@Configuration
public class ConfiguracaoWeb implements WebMvcConfigurer {

	@Autowired
	private InterceptorSeguranca interceptorSeguranca;

	/** Rotas que nao exigem sessao autenticada. */
	/**
	 * Rotas que nao exigem sessao autenticada.
	 * Atencao: os padroes de documentacao precisam cobrir os SUB-CAMINHOS acessados
	 * pelo Swagger UI (/api-docs/swagger-config, /api-docs.yaml, /webjars/...), caso
	 * contrario a interface carrega e falha com "Failed to load resource: 401".
	 */
	private static final List<String> ROTAS_PUBLICAS = List.of(
			// autenticacao
			"/login", "/logout",
			// portal e paginas
			"/", "/index.html", "/favicon.ico", "/error",
			// Swagger / OpenAPI (UI, JSON, YAML, config e assets webjars)
			"/api-docs", "/api-docs/**", "/api-docs.yaml", "/v3/api-docs", "/v3/api-docs/**",
			"/swagger-resources/**",
			"/swagger-ui/**", "/swagger-ui.html", "/webjars/**",
			// console do banco
			"/h2-console/**");

	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(interceptorSeguranca).addPathPatterns("/**").excludePathPatterns(ROTAS_PUBLICAS);
	}

	@Override
	public void addCorsMappings(CorsRegistry registry) {
		registry.addMapping("/**")
				.allowedOriginPatterns("*")
				.allowedMethods("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
				.allowedHeaders("*")
				.allowCredentials(true);
	}

}
