function trocaCadastro(){
    window.location.replace("http://127.0.0.1:5000/cadastroAutorizador.html");
}
function trocaVisualizar(){
    window.location.replace("http://127.0.0.1:5000/visualizaBeneficiado.html");
}
function voltarParaIndex(){
    window.location.replace("http://127.0.0.1:5000/");
}
function faleButton(){
    window.location.replace("http://127.0.0.1:5000/faleconosco.html");
}
function rolamentoIndex(secaoId) {
    var secao= document.getElementById(secaoId);
    if (secao) {
        secao.scrollIntoView({ behavior: 'smooth' });
    }
}