import * as API from './api.js';
import { createEmailPreviewListView, createEmailView } from './views.js';

// Select all screens
const screens = document.querySelectorAll('[data-screen]');

// Select the containers to be used later
const emailContainer = document.querySelector('#email-view');
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


const setActiveScreen = (name) => {
    for (const screen of screens) {
        if (screen.dataset.screen === name) screen.style.display = 'block';
        else screen.style.display = 'none';
    }
};

const showComposeEmail = () => {
    setActiveScreen('compose');

    // Clear out composition fields
    composeRecipients.value = '';
    composeSubject.value = '';
    composeBody.value = '';
};

const showEmail = async (id) => {
    setActiveScreen('email');

    // Render email
    const email = await API.loadEmail(id);
    const emailView = createEmailView(email);
    emailContainer.replaceChildren(emailView);
};

const showMailbox = async (title, action) => {
    setActiveScreen('emails');

    // Show the mailbox name
    emailScreenTitle.textContent = title;

    // Render email previews
    const emails = await API.loadEmails(action);
    const emailPreviewListView = createEmailPreviewListView(emails, showEmail);
    emailScreenList.replaceChildren(...emailPreviewListView);
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
