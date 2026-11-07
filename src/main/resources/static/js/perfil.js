document.addEventListener("DOMContentLoaded", () => {

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


    // =========================
    // FORM PERFIL
    // =========================

    const formPerfil = document.getElementById("form-perfil");

    formPerfil.addEventListener("submit", async function (e) {

        e.preventDefault();

        // PENDENCIA: a API Java nao possui endpoint de atualizacao de perfil/foto.
        // Nao simulamos sucesso: informamos o usuario e mantemos os dados intactos.
        PetCleanApi.pendente("Atualizar perfil");
        alert("Não foi possível salvar as informações do perfil: recurso ainda não disponível na API Java (pendência documentada).");

    });


    // =========================
    // ALTERAR SENHA
    // =========================

    const formSenha = document.getElementById("form-alterar-senha");

    formSenha.addEventListener("submit", async function (e) {

        e.preventDefault();

        // PENDENCIA: a API Java nao possui endpoint de alteracao de senha.
        PetCleanApi.pendente("Alterar senha");
        alert("Não foi possível alterar a senha: recurso ainda não disponível na API Java (pendência documentada).");

    });

});