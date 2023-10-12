const createMessageView = (sender, subject, timestamp, read) => {
    const className = read ? 'message--read' : '';

    return (`
        <li class="message ${className}">
            <span>${sender}</span>
            <span>${subject}</span>
            <span>${timestamp}</span>
        </li>
    `);
};

export const createMessageListView = (emails) => {
    return emails.map(({ sender, subject, timestamp, read }) => {
        return createMessageView(sender, subject, timestamp, read);
    }).join('');
};
