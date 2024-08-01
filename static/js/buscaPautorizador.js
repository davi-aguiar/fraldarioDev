// máscara cpf => pontos e traços

function mascaraCPF(cpf) {
    cpf.value = cpf.value
        .replace(/\D/g, '') // Remove caracteres não numéricos
        .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto entre o terceiro e o quarto dígitos
        .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto entre o sexto e o sétimo dígitos
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Coloca um traço entre o nono e o décimo dígitos
};



const hamburger = document.querySelector("#toggle-btn");

hamburger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});


function fecharMensagem() {
    document.getElementById("mensagem-flash").style.display = "none";
};

(function () {
    'use strict';

    // Get references to input and submit button
    const cpfInput = document.getElementById('cpf_pesquisado');
    const submitButton = document.querySelector('form button[type="submit"]');
    const feedbackElement = document.querySelector('.invalid-feedback'); // Assuming feedback element exists


    cpfInput.addEventListener('input', function () {
        // Remove non-digits from input value
        const cpf = cpfInput.value.replace(/\D/g, '');


        const isValid = cpf.length === 11 && /^\d+$/.test(cpf);


        submitButton.disabled = !isValid;


        if (isValid) {
            feedbackElement.style.display = 'none';
        } else {
            feedbackElement.style.display = 'block';
        }
    });
})();


