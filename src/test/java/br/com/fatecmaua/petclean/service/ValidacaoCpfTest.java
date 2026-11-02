package br.com.fatecmaua.petclean.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** US-15 (3): o CPF precisa ser validado antes de salvar. */
class ValidacaoCpfTest {

	@Test
	@DisplayName("CPF valido com e sem pontuacao e aceito")
	void aceitaCpfValido() {
		assertTrue(ValidacaoCpf.isValido("123.456.789-09"));
		assertTrue(ValidacaoCpf.isValido("12345678909"));
	}

	@Test
	@DisplayName("CPF com digito verificador errado e recusado")
	void recusaDigitoInvalido() {
		assertFalse(ValidacaoCpf.isValido("123.456.789-00"));
	}

	@Test
	@DisplayName("CPF com sequencia repetida e recusado")
	void recusaSequenciaRepetida() {
		assertFalse(ValidacaoCpf.isValido("111.111.111-11"));
	}

	@Test
	@DisplayName("CPF com quantidade errada de digitos e recusado")
	void recusaTamanhoInvalido() {
		assertFalse(ValidacaoCpf.isValido("123.456.789"));
		assertFalse(ValidacaoCpf.isValido(null));
	}

	@Test
	@DisplayName("Normalizacao remove a pontuacao e a formatacao devolve a mascara")
	void normalizaEFormata() {
		assertEquals("12345678909", ValidacaoCpf.normalizar("123.456.789-09"));
		assertEquals("123.456.789-09", ValidacaoCpf.formatar("12345678909"));
	}

}
