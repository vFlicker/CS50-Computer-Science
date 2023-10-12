import * as API from './api.js';
import { createMessageListView } from './views.js';

// Select the containers to be used later
const emailsContainer = document.querySelector('#emails-view');
const composeContainer = document.querySelector('#compose-view');

// Select email list container and title
const emailScreenTitle = emailsContainer.querySelector('h3');
const emailScreenList = emailsContainer.querySelector('ul');

// Select the form and inputs to be used later
const composeForm = composeContainer.querySelector('#compose-form');
const composeRecipients = composeForm.querySelector('#compose-recipients');
const composeSubject = composeForm.querySelector('#compose-subject');
const composeBody = composeForm.querySelector('#compose-body');

// Select action buttons
const actionButtons = document.querySelectorAll('[data-action]')

const showComposeEmail = () => {
    // Show compose view and hide other views
    emailsContainer.style.display = 'none';
    composeContainer.style.display = 'block';

    // Clear out composition fields
    composeRecipients.value = '';
    composeSubject.value = '';
    composeBody.value = '';
};

const showMailbox = async (title, action) => {
    // Show the mailbox and hide other views
    emailsContainer.style.display = 'block';
    composeContainer.style.display = 'none';

    // Show the mailbox name
    emailScreenTitle.textContent = title;

    // Render messages
    const emails = await API.loadMailbox(action);
    const messageList = createMessageListView(emails);
    emailScreenList.innerHTML = messageList;
};


const onActionButtonClickHandler = (evt) => {
    const action = evt.target.dataset.action;
    const title = evt.target.textContent;

    if (action === 'compose') {
        showComposeEmail();
    } else {
        showMailbox(title, action);
    }
};

const onFormSubmitHandler = async (evt) => {
    evt.preventDefault();
    await API.sendEmail();
    showMailbox('Sent', 'sent');
};


// By default, load the inbox
showMailbox('Inbox', 'inbox');

// Use buttons to toggle between views
for (const actionButton of actionButtons) {
    actionButton.addEventListener('click', onActionButtonClickHandler);
}

// Add listener when submit form
composeForm.addEventListener('submit', onFormSubmitHandler);
