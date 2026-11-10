document.addEventListener("DOMContentLoaded", function () {
    const modalAgend = document.getElementById("modal-agendamento");
    const btnNovoAgend = document.getElementById("btn-novo-agendamento");
    const btnFecharModal = document.getElementById("btn-fechar-modal");
    const btnCancelarModal = document.getElementById("btn-cancelar-modal");
    const formAgend = document.getElementById("form-agendamento");
    
    const inputId = document.getElementById("agendamento-id");
    const inputData = document.getElementById("agend-data");
    const inputHora = document.getElementById("agend-hora");
    const selectServico = document.getElementById("agend-servico");
    const selectPet = document.getElementById("agend-pet");
    const modalTitulo = document.getElementById("modal-titulo");

    if (btnNovoAgend) {
        btnNovoAgend.addEventListener("click", function () {
            formAgend.reset();
            inputId.value = "";
            modalTitulo.textContent = "Novo Agendamento";
            modalAgend.classList.add("active");
        });
    }

    const fecharModal = () => {
        modalAgend.classList.remove("active");
        formAgend.reset();
    };

    if (btnFecharModal) btnFecharModal.addEventListener("click", fecharModal);
    if (btnCancelarModal) btnCancelarModal.addEventListener("click", fecharModal);

    // Mapeamento para Edição
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            inputId.value = this.getAttribute("data-id");
            inputData.value = this.getAttribute("data-data");
            inputHora.value = this.getAttribute("data-hora");
            selectServico.value = this.getAttribute("data-servico");
            selectPet.value = this.getAttribute("data-pet");
            modalTitulo.textContent = "Editar Agendamento";
            modalAgend.classList.add("active");
        });
    });

    // Submissão assíncrona
    if (formAgend) {
        formAgend.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(formAgend);
            const editando = !!inputId.value;
            const idPet = formData.get("pet_id");

            // AgendamentoRequest exige o cliente: ele e obtido a partir do pet escolhido.
            PetCleanApi.get("/pets/" + idPet)
            .then(respostaPet => {
                const pet = respostaPet.ok && respostaPet.dados
                    ? (respostaPet.dados.pet || respostaPet.dados)
                    : null;
                const idCliente = pet && pet.cliente ? pet.cliente.id : null;

                const corpo = {
                    idCliente: idCliente ? Number(idCliente) : null,
                    idPet: Number(idPet),
                    servico: formData.get("servico"),
                    data: formData.get("data_servico"),
                    hora: formData.get("hora_servico")
                };
                const caminho = editando ? "/agendamentos/" + inputId.value : "/agendamentos";
                return PetCleanApi.requisitar(caminho, editando ? "PUT" : "POST", corpo);
            })
            .then(resultado => {
                const resposta = PetCleanApi.envelope(resultado,
                    editando ? "Agendamento atualizado com sucesso!" : "Agendamento realizado com sucesso!",
                    "Não foi possível salvar o agendamento.");
                alert(resposta.mensagem);
                if (resposta.status === "sucesso") {
                    window.location.reload();
                }
            })
            .catch(error => console.error("Erro no agendamento:", error));
        });
    }

    // Excluir Registro
    document.querySelectorAll(".btn-excluir").forEach(btn => {
        btn.addEventListener("click", function () {
            if (confirm("Deseja realmente desmarcar e excluir este agendamento?")) {
                const idExcluir = this.getAttribute("data-id");
                PetCleanApi.del("/agendamentos/" + idExcluir)
                .then(resultado => {
                    const resposta = PetCleanApi.envelope(resultado, "Agendamento excluído com sucesso!",
                        "Não foi possível excluir o agendamento.");
                    alert(resposta.mensagem);
                    if (resposta.status === "sucesso") {
                        window.location.reload();
                    }
                })
                .catch(error => console.error("Erro ao remover agendamento:", error));
            }
        });
    });
});