

var cpf = document.getElementById("cpfPego").value;
var dataAtual = new Date();
function visu() {
    window.location.replace('http://127.0.0.1:5000/visualizaBeneficiado.html')
}
function visuPendente() {
    window.location.replace('http://127.0.0.1:5000/usuarioPendente.html')
}
function visuRelatorio() {
    window.location.replace('http://127.0.0.1:5000/relatorioFarmacia.html')
}
function voltarIndex() {
    window.history.back();
}
function voltarVisu() {
    window.location.replace('http://127.0.0.1:5000/visualizaFarmacia.html')
}
function inicioIndex() {
    window.location.replace('http://127.0.0.1:5000/')

}
function trocaUsuarioPendente() {
    window.location.replace('http://127.0.0.1:5000/usuarioPendente.html')
}
function trocaRelatorio() {
    window.location.replace('http://127.0.0.1:5000/relatorioFarmacia.html')
}

function fecharMensagem() {
    document.getElementById("mensagem-flash").style.display = "none";
}

function gerarelatorio() {

}

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});

var myModal = document.getElementById('exampleModal'); // Corrigindo o ID do modal
var myInput = document.getElementById('myInput');

myModal.addEventListener('shown.bs.modal', function () {
    myInput.focus();
});
// Obter o formulário de edição da farmácia
const form = document.getElementById('editFarmaciaForm');

// Adicionar um ouvinte de evento para o evento de envio do formulário
form.addEventListener('submit', function (event) {
    // Impedir o envio padrão do formulário
    event.preventDefault();

    // Obter os dados do formulário
    const formData = new FormData(form);

    // Converter os dados do formulário em um objeto JSON
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Enviar os dados como JSON para a rota de atualização da farmácia
    fetch('/atualizar_farmacia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Definir o tipo de conteúdo como JSON
        },
        body: JSON.stringify(jsonData) // Enviar os dados como JSON
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao atualizar a farmácia.');
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Exibir a resposta do servidor no console
            // Aqui você pode adicionar lógica adicional, como mostrar uma mensagem de sucesso
        })
        .catch(error => {
            console.error(error); // Lidar com erros de requisição
            // Aqui você pode adicionar lógica adicional, como mostrar uma mensagem de erro ao usuário
        });
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

// Adicionando um event listener para o overlay
document.getElementById("overlay").addEventListener("click", function () {
    togglePopup(); // Fecha o popup quando o overlay é clicado
});
function openPdfInNewTab() {
    fetch('/createPdf', {
        method: 'POST'
    })
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            window.open(url, '_blank');
        })
        .catch(error => {
            console.error('Erro ao abrir o PDF:', error);
        });
}