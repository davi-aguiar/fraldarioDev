// loading.js
function handleFormSubmit(event) {
  const submitBtn = document.getElementById('submitBtn');
  const spinner = submitBtn.querySelector('.spinner-border');
  const buttonText = submitBtn.querySelector('.button-text');

  submitBtn.disabled = true;
  spinner.classList.remove('d-none');
  buttonText.textContent = "Enviando...";
}
