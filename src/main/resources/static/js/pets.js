document.addEventListener("DOMContentLoaded", function () {
    const modalPet = document.getElementById("modal-pet");
    const btnNovoPet = document.getElementById("btn-novo-pet");
    const btnFecharModal = document.getElementById("btn-fechar-modal");
    const btnCancelarModal = document.getElementById("btn-cancelar-modal");
    const formPet = document.getElementById("form-pet");
    
    const inputId = document.getElementById("pet-id");
    const inputNome = document.getElementById("pet-nome");
    const inputRaca = document.getElementById("pet-raca");
    const inputIdade = document.getElementById("pet-idade");
    const selectCliente = document.getElementById("pet-cliente");
    const modalTitulo = document.getElementById("modal-titulo");

    if (btnNovoPet) {
        btnNovoPet.addEventListener("click", function () {
            formPet.reset();
            inputId.value = "";
            modalTitulo.textContent = "Novo Pet";
            modalPet.classList.add("active");
        });
    }

    const fecharModal = () => {
        modalPet.classList.remove("active");
        formPet.reset();
    };

    if (btnFecharModal) btnFecharModal.addEventListener("click", fecharModal);
    if (btnCancelarModal) btnCancelarModal.addEventListener("click", fecharModal);

    // Mapeamento de Edição
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            inputId.value = this.getAttribute("data-id");
            inputNome.value = this.getAttribute("data-nome");
            inputRaca.value = this.getAttribute("data-raca");
            inputIdade.value = this.getAttribute("data-idade");
            selectCliente.value = this.getAttribute("data-cliente");
            modalTitulo.textContent = "Editar Pet";
            modalPet.classList.add("active");
        });
    });

    // Submissão do Formulário
    if (formPet) {
        formPet.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(formPet);
            const editando = !!inputId.value;

            // PetRequest da API Java (especie e porte sao obrigatorios na API e nao
            // existem no formulario original: se faltarem, a API devolve o erro real)
            const corpo = {
                idCliente: Number(formData.get("cliente_id")),
                nome: formData.get("nome"),
                raca: formData.get("raca"),
                idade: formData.get("idade") ? Number(formData.get("idade")) : null
            };
            const caminho = editando ? "/pets/" + inputId.value : "/pets";

            PetCleanApi.requisitar(caminho, editando ? "PUT" : "POST", corpo)
            .then(resultado => {
                const resposta = PetCleanApi.envelope(resultado,
                    editando ? "Pet atualizado com sucesso!" : "Pet cadastrado com sucesso!",
                    "Não foi possível salvar o pet.");
                alert(resposta.mensagem);
                if (resposta.status === "sucesso") {
                    window.location.reload();
                }
            })
            .catch(error => console.error("Erro ao processar pet:", error));
        });
    }

    // Ação de Exclusão
    document.querySelectorAll(".btn-excluir").forEach(btn => {
        btn.addEventListener("click", function () {
            if (confirm("Tem certeza que deseja remover este pet do sistema?")) {
                const idExcluir = this.getAttribute("data-id");
                PetCleanApi.del("/pets/" + idExcluir)
                .then(resultado => {
                    const resposta = PetCleanApi.envelope(resultado, "Pet removido com sucesso!",
                        "Não foi possível remover o pet.");
                    alert(resposta.mensagem);
                    if (resposta.status === "sucesso") {
                        window.location.reload();
                    }
                })
                .catch(error => console.error("Erro ao excluir pet:", error));
            }
        });
    });
});