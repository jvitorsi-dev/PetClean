package br.com.fatecmaua.petclean.service;

/**
 * US-15 (3): o CPF e validado antes de salvar, tanto o formato quanto os digitos
 * verificadores. O valor e sempre normalizado para 11 digitos (sem pontuacao), o que
 * garante a unicidade no banco.
 */
public final class ValidacaoCpf {

	private ValidacaoCpf() {
	}

	public static String normalizar(String cpf) {
		return cpf == null ? null : cpf.replaceAll("\\D", "");
	}

	public static boolean isValido(String cpf) {
		String numeros = normalizar(cpf);
		if (numeros == null || numeros.length() != 11) {
			return false;
		}
		// rejeita sequencias repetidas (000.000.000-00, 111.111.111-11, ...)
		if (numeros.chars().distinct().count() == 1) {
			return false;
		}
		return digitoVerificador(numeros, 9) == Character.getNumericValue(numeros.charAt(9))
				&& digitoVerificador(numeros, 10) == Character.getNumericValue(numeros.charAt(10));
	}

	private static int digitoVerificador(String numeros, int posicao) {
		int soma = 0;
		for (int i = 0; i < posicao; i++) {
			soma += Character.getNumericValue(numeros.charAt(i)) * (posicao + 1 - i);
		}
		int resto = soma % 11;
		return resto < 2 ? 0 : 11 - resto;
	}

	/** Formata para exibicao: 12345678901 -> 123.456.789-01. */
	public static String formatar(String cpf) {
		String numeros = normalizar(cpf);
		if (numeros == null || numeros.length() != 11) {
			return cpf;
		}
		return numeros.substring(0, 3) + "." + numeros.substring(3, 6) + "." + numeros.substring(6, 9) + "-"
				+ numeros.substring(9);
	}

}
