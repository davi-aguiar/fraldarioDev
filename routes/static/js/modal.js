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
