document.addEventListener("DOMContentLoaded", function() {
    // Obtém o nome da página atual
    var paginaAtual = window.location.pathname.split("/").pop();

    // Verifica se a página atual corresponde à página em que você deseja que o botão seja "selecionado"
    if (paginaAtual === "cadastro") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("cadastro").classList.add("active");
    }
    if (paginaAtual === "cadastroAutorizador") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("cadastro").classList.add("active");
    }
    if (paginaAtual === "cadastro_beneficiado") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("cadastro").classList.add("active");
    }


    if (paginaAtual === "dashboards") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("dashboard").classList.add("active");
    }
    if (paginaAtual === "relatorios") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("relatorios").classList.add("active");
    }



    if (paginaAtual === "visualizar") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "relatorio.html") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("dash").classList.add("active");
    }

    if (paginaAtual === "buscaPautorizador") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "buscaPfarmacia") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "buscaPbeneficiado") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "busca") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "buscaPbeneficiado") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "buscaPbeneficiado") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }
    if (paginaAtual === "buscaPbeneficiado") {
        // Adiciona a classe "selecionado" ao botão
        document.getElementById("visualizar").classList.add("active");
    }



});