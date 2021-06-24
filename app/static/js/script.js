// DOM Elements
const submitNewBtn = document.querySelector('#button-new-submit');
const submitEditBtn = document.querySelector('#button-edit-submit');

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
    .then((res) => {
      if (res.status === 'success') {
        showAlert('success', 'You have added a new data!');

        window.setTimeout(() => {
          location.replace('/');
        }, 1500);
      }
    })
    .catch((err) => {
      showAlert('error', err.message);
    });
};

const submitEditForm = (e) => {
  e.preventDefault();

  const linkId = document.querySelector('#link_id').value;
  const linkName = document.querySelector('#link_name').value;
  const linkDescription = document.querySelector('#link_description').value;
  const linkUrl = document.querySelector('#link_url').value;

  const options = {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: linkName,
      description: linkDescription,
      url: linkUrl,
    }),
  };

  fetch(`/api/v1/links/${linkId}`, options)
    .then((raw) => raw.json())
    .then((res) => {
      if (res.status === 'success') {
        showAlert('success', 'You have edited the data!');

        window.setTimeout(() => {
          location.replace('/');
        }, 1500);
      }
    })
    .catch((err) => {
      showAlert('error', err.message);
    });
};

// Delegations
if (submitNewBtn) {
  submitNewBtn.addEventListener('click', (e) => submitNewForm(e));
}

if (submitEditBtn) {
  submitEditBtn.addEventListener('click', (e) => submitEditForm(e));
}
