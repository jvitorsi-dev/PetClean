document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".login-form");
    const erroBox = document.getElementById("mensagem-erro");

    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            // Oculta erro anterior se houver
            erroBox.style.display = "none";
            erroBox.textContent = "";

            const formData = new FormData(form);

            // A API Java espera JSON: { email, senha }. O formulario original usa name="password".
            const credenciais = {
                email: formData.get("email"),
                senha: formData.get("password")
            };

            fetch("/login", {
                method: "POST",
                credentials: "same-origin",
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                body: JSON.stringify(credenciais)
            })
            .then(async response => ({ ok: response.ok, data: await response.json().catch(() => null) }))
            .then(resultado => {
                if (resultado.ok) {
                    // LoginResponse.rotaPendente devolve a pagina pedida antes do login (US-02)
                    const destino = (resultado.data && resultado.data.rotaPendente)
                        ? resultado.data.rotaPendente
                        : "dashboard.html";
                    window.location.href = destino;
                } else {
                    // Exibe a mensagem de erro devolvida pela API
                    erroBox.textContent = PetCleanApi.mensagem({ dados: resultado.data },
                        "E-mail ou senha inválidos.");
                    erroBox.style.display = "block";
                }
            })
            .catch(error => {
                console.error("Erro na requisição:", error);
                erroBox.textContent = "Erro interno de comunicação com o servidor.";
                erroBox.style.display = "block";
            });
        });
    }
});