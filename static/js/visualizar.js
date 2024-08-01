function voltar() {
    window.location.replace('/autorizador.html');
}

function visuBeneficiado() {
    window.location.replace('/visualizaBeneficiado.html');
}

function pesquisarBeneficiado() {
    // Adicione sua lógica de pesquisa aqui
}

function trocaCadastro() {
    // Get all buttons in the sidebar
    const buttons = document.querySelectorAll('.sidebar .button');
    buttons.forEach(button => button.classList.remove('selected'));

    const clickedButton = event.target;
    clickedButton.classList.add('selected');
}

function calcularDataFinal() {
    const dataInicioElement = document.getElementById('data_inicio');
    const validadeMesesElement = document.getElementById('validade_meses');
    const dataFinalElement = document.getElementById('dataFinal');

    if (dataInicioElement && validadeMesesElement && dataFinalElement) {
        const dataInicio = dataInicioElement.value;
        const validadeMeses = validadeMesesElement.value;

        if (dataInicio && validadeMeses) {
            const startDate = new Date(dataInicio);
            const months = parseInt(validadeMeses);

            if (!isNaN(startDate) && !isNaN(months)) {
                // Adiciona os meses à data de início
                startDate.setMonth(startDate.getMonth() + months);

                // Formata a data final
                const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
                dataFinalElement.innerText = startDate.toLocaleDateString('pt-BR', options);
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const hamBurger = document.querySelector(".toggle-btn");
    if (hamBurger) {
        hamBurger.addEventListener("click", function () {
            document.querySelector("#sidebar").classList.toggle("expand");
        });
    }

    // CPF validation
    const cpfInput = document.getElementById('cpf_pesquisado');
    const submitButton = document.querySelector('form button[type="submit"]');
    const feedbackElement = document.querySelector('.invalid-feedback'); // Assuming feedback element exists

    if (cpfInput && submitButton && feedbackElement) {
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
    }

    // Adiciona event listeners aos campos de data de início e validade em meses
    const dataInicioElement = document.getElementById('data_inicio');
    const validadeMesesElement = document.getElementById('validade_meses');
    if (dataInicioElement && validadeMesesElement) {
        dataInicioElement.addEventListener('input', calcularDataFinal);
        validadeMesesElement.addEventListener('input', calcularDataFinal);
    }

    // Calcula a data final ao carregar a página
    calcularDataFinal();
});
