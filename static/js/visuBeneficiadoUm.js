function voltar() {
    window.location.replace('/autorizador.html');
}
function visuBeneficiado() {
    window.location.replace('/visualizaBeneficiado.html');
}

function pesquisarBeneficiado() {

}

function trocaCadastro() {
    // Get all buttons in the sidebar
    const buttons = document.querySelectorAll('.sidebar .button');

    buttons.forEach(button => button.classList.remove('selected'));


    const clickedButton = event.target;


    clickedButton.classList.add('selected');
}


const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});

(function () {
    'use strict';

    // Get references to input and submit button
    const cpfInput = document.getElementById('cpf_pesquisado');
    const submitButton = document.querySelector('form button[type="submit"]');
    const feedbackElement = document.querySelector('.invalid-feedback'); // Assuming feedback element exists

    // Event listener for input changes
    cpfInput.addEventListener('input', function () {
        // Remove non-digits from input value
        const cpf = cpfInput.value.replace(/\D/g, '');

        // Check for valid CPF (11 digits, all numbers)
        const isValid = cpf.length === 11 && /^\d+$/.test(cpf);

        // Toggle submit button disabled state based on validity
        submitButton.disabled = !isValid;

        // Update feedback based on validity
        if (isValid) {
            feedbackElement.style.display = 'none'; // Hide feedback if valid
        } else {
            feedbackElement.style.display = 'block'; // Show feedback if invalid
        }
    });
})();

