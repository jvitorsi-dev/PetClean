/*
 * Central de comunicacao com a API Java (Spring Boot).
 * Substitui as chamadas fetch("../php/....php") do projeto original.
 * Mantem o mesmo formato de retorno que os scripts originais esperam:
 *   { status: "sucesso" | "erro", mensagem: "..." }
 * para que alert(), confirm() e window.location.reload() continuem identicos.
 */
window.PetCleanApi = (function () {
    const BASE = "/api";

    async function requisitar(caminho, metodo, corpo) {
        const opcoes = {
            method: metodo || "GET",
            credentials: "same-origin",
            headers: { "Accept": "application/json" }
        };
        if (corpo !== undefined && corpo !== null) {
            opcoes.headers["Content-Type"] = "application/json";
            opcoes.body = JSON.stringify(corpo);
        }

        const resposta = await fetch(BASE + caminho, opcoes);

        // Sessao expirada: a API responde 401 (o PHP redirecionava sozinho).
        if (resposta.status === 401) {
            window.location.href = "/paginas/login.html";
            return { ok: false, status: 401, dados: null };
        }

        let dados = null;
        try {
            dados = await resposta.json();
        } catch (e) {
            dados = null;
        }
        return { ok: resposta.ok, status: resposta.status, dados: dados };
    }

    /** Extrai a mensagem de erro do ErroResposta {status, erro, mensagem, detalhes}. */
    function mensagem(resultado, padrao) {
        const dados = resultado ? resultado.dados : null;
        if (!dados) return padrao;
        const partes = [];
        if (dados.mensagem) partes.push(dados.mensagem);
        if (Array.isArray(dados.detalhes)) {
            partes.push(dados.detalhes.join(" "));
        } else if (typeof dados.detalhes === "string" && dados.detalhes) {
            partes.push(dados.detalhes);
        }
        return partes.length ? partes.join(" ") : padrao;
    }

    /** Envelope compativel com data.status / data.mensagem usados nos scripts originais. */
    function envelope(resultado, mensagemSucesso, mensagemErro) {
        if (resultado && resultado.ok) {
            return { status: "sucesso", mensagem: mensagemSucesso, dados: resultado.dados };
        }
        return { status: "erro", mensagem: mensagem(resultado, mensagemErro), dados: null };
    }

    return {
        requisitar: requisitar,
        mensagem: mensagem,
        envelope: envelope,
        get: (caminho) => requisitar(caminho, "GET"),
        post: (caminho, corpo) => requisitar(caminho, "POST", corpo),
        put: (caminho, corpo) => requisitar(caminho, "PUT", corpo),
        patch: (caminho, corpo) => requisitar(caminho, "PATCH", corpo),
        del: (caminho) => requisitar(caminho, "DELETE"),
        /** Registra no console a pendencia de um recurso que a API Java ainda nao possui. */
        pendente: function (recurso) {
            console.warn(recurso + ": recurso sem endpoint equivalente na API Java (pendencia documentada).");
        }
    };
})();
