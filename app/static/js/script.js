// DOM Elements
const submitNewBtn = document.querySelector('#button-new-submit');

// Functions
const hideAlert = () => {
  const el = document.querySelector('.alert');

  if (el) {
    el.parentElement.removeChild(el);
  }
};

const showAlert = (type, message, time = 7) => {
  hideAlert();

  const markup = `<div class='alert alert--${type}'>${message}</div>`;
  document.querySelector('body').insertAdjacentHTML('afterbegin', markup);
  window.setTimeout(hideAlert, time * 1000);
};

const submitNewForm = (e) => {
  e.preventDefault();

  const linkName = document.querySelector('#link_name').value;
  const linkDescription = document.querySelector('#link_description').value;
  const linkUrl = document.querySelector('#link_url').value;

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: linkName,
      description: linkDescription,
      url: linkUrl,
    }),
  };

  fetch('/api/v1/links/', options)
    .then((raw) => raw.json())
    .then((res) => console.log(res))
    .catch((err) => console.log(err));
};

// Delegations
if (submitNewBtn) {
  submitNewBtn.addEventListener('click', (e) => submitNewForm(e));
}
