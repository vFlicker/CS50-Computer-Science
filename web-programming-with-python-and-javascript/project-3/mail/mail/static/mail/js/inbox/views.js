const createElement = (template) => {
    const newElement = document.createElement('div');
    newElement.innerHTML = template;

    return newElement.firstElementChild;
};

const createEmailPreviewTemplate = (sender, subject, timestamp, read) => {
    const className = read ? 'email-preview-item--read' : '';

    return (`
        <li class="email-preview-item ${className}">
            <span>${sender}</span>
            <span>${subject}</span>
            <span>${timestamp}</span>
        </li>
    `);
};

const createEmailTemplate = ({ sender, recipients, subject, timestamp, body }) => {
    return (`
        <div class="email">
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
    `);
};

export const createEmailPreviewListView = (emails, onClick) => {
    return emails.map(({ id, sender, subject, timestamp, read }) => {
        const template = createEmailPreviewTemplate(sender, subject, timestamp, read);
        const element = createElement(template);

        element.addEventListener('click', () => onClick(id));

        return element;
    });
};

export const createEmailView = (email) => {
    const template = createEmailTemplate(email);
    const element = createElement(template);
    return element;
};
