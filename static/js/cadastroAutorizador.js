function voltar() {
    window.location.replace("http://127.0.0.1:5000/autorizador.html")
}
// Função para preencher o campo de data com a data atual
function preencherDataAtual() {
    // Obter a data atual
    var dataAtual = new Date();
    var ano = dataAtual.getFullYear();
    var mes = ('0' + (dataAtual.getMonth() + 1)).slice(-2);
    var dia = ('0' + dataAtual.getDate()).slice(-2);
    var dataFormatada = ano + '-' + mes + '-' + dia;

    // Atribuir a data atual ao valor do campo de data
    document.getElementById('dataInicio').value = dataFormatada;
}

// Chamar a função quando a página for carregada
window.onload = preencherDataAtual;
function fecharMensagem() {
    document.getElementById("mensagem-flash").style.display = "none";
}

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});



