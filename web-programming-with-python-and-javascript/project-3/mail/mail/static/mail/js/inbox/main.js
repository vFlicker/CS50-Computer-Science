import * as API from './api.js';
import { Action, Screen } from './constants.js';
import { createEmailPreviewListView, createEmailView } from './views.js';
import { capitalizeFirstLetter } from './utils.js';

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

const showComposeEmail = ({ recipients, subject, body } = {}) => {
    setActiveScreen(Screen.COMPOSE);

    // Set data or clear fields
    composeRecipients.value = recipients ?? '';
    composeSubject.value = subject ?? '';
    composeBody.value = body ?? '';
};

const handleReplyClick = ({ sender, subject }) => {
    showComposeEmail({ recipients: [sender], subject });
};

const handleEmailPreviewClick = async (id) => {
    setActiveScreen(Screen.EMAIL);

    // Render email
    const email = await API.loadEmail(id);
    const emailView = createEmailView(email, handleReplyClick);
    emailContainer.replaceChildren(emailView);

    // Mark the email as read
    API.readEmail(id);
};

const handleButtonClick = async (id, action) => {
    switch (action) {
        case Action.INBOX:
            await API.archiveEmail(id);
            showMailbox('Inbox', Action.INBOX);
            break;
        case Action.ARCHIVE:
            await API.unarchiveEmail(id);
            showMailbox('Inbox', Action.ARCHIVE);
            break;
    }
};

const showMailbox = async (title, action) => {
    setActiveScreen(Screen.EMAILS);

    // Show the mailbox name
    emailScreenTitle.textContent = title;

    // Render email previews
    const emails = await API.loadEmails(action);

    const emailPreviewListView = createEmailPreviewListView(emails, action, handleEmailPreviewClick, handleButtonClick);
    emailScreenList.replaceChildren(...emailPreviewListView);
};


const applyAction = (action) => {
    const title = capitalizeFirstLetter(action);

    if (action === Action.COMPOSE) {
        showComposeEmail();
    } else {
        showMailbox(title, action);
    }
};

const onActionButtonClickHandler = (evt) => {
    const action = evt.target.dataset.action;

    applyAction(action);
    history.pushState({ screen: action}, "", action);
};

const onFormSubmitHandler = async (evt) => {
    evt.preventDefault();

    await API.sendEmail({
        recipients: composeRecipients.value,
        subject: composeSubject.value,
        body: composeBody.value,
    });

    showMailbox('Sent', Action.SENT);
};

const onStatePop = (evt) => {
    applyAction(evt.state.screen);
};

// By default, load the inbox
showMailbox('Inbox', Action.INBOX);
history.pushState({ screen: Action.INBOX}, "", Action.INBOX);

// Use buttons to toggle between views
for (const actionButton of actionButtons) {
    actionButton.addEventListener('click', onActionButtonClickHandler);
}

// Add listener when submit form
composeForm.addEventListener('submit', onFormSubmitHandler);

// Add listener when user click back in browser
window.addEventListener('popstate', onStatePop);
