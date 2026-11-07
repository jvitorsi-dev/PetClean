document.addEventListener("DOMContentLoaded", function () {
    const modalCliente = document.getElementById("modal-cliente");
    const btnNovoCliente = document.getElementById("btn-novo-cliente");
    const btnFecharModal = document.getElementById("btn-fechar-modal");
    const btnCancelarModal = document.getElementById("btn-cancelar-modal");
    const formCliente = document.getElementById("form-cliente");
    
    const inputId = document.getElementById("cliente-id");
    const inputNome = document.getElementById("cliente-nome");
    const inputTelefone = document.getElementById("cliente-telefone");
    const inputEmail = document.getElementById("cliente-email");
    const inputCpf = document.getElementById("cliente-cpf");
    const inputEndereco = document.getElementById("cliente-endereco");
    const modalTitulo = document.getElementById("modal-titulo");

    // Abrir para Cadastro
    if (btnNovoCliente) {
        btnNovoCliente.addEventListener("click", function () {
            formCliente.reset();
            inputId.value = "";
            modalTitulo.textContent = "Novo Cliente";
            modalCliente.classList.add("active");
        });
    }

    const fecharModal = () => {
        modalCliente.classList.remove("active");
        formCliente.reset();
    };

    if (btnFecharModal) btnFecharModal.addEventListener("click", fecharModal);
    if (btnCancelarModal) btnCancelarModal.addEventListener("click", fecharModal);

    // Exibe o CPF salvo (a API grava só dígitos) no formato 000.000.000-00
    const formatarCpf = (cpf) => {
        const digitos = (cpf || "").replace(/\D/g, "");
        if (digitos.length !== 11) return cpf || "";
        return digitos.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    };

    // Abrir para Edição (Captura dados direto dos atributos do botão)
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            inputId.value = this.getAttribute("data-id");
            inputNome.value = this.getAttribute("data-nome");
            inputTelefone.value = this.getAttribute("data-telefone");
            inputEmail.value = this.getAttribute("data-email");
            inputCpf.value = formatarCpf(this.getAttribute("data-cpf"));
            inputEndereco.value = this.getAttribute("data-endereco");
            modalTitulo.textContent = "Editar Cliente";
            modalCliente.classList.add("active");
        });
    });

    // Envio do Formulário (Salvar / Atualizar)
    if (formCliente) {
        formCliente.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(formCliente);
            const editando = !!inputId.value;

            // ClienteRequest da API Java (o formulario original nao possui CPF nem endereco)
            const corpo = {
                nome: formData.get("nome"),
                cpf: formData.get("cpf"),
                telefone: formData.get("telefone"),
                email: formData.get("email"),
                endereco: formData.get("endereco")
            };
            const caminho = editando ? "/clientes/" + inputId.value : "/clientes";

            PetCleanApi.requisitar(caminho, editando ? "PUT" : "POST", corpo)
            .then(resultado => {
                const resposta = PetCleanApi.envelope(resultado,
                    editando ? "Cliente atualizado com sucesso!" : "Cliente cadastrado com sucesso!",
                    "Não foi possível salvar o cliente.");
                alert(resposta.mensagem);
                if (resposta.status === "sucesso") {
                    window.location.reload();
                }
            })
            .catch(error => console.error("Erro ao processar cliente:", error));
        });
    }

    // Ação de Exclusão Direta
    document.querySelectorAll(".btn-excluir").forEach(btn => {
        btn.addEventListener("click", function () {
            if (confirm("Tem certeza que deseja excluir este cliente? Todos os pets associados a ele serão removidos.")) {
                const idExcluir = this.getAttribute("data-id");
                PetCleanApi.del("/clientes/" + idExcluir)
                .then(resultado => {
                    const resposta = PetCleanApi.envelope(resultado, "Cliente excluído com sucesso!",
                        "Não foi possível excluir o cliente.");
                    alert(resposta.mensagem);
                    if (resposta.status === "sucesso") {
                        window.location.reload();
                    }
                })
                .catch(error => console.error("Erro ao excluir cliente:", error));
            }
        });
    });
});