document.addEventListener("DOMContentLoaded", function () {
    const modalProd = document.getElementById("modal-produto");
    const btnNovoProd = document.getElementById("btn-novo-produto");
    const btnFecharModal = document.getElementById("btn-fechar-modal");
    const btnCancelarModal = document.getElementById("btn-cancelar-modal");
    const formProd = document.getElementById("form-produto");
    
    const inputId = document.getElementById("produto-id");
    const inputNome = document.getElementById("prod-nome");
    const inputCategoria = document.getElementById("prod-categoria");
    const inputQuantidade = document.getElementById("prod-quantidade");
    const inputMinimo = document.getElementById("prod-minimo");
    const inputPreco = document.getElementById("prod-preco");
    const modalTitulo = document.getElementById("modal-titulo");

    if (btnNovoProd) {
        btnNovoProd.addEventListener("click", function () {
            formProd.reset();
            inputId.value = "";
            modalTitulo.textContent = "Novo Produto";
            modalProd.classList.add("active");
        });
    }

    const fecharModal = () => {
        modalProd.classList.remove("active");
        formProd.reset();
    };

    if (btnFecharModal) btnFecharModal.addEventListener("click", fecharModal);
    if (btnCancelarModal) btnCancelarModal.addEventListener("click", fecharModal);

    // Mapeamento para Edição
    document.querySelectorAll(".btn-editar").forEach(btn => {
        btn.addEventListener("click", function () {
            inputId.value = this.getAttribute("data-id");
            inputNome.value = this.getAttribute("data-nome");
            inputCategoria.value = this.getAttribute("data-categoria");
            inputQuantidade.value = this.getAttribute("data-quantidade");
            inputMinimo.value = this.getAttribute("data-minimo");
            inputPreco.value = this.getAttribute("data-preco");
            modalTitulo.textContent = "Editar Produto";
            modalProd.classList.add("active");
        });
    });

    // Envio assíncrono via FETCH
    if (formProd) {
        formProd.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(formProd);
            const editando = !!inputId.value;

            // A categoria e um <select> com as 6 opcoes do enum da API
            const corpo = {
                nome: formData.get("nome"),
                categoria: formData.get("categoria"),
                quantidade: Number(formData.get("quantidade")),
                estoqueMinimo: Number(formData.get("estoque_minimo")),
                preco: formData.get("preco_venda")
            };
            const caminho = editando ? "/produtos/" + inputId.value : "/produtos";

            PetCleanApi.requisitar(caminho, editando ? "PUT" : "POST", corpo)
            .then(resultado => {
                const resposta = PetCleanApi.envelope(resultado,
                    editando ? "Produto atualizado com sucesso!" : "Produto cadastrado com sucesso!",
                    "Não foi possível salvar o produto.");
                alert(resposta.mensagem);
                if (resposta.status === "sucesso") {
                    window.location.reload();
                }
            })
            .catch(error => console.error("Erro no estoque:", error));
        });
    }

    // Excluir Produto
    document.querySelectorAll(".btn-excluir").forEach(btn => {
        btn.addEventListener("click", function () {
            if (confirm("Tem certeza que deseja remover este produto do estoque?")) {
                const idExcluir = this.getAttribute("data-id");
                PetCleanApi.del("/produtos/" + idExcluir)
                .then(resultado => {
                    const resposta = PetCleanApi.envelope(resultado, "Produto removido do estoque!",
                        "Não foi possível remover o produto.");
                    alert(resposta.mensagem);
                    if (resposta.status === "sucesso") {
                        window.location.reload();
                    }
                })
                .catch(error => console.error("Erro ao remover do estoque:", error));
            }
        });
    });
});