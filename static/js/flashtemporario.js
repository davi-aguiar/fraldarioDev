// window.onload = function() {
//     var flashes = document.querySelectorAll('#mensagem-flash, #flash-message');
//     console.log(flashes)
//     flashes.forEach(function(flash) {
//         console.log(flash)

//         setTimeout(function() {
//             flash.style.opacity = '0';
//             flash.style.borderWidth = '0px';
//             setTimeout(function() {
//                 flash.remove();
//             }, 300);  // Tempo para transição de opacidade
//         }, 1000);  // 5 segundos para início da transição
//     });
// }


// var mensagem = document.getElementById('flashzin').innerText

// Função para personalizar os alerts

function exibirAlerta(message) {
  const alerta = document.createElement("div");
  alerta.classList.add("toast");

  const toastContent = document.createElement("div");
  toastContent.classList.add("toast-content");

  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message");

  const text2 = document.createElement("span");
  text2.classList.add("text", "text-2");
  text2.textContent = message;

  const closeButton = document.createElement("i");
  closeButton.classList.add("fa-solid", "fa-xmark", "close");

  const progress = document.createElement("div");
  progress.classList.add("progress");

  // Adicionando elementos ao DOM
  messageContainer.appendChild(text2);
  toastContent.appendChild(messageContainer);
  alerta.appendChild(toastContent);
  alerta.appendChild(closeButton);
  alerta.appendChild(progress);
  document.body.appendChild(alerta);

  // Exibindo o alerta
  alerta.classList.add("active");
  progress.classList.add("active");

  // Configurando o temporizador para fechar o alerta após 5 segundos
  const timer = setTimeout(() => {
    alerta.classList.remove("active");
    progress.classList.remove("active");
    document.body.removeChild(alerta); // Removendo o alerta do DOM
    clearTimeout(timer);
  }, 2000);

  // Adicionando evento de clique para fechar o alerta
  closeButton.addEventListener("click", () => {
    alerta.classList.remove("active");
    progress.classList.remove("active");
    document.body.removeChild(alerta); // Removendo o alerta do DOM
    clearTimeout(timer);
  });

}

document.addEventListener('DOMContentLoaded', (event) => {
    // Function to be called when the page is fully loaded
    var mensagem = document.getElementById('flashzin').innerText
    
    exibirAlerta(mensagem)
    
});

