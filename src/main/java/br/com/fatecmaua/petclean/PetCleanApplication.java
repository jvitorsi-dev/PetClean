package br.com.fatecmaua.petclean;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@EnableJpaRepositories(basePackages = "br.com.fatecmaua.petclean.repository")
@ComponentScan(basePackages = "br.com.fatecmaua.petclean")
@EntityScan(basePackages = "br.com.fatecmaua.petclean.model")
@SpringBootApplication
public class PetCleanApplication {

	public static void main(String[] args) {
		SpringApplication.run(PetCleanApplication.class, args);
	}

}
