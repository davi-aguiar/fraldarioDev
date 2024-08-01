document.addEventListener("DOMContentLoaded", function () {
  // Tempo em milissegundos para a tela de splash (por exemplo, 3 segundos)
  var splashScreenTime = 3000;

  setTimeout(function () {
    // Esconder a tela de splash
    var splashScreen = document.getElementById("splash-screen");
    splashScreen.style.opacity = '0';
    splashScreen.style.transition = 'opacity 1s ease-out';

    setTimeout(function () {
      splashScreen.style.display = 'none';

      // Mostrar o conteúdo principal
      var mainContent = document.getElementById("main-content");
      mainContent.style.display = "block";
    }, 1000); // Tempo para a transição de opacidade
  }, splashScreenTime);
});