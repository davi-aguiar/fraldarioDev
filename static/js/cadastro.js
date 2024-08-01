function mostrarCampo(id) {
    var campo = document.getElementById(id);
    campo.style.display = "block";
}
function mostrarSenha() {
    var inputPass = document.getElementById("password")
    var btnShowPass = document.getElementById("btn-senha")
    if (inputPass.type === 'password') {
        inputPass.setAttribute('type', 'text');
        btnShowPass.classList.replace('bi-eye-fill', 'bi-eye-slash-fill')
    } else {
        inputPass.setAttribute('type', 'password')
        btnShowPass.classList.replace('bi-eye-slash-fill', 'bi-eye-fill')
    }
}
function mostraSenha() {
    var campoSenha = document.getElementById("passwordConfirmed")
    var mostraSenha = document.getElementById("btn-confirma")
    if (campoSenha.type === 'password') {
        campoSenha.setAttribute('type', 'text');
        mostraSenha.classList.replace('bi-eye-fill', 'bi-eye-slash-fill')
    } else {
        campoSenha.setAttribute('type', 'password')
        mostraSenha.classList.replace('bi-eye-slash-fill', 'bi-eye-fill')
    }
}
function confereSenha() {
    const senha = document.querySelector('input[name=password]');
    const confirma = document.querySelector('input[name=passwordConfirmed]');

    if (confirma.value === senha.value) {
        confirma.setCustomValidity('');
    } else {
        confirma.setCustomValidity('As senhas não conferem')
    }
}
function handleFormSubmit() {
    const button = document.getElementById('buttonEnvio');
    button.disabled = true;
    button.innerHTML = 'Enviando... <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
}
function ocultarCampo(id) {
    var campo = document.getElementById(id);
    campo.style.display = "none";
}

function selecionarTipoLogin() {
    var radioFarmacia = document.getElementById("loginFarmacia");
    var radioAutorizador = document.getElementById("loginAutorizador");
    var radioPrefeitura = document.getElementById("loginPrefeitura");
    var inputCnpj = document.getElementById("campoCnpj");
    var inputCpf = document.getElementById("campoCpf");
    var inputPrefeitura = document.getElementById("campoPrefeitura")
    if (radioFarmacia.checked) {
        mostrarCampo("campoCnpj");
        ocultarCampo("campoCpf");
        ocultarCampo("campoPrefeitura");
        inputCnpj.value = "1"; // Para o tipo de login Farmácia
    } else if (radioAutorizador.checked) {
        mostrarCampo("campoCpf");
        ocultarCampo("campoCnpj");
        ocultarCampo("campoPrefeitura");
        inputCpf.value = "2"; // Para o tipo de login Autorizador
    } else if (radioPrefeitura.checked) {
        ocultarCampo("campoCpf");
        ocultarCampo("campoCnpj");
        mostrarCampo("campoPrefeitura");
        inputPrefeitura.value = "3";
    }
}

function voltarPrefeitura() {
    window.location.replace("http://127.0.0.1:5000/pagina_prefeitura");
}
function fecharMensagem() {
    document.getElementById("mensagem-flash").style.display = "none";
}


function buscarCep() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    document.getElementById('logradouro').value = data.logradouro;
                    document.getElementById('cidade').value = data.localidade;
                    document.getElementById('estado').value = data.uf;
                    document.getElementById('bairro').value = data.bairro;
                } else {
                    alert('CEP não encontrado.');
                }
            })
            .catch(error => console.error('Erro ao buscar CEP:', error));
    } else {
        alert('Formato de CEP inválido.');
    }
}

function selecionarTipoLogin() {
    const tipoLogin = document.querySelector('input[name="login"]:checked').value;
    document.getElementById('campoCnpj').style.display = tipoLogin == 1 ? 'block' : 'none';
    document.getElementById('campoCpf').style.display = tipoLogin == 2 ? 'block' : 'none';
    document.getElementById('campoPrefeitura').style.display = tipoLogin == 3 ? 'block' : 'none';
}





document.addEventListener('DOMContentLoaded', function() {
    // Verifica se há algum input radio selecionado
    var tipoLogin = document.querySelector('input[name="login"]:checked');
    if (tipoLogin) {
        selecionarTipoLogin();
    }
});

function selecionarTipoLogin() {
    var tipoLogin = document.querySelector('input[name="login"]:checked').value;
    document.getElementById('campoCnpj').style.display = (tipoLogin == '1') ? 'block' : 'none';
    document.getElementById('campoCpf').style.display = (tipoLogin == '2') ? 'block' : 'none';
    document.getElementById('campoPrefeitura').style.display = (tipoLogin == '3') ? 'block' : 'none';
}

function consultarDocumento(tipo) {
    let documento = '';
    if (tipo === 'cnpj') {
        documento = document.getElementById('cnpj').value;
        fetch(`/consultar_cnpj/${documento}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw new Error(data.error); });
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    document.getElementById('nomeFantasia').value = data.fantasia || data.nome;
                    document.getElementById('razaoSocial').value = data.nome;
                    // Preencha outros campos conforme necessário
                }
            })
            .catch(error => {
                flashMessage(error.message);
            });
    } else if (tipo === 'cpf') {
        documento = document.getElementById('cpf').value;
        fetch(`/consultar_cpf/${documento}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw new Error(data.error); });
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    document.getElementById('nomeAutorizador').value = data.nome;
                    // Preencha outros campos conforme necessário
                }
            })
            .catch(error => {
                flashMessage(error.message);
            });
    }
}

function flashMessage(message) {
    const flashDiv = document.getElementById('mensagem-flash');
    const flashContent = document.getElementById('flashzin');
    flashContent.textContent = message;
    flashDiv.style.display = 'block';
    setTimeout(() => {
        flashDiv.style.display = 'none';
    }, 5000);
}

