document.addEventListener("DOMContentLoaded", function () {
    const checkDarkMode = document.getElementById("check-dark-mode");
    const colorButtons = document.querySelectorAll(".btn-color-pick");

    // 1. SINCRONIZA O ESTADO DO INTERRUPTOR DO MODO ESCURO NA TELA
    if (localStorage.getItem("dark-mode") === "enabled") {
        if (checkDarkMode) checkDarkMode.checked = true;
    }

    if (checkDarkMode) {
        checkDarkMode.addEventListener("change", function () {
            if (checkDarkMode.checked) {
                document.body.classList.add("dark-theme");
                localStorage.setItem("dark-mode", "enabled");
            } else {
                document.body.classList.remove("dark-theme");
                localStorage.setItem("dark-mode", "disabled");
            }
        });
    }

    // 2. SINCRONIZA O ESTADO ATIVO DOS BOTÕES DE PALETA NA TELA
    const corSalva = localStorage.getItem("theme-primary-color");
    if (corSalva) {
        colorButtons.forEach(btn => {
            btn.classList.remove("active");
            if (btn.getAttribute("data-color") === corSalva) {
                btn.classList.add("active");
            }
        });
    }

    colorButtons.forEach(button => {
        button.addEventListener("click", function () {
            colorButtons.forEach(b => b.classList.remove("active"));
            this.classList.add("active");
            
            const corSelecionada = this.getAttribute("data-color");
            
            // Injeta a nova cor na raiz do documento para atualização instantânea
            document.documentElement.style.setProperty('--theme-primary', corSelecionada);
            localStorage.setItem("theme-primary-color", corSelecionada);
        });
    });
});