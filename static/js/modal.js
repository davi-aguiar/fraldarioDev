const dialog = document.getElementById('exampleModal');
const openDialogBtn = document.getElementById('openDialogBtn');
const closeDialogBtn = document.getElementById('closeDialogBtn');
const closeDialogBtnFooter = document.getElementById('closeDialogBtnFooter');

openDialogBtn.addEventListener('click', () => {
  dialog.showModal();
});

closeDialogBtn.addEventListener('click', () => {
  dialog.close();
});

closeDialogBtnFooter.addEventListener('click', () => {
  dialog.close();
});

// modal.js

document.addEventListener('DOMContentLoaded', function () {
  const dialog = document.getElementById('exampleModal');
  const openDialogBtn = document.getElementById('openDialogBtn');
  const closeDialogBtnFooter = document.getElementById('closeDialogBtnFooter');

  if (dialog && openDialogBtn && closeDialogBtnFooter) {
    // Initialize Bootstrap modal
    const bootstrapModal = new bootstrap.Modal(dialog);

    openDialogBtn.addEventListener('click', () => {
      bootstrapModal.show();
    });

    closeDialogBtnFooter.addEventListener('click', () => {
      bootstrapModal.hide();
    });
  }
});
// Seleciona o elemento de confirmação
var escolha = document.getElementById("confirmacao");
var confirmacao=document.getElementById("openDialogBtnF")
// Verifica se o elemento de confirmação está marcado como "Não"
$(document).ready(function() {
  $('#escolha-primaria').click(function() {
      // Verifica se a escolha é "False"
      if ($('#confirmacao:checked').val() === "False") {
          $('#escolhaModalTree').modal('show');
          $('#escolhaModal').modal('hide');
      } else {
          $('#editModal').modal('show');
          $('#escolhaModal').modal('hide');
      }
  });

  $('#escolha-justificativaDois').click(function() {
      $('#escolhaModalTree').modal('hide');
  });
  $('#escolha-justificativaTres').click(function(){
    $('#editModal').modal('show');
    $('#escolhaModalTree').modal('hide');
  })
});


