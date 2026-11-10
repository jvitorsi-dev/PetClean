document.addEventListener("DOMContentLoaded", () => {

    const formPerfil = document.getElementById("form-perfil");
    const usuarioId = formPerfil ? formPerfil.dataset.usuarioId : null;

    // =========================
    // MODAL ALTERAR SENHA
    // =========================

    const modal = document.getElementById("modal-senha");

    const btnAbrir = document.getElementById("btn-abrir-modal-senha");
    const btnFechar = document.getElementById("btn-fechar-modal-senha");
    const btnCancelar = document.getElementById("btn-cancelar-modal-senha");

    btnAbrir.addEventListener("click", () => {
        modal.classList.add("active");
    });

    btnFechar.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    btnCancelar.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("active");
        }
    });


    // =========================
    // FOTO DE PERFIL
    // =========================

    const btnFoto = document.getElementById("btn-acionar-foto");
    const inputFoto = document.getElementById("input-foto-avatar");

    btnFoto.addEventListener("click", () => {
        inputFoto.click();
    });

    if (inputFoto) {
        inputFoto.addEventListener("change", async () => {
            if (!inputFoto.files || inputFoto.files.length === 0 || !usuarioId) {
                return;
            }

            const dados = new FormData();
            dados.append("foto", inputFoto.files[0]);

            try {
                const resposta = await fetch("/api/usuarios/" + usuarioId + "/foto", {
                    method: "POST",
                    body: dados,
                    credentials: "same-origin"
                });

                // Sessao expirada: mesmo tratamento do PetCleanApi
                if (resposta.status === 401) {
                    window.location.href = "/paginas/login.html";
                    return;
                }

                let corpo = null;
                try {
                    corpo = await resposta.json();
                } catch (e) {
                    corpo = null;
                }

                if (resposta.ok) {
                    alert("Foto de perfil atualizada com sucesso.");
                    window.location.reload();
                } else {
                    alert(PetCleanApi.mensagem({ ok: false, status: resposta.status, dados: corpo },
                        "Não foi possível enviar a foto de perfil."));
                }
            } catch (erro) {
                console.error("Erro ao enviar a foto:", erro);
                alert("Não foi possível enviar a foto de perfil.");
            }
        });
    }


    // =========================
    // FORM PERFIL
    // =========================

    formPerfil.addEventListener("submit", async function (e) {

        e.preventDefault();

        const dados = {
            nome: formPerfil.querySelector('[name="nome"]').value.trim(),
            email: formPerfil.querySelector('[name="email"]').value.trim(),
            telefone: formPerfil.querySelector('[name="telefone"]').value.trim(),
            nomePetshop: formPerfil.querySelector('[name="nome_petshop"]').value.trim(),
            endereco: formPerfil.querySelector('[name="endereco"]').value.trim()
        };

        const resultado = await PetCleanApi.put("/usuarios/" + usuarioId, dados);

        if (resultado.ok) {
            alert("Perfil atualizado com sucesso.");
            // o cabecalho das paginas mostra nome/e-mail: recarrega para refletir a mudanca
            window.location.reload();
        } else {
            alert(PetCleanApi.mensagem(resultado, "Não foi possível salvar as informações do perfil."));
        }

    });


    // =========================
    // ALTERAR SENHA
    // =========================

    const formSenha = document.getElementById("form-alterar-senha");

    formSenha.addEventListener("submit", async function (e) {

        e.preventDefault();

        const dados = {
            senhaAtual: document.getElementById("senha-atual").value,
            novaSenha: document.getElementById("nova-senha").value
        };

        const resultado = await PetCleanApi.put("/usuarios/" + usuarioId + "/senha", dados);

        if (resultado.ok) {
            alert("Senha alterada com sucesso.");
            modal.classList.remove("active");
            formSenha.reset();
            window.location.reload();
        } else {
            alert(PetCleanApi.mensagem(resultado, "Não foi possível alterar a senha."));
        }

    });

});
