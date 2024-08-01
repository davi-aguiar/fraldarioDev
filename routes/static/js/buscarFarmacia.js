function loadTableData(page) {
  $.ajax({
    url: '/buscaPautorizador/' + page,
    type: 'GET',
    success: function (response) {
      $('#modal-body').html(response); // Atualiza o conteúdo do modal
    },
    error: function (xhr, status, error) {
      console.error('Erro ao carregar dados:', error); // Lidar com erros
    }
  });
}

// Carregar dados ao abrir o modal
$('#dataModal').on('show.bs.modal', function () {
  loadTableData(1);
});

// Clique em links de paginação
$(document).on('click', '.page-next', function (e) {
  e.preventDefault();
  var currentPage = parseInt($('#current-page').val()); // Obtém o número da página atual
  var nextPage = currentPage + 1; // Calcula a próxima página
  loadTableData(nextPage); // Carrega os dados da próxima página
  $('#dataModal').modal('show'); // Abre o modal após carregar os dados
});
