// ===============================
// MÁSCARA DE TELEFONE
// ===============================
const telFale = document.getElementById("telefone");

if (telFale) {
  telFale.addEventListener("keypress", (e) => {
    if (!/[0-9]/.test(e.key)) e.preventDefault();
  });

  telFale.addEventListener("paste", (e) => {
    const texto = (e.clipboardData || window.clipboardData).getData("text");
    if (!/^\d+$/.test(texto)) e.preventDefault();
  });

  telFale.addEventListener("input", function () {
    let v = telFale.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length <= 10) {
      telFale.value = v.replace(/(\d{2})(\d)/, "($1) $2");
    } else {
      telFale.value = v.replace(/(\d{2})(\d{5})(\d)/, "($1) $2-$3");
    }
  });
}

// ===============================
// VALIDAÇÃO DE EMAIL
// ===============================
function validarEmailFale(email) {
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$/.test(email);
}

// ===============================
// FORMULÁRIO FALE CONOSCO
// ===============================
const formFale = document.querySelector(".form");
const modalSucesso = document.getElementById("modal-sucesso");

if (formFale && modalSucesso) {
  formFale.addEventListener("submit", function (e) {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const assunto = document.getElementById("assunto").value;
    const mensagem = document.getElementById("mensagem").value.trim();

    // VALIDAÇÕES
    if (nome.length < 3) {
      alert("Digite um nome válido.");
      return;
    }
    if (!validarEmailFale(email)) {
      alert("Digite um e-mail válido.");
      return;
    }
    if (!assunto) {
      alert("Selecione um assunto.");
      return;
    }
    if (mensagem.length < 5) {
      alert("A mensagem deve ter pelo menos 5 caracteres.");
      return;
    }

    // DISPARAR MODAL
    modalSucesso.classList.add("mostrar");

    // LIMPAR CAMPOS
    formFale.reset();

    // ESCONDER DEPOIS DE 3 SEGUNDOS
    setTimeout(() => {
      modalSucesso.classList.remove("mostrar");
    }, 3000);
  });
}