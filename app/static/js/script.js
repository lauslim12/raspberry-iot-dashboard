// DOM Elements
const submitNewBtn = document.querySelector('#button-new-submit');

// Functions
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
