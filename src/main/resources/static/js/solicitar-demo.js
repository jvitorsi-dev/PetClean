document.addEventListener("DOMContentLoaded", function () {
    const formDemo = document.getElementById("form-solicitar-demo");
    const sucessoOverlay = document.getElementById("sucesso-overlay");
    const erroOverlay = document.getElementById("erro-overlay");
    const erroMsg = document.getElementById("erro-msg");

    if (formDemo) {
        formDemo.addEventListener("submit", function (e) {
            e.preventDefault();

            const btnSubmit = this.querySelector(".botao-enviar");
            
            // Bloqueia o botão para evitar cliques duplos durante o envio do e-mail
            if (btnSubmit) {
                btnSubmit.disabled = true;
                btnSubmit.style.opacity = "0.7";
            }

            /* PENDENCIA: o projeto original enviava o formulario para
               php/solicitar-demo/processar-solicitacao.php (grava e dispara e-mail).
               A API Java nao possui endpoint equivalente, portanto nao ha envio:
               a overlay de erro original e reaproveitada com a mensagem real. */
            if (btnSubmit) {
                btnSubmit.disabled = false;
                btnSubmit.style.opacity = "1";
            }
            console.warn("Solicitar demonstração: recurso sem endpoint na API Java (pendência documentada).");
            if (erroOverlay && erroMsg) {
                erroMsg.textContent = "Não foi possível enviar a solicitação: recurso ainda não disponível na API Java (pendência documentada).";
                erroOverlay.style.display = "flex";

                setTimeout(() => {
                    erroOverlay.style.display = "none";
                }, 4000);
            }
        });
    }
});