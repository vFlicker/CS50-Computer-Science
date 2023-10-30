import { Action } from './constants.js';

const archiveButtonText = {
    [Action.INBOX]: 'Archive',
    [Action.ARCHIVE]: 'Unarchive',
};

const createElement = (template) => {
    const newElement = document.createElement('div');
    newElement.innerHTML = template;

    return newElement.firstElementChild;
};

const createEmailPreviewTemplate = ({ sender, subject, timestamp, read }, buttonText) => {
    const className = read ? 'email-preview-item--read' : '';

    const button = buttonText
        ? `<button class="email-preview-item__button">${buttonText}</button>`
        : '';

    return (`
        <li class="email-preview-item ${className}">
            <div class="email-preview-item__content">
                <span>${sender}</span>
                <span>${subject}</span>
                <span>${timestamp}</span>
            </div>

            ${button}
        </li>
    `);
};

const createEmailTemplate = ({ sender, recipients, subject, timestamp, body }) => {
    return (`
        <div class="email">
            <div class="email__content">
                <h3 class="email__subject">${subject}</h3>
                <div class="email__header">
                    <div>
                        <div class="email__sender"><span>Sender:</span> ${sender}</div>
                        <div class="email__recipients"><span>Recipients:</span> ${recipients.join(', ')}</div>
                    </div>
                    <div class="email__time">${timestamp}</div>
                </div>
                <div class="email__body">${body}</div>
            </div>

            <button class="email__reply btn btn-primary">Reply</button>
        </div>
    `);
};

export const createEmailPreviewListView = (emails, action, onEmailPreviewClick, onButtonClick) => {
    const buttonText = archiveButtonText[action];

    return emails.map(({ id, sender, subject, timestamp, read }) => {
        const template = createEmailPreviewTemplate({ sender, subject, timestamp, read }, buttonText);
        const element = createElement(template);

        element
            .addEventListener('click', () => onEmailPreviewClick(id));

        const buttonElement = element.querySelector('.email-preview-item__button');
        if (buttonElement) {
            buttonElement.addEventListener('click', (evt) => {
                evt.stopPropagation();
                onButtonClick(id, action);
            });
        }

        return element;
    });
};

export const createEmailView = (email, onReplyClick) => {
    const template = createEmailTemplate(email);
    const element = createElement(template);

    element
        .querySelector('.email__reply')
        .addEventListener('click', () => onReplyClick(email))

    return element;
};
