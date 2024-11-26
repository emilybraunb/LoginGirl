// Referência ao formulário
const loginForm = document.getElementById('login-form');
// Referência à mensagem de erro
const errorMessage = document.getElementById('error-message');

// Credenciais corretas
const validUsername = "Emizinha";
const validPassword = "Emizinha123";

// Adiciona um evento de submissão ao formulário
loginForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o envio padrão do formulário

    // Obtém os valores inseridos pelo usuário
    const enteredUsername = document.getElementById('username').value;
    const enteredPassword = document.getElementById('password').value;

    // Verifica se as credenciais são válidas
    if (enteredUsername === validUsername && enteredPassword === validPassword) {
        // Redireciona para a página inicial
        window.location.href = "home.html";
    } else {
        // Exibe a mensagem de erro
        errorMessage.style.display = "block";
    }
});
