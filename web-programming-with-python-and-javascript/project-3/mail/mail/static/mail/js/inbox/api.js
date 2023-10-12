export const loadMailbox = async (mailbox) => {
    const response = await fetch(`/emails/${mailbox}`);
    const emails = await response.json();
    return emails;
};

export const loadEmail = async (id) => {
    const response = await fetch(`/emails/${id}`);
    const email = await response.json();
    return email;
};

export const sendEmail = async () => {
    await fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: composeRecipients.value,
            subject: composeSubject.value,
            body: composeBody.value
        })
    });
};

