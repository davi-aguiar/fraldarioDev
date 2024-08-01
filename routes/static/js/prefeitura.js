function trocaCadastro() {
    window.location.replace("http://127.0.0.1:5000/cadastro");
}
function trocaVisualizar() {
    window.location.replace("http://127.0.0.1:5000/visualiza.html");
}
function voltarParaIndex() {
    window.location.replace("http://127.0.0.1:5000/");
}
function faleButton() {
    window.location.replace("http://127.0.0.1:5000/faleconosco.html");
}
function rolamentoIndex(secaoId) {
    var secao = document.getElementById(secaoId);
    if (secao) {
        secao.scrollIntoView({ behavior: 'smooth' });
    }
}
function fecharMensagem() {
    document.getElementById("flash-message").style.display = "none";
}


const hamburger = document.querySelector("#toggle-btn");

hamburger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});
function listarArquivos() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var files = JSON.parse(this.responseText);
            var fileList = document.getElementById("file-list");
            fileList.innerHTML = ""; // Limpa a lista antes de adicionar os novos arquivos
            if (files.length > 0) {
                files.forEach(function (file) {
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    a.textContent = file.filename;
                    a.href = "#"; // Define temporariamente o href como "#" para evitar que o navegador navegue
                    a.onclick = function () {
                        baixarArquivo(file.url, file.filename);
                        return false; // Evita a navegação padrão ao clicar no link
                    };
                    li.appendChild(a);
                    fileList.appendChild(li);
                });
                showPopup(); // Exibe o popup com a lista de arquivos
            } else {
                alert("Nenhum arquivo encontrado.");
            }
        }
    };
    xhttp.open("GET", "/list-files-prefeitura", true);
    xhttp.send();
}

function baixarArquivo(url, filename) {
    var link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
}

function visualizarPDF(url) {
    var link = document.createElement('a');
    link.href = url;
    link.download = url.substr(url.lastIndexOf('/') + 1);
    link.click();
}

var isPopupOpen = false;

function togglePopup() {
    if (isPopupOpen) {
        hidePopup();
    } else {
        listarArquivos(); // Se o popup não estiver aberto, lista os arquivos antes de exibir o popup
        showPopup();
    }
}

function showPopup() {
    document.getElementById("popup").style.display = "block";
    document.getElementById("overlay").style.display = "block";
    isPopupOpen = true;
}

function hidePopup() {
    document.getElementById("popup").style.display = "none";
    document.getElementById("overlay").style.display = "none";
    isPopupOpen = false;
}