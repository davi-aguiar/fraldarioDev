function inicioButton() {
    window.location.replace("/");
}
function faleButton() {
    window.location.replace("/faleconosco");
}
function rolamentoIndex(classeSecao) {
    var secao = document.getElementsByClassName(classeSecao);
    if (secao.length > 0) {
        secao[0].scrollIntoView({ behavior: 'smooth' });
    }
}

function fecharMensagem() {
    document.getElementById("mensagem-flash").style.display = "none";
}