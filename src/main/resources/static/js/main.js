document.addEventListener("DOMContentLoaded", function () {
    // ==========================================================================
    // 1. MAPEAMENTO DE ELEMENTOS DOS MENUS SUSPENSOS (DROPDOWNS)
    // ==========================================================================
    const gatilhoNotif = document.getElementById("notificacoes-gatilho");
    const menuNotif = document.querySelector(".dropdown-notificacoes-menu");
    const gatilhoPerfil = document.getElementById("perfil-gatilho");
    const menuPerfil = document.querySelector(".dropdown-perfil-menu");

    // ELEMENTOS INTERNOS DO SISTEMA DE NOTIFICAÇÕES
    const badge = document.querySelector(".badge-dot");
    const container = document.getElementById("notif-list-container");
    const countText = document.getElementById("notif-count-text");
    const btnMarcar = document.querySelector(".btn-marcar-todas");

    // ==========================================================================
    // 2. CONTROLE DE INTERAÇÃO DOS DROPDOWNS (ABRIR / FECHAR)
    // ==========================================================================
    
    // Alternar abertura do menu de notificações
    if (gatilhoNotif && menuNotif) {
        gatilhoNotif.addEventListener("click", function (e) {
            e.stopPropagation(); // Impede o clique de propagar para o documento
            if (menuPerfil) menuPerfil.classList.remove("active");
            menuNotif.classList.toggle("active");
        });
    }

    // Alternar abertura do menu de perfil
    if (gatilhoPerfil && menuPerfil) {
        gatilhoPerfil.addEventListener("click", function (e) {
            e.stopPropagation(); // Impede o clique de propagar para o documento
            if (menuNotif) menuNotif.classList.remove("active");
            menuPerfil.classList.toggle("active");
        });
    }

    // Fechar todos os menus ativos se o usuário clicar em qualquer área vazia da tela
    document.addEventListener("click", function () {
        if (menuNotif) menuNotif.classList.remove("active");
        if (menuPerfil) menuPerfil.classList.remove("active");
    });

    // Impede o fechamento indesejado ao clicar dentro das caixas dos menus
    if (menuNotif) {
        menuNotif.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }
    if (menuPerfil) {
        menuPerfil.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }

    // ==========================================================================
    // 3. ENGENHARIA DE ALERTAS E NOTIFICAÇÕES VIA AJAX (ASSÍNCRONO)
    // ==========================================================================
    
    function carregarNotificacoes() {
        // Verifica se o contêiner existe na página atual antes de disparar a requisição
        if (!container) return;

        // A API Java nao possui endpoint de notificacoes: os alertas sao derivados de
        // dados reais ja disponiveis (estoque critico + agenda do dia), sem simular nada.
        const hoje = new Date();
        const dataHoje = hoje.getFullYear() + "-" +
            String(hoje.getMonth() + 1).padStart(2, "0") + "-" +
            String(hoje.getDate()).padStart(2, "0");

        Promise.all([
            PetCleanApi.get("/produtos/estoque-critico"),
            PetCleanApi.get("/agendamentos/agenda?data=" + dataHoje)
        ])
            .then(([estoque, agenda]) => {
                const mensagens = [];

                const criticos = (estoque.ok && Array.isArray(estoque.dados)) ? estoque.dados : [];
                criticos.forEach(produto => {
                    mensagens.push(`Estoque baixo: ${produto.nome} (${produto.quantidade} un.)`);
                });

                let doDia = [];
                if (agenda.ok && agenda.dados) {
                    doDia = Array.isArray(agenda.dados) ? agenda.dados : (agenda.dados.agendamentos || []);
                }
                doDia.forEach(agendamento => {
                    const pet = typeof agendamento.pet === "string"
                        ? agendamento.pet
                        : (agendamento.pet ? agendamento.pet.nome : "Pet");
                    const hora = (agendamento.hora || "").substring(0, 5);
                    mensagens.push(`${hora} - ${pet} (agendamento de hoje)`);
                });

                // "Marcar todas como lidas" nao tem endpoint: o estado fica na sessao do navegador.
                const jaLidas = sessionStorage.getItem("notificacoesLidas") === "1";
                const naoLidas = jaLidas ? 0 : mensagens.length;

                if (naoLidas > 0) {
                    if (badge) {
                        badge.textContent = naoLidas;
                        badge.style.display = "flex";
                    }
                    if (countText) countText.textContent = `Você tem ${naoLidas} novas notificações.`;
                } else {
                    if (badge) badge.style.display = "none";
                    if (countText) countText.textContent = "Nenhuma notificação não lida.";
                }

                // 2. Monta a listagem dinâmica de mensagens dentro do menu
                container.innerHTML = "";
                if (naoLidas === 0 || mensagens.length === 0) {
                    container.innerHTML = '<p style="text-align:center; font-size:12px; color:#99A1AF; padding:12px; margin:0;">Sem alertas pendentes.</p>';
                } else {
                    mensagens.forEach(texto => {
                        container.innerHTML += `
                            <div class="notif-item">
                                <div>${texto}</div>
                            </div>
                        `;
                    });
                }
            })
            .catch(err => console.error("Erro ao processar requisição de alertas:", err));
    }

    // Ação do botão "Marcar todas como lidas"
    if (btnMarcar) {
        btnMarcar.addEventListener("click", function (e) {
            e.stopPropagation(); // Mantém o menu aberto durante o clique

            // Sem endpoint de persistencia na API Java: marca localmente para a sessao.
            sessionStorage.setItem("notificacoesLidas", "1");
            if (badge) badge.style.display = "none";
            if (countText) countText.textContent = "Nenhuma notificação não lida.";
            container.innerHTML = '<p style="text-align:center; font-size:12px; color:#99A1AF; padding:12px; margin:0;">Sem alertas pendentes.</p>';
        });
    }

    // ==========================================================================
    // 4. MECÂNICA DE LOGOUT / SAÍDA DO PAINEL (NOVO)
    // ==========================================================================
    
    // Captura tanto o link do menu lateral quanto o link do menu suspenso do avatar
    const botoesLogout = document.querySelectorAll(".logout, .link-sair-painel");
    
    botoesLogout.forEach(botao => {
        botao.addEventListener("click", function (e) {
            e.preventDefault(); // Cancela o comportamento nativo de link cego HTML
            
            if (confirm("Deseja realmente encerrar sua sessão e sair do sistema?")) {
                // Encerra a sessao na API Java (POST /logout) e volta para o login
                fetch("/logout", { method: "POST", credentials: "same-origin" })
                    .catch(err => console.error("Erro ao encerrar sessão:", err))
                    .finally(() => { window.location.href = "/paginas/login.html"; });
            }
        });
    });

    // Botão "Invalidar Todas as Sessões" (tela de Configurações): mesma semântica do
    // invalidar-sessoes.php original — encerra a sessão atual e volta para o login
    const botaoInvalidarSessoes = document.querySelector(".btn-terminate-sessions");

    if (botaoInvalidarSessoes) {
        botaoInvalidarSessoes.addEventListener("click", function (e) {
            e.preventDefault();

            if (confirm("Tem certeza que deseja invalidar todas as sessões e deslogar do sistema?")) {
                fetch("/logout", { method: "POST", credentials: "same-origin" })
                    .catch(err => console.error("Erro ao invalidar sessões:", err))
                    .finally(() => { window.location.href = "/paginas/login.html"; });
            }
        });
    }

    // ==========================================================================
    // 5. EXECUÇÃO AUTOMÁTICA
    // ==========================================================================
    // Executa a primeira carga de notificações assim que o documento estiver pronto
    carregarNotificacoes();

    // Agenda atualizações automáticas de alertas em background a cada 30 segundos
    setInterval(carregarNotificacoes, 30000);
});