export const loadEmail = async (id) => {
    const response = await fetch(`/emails/${id}`);
    const email = await response.json();
    return email;
};

export const readEmail = async (id) => {
    await fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true,
        })
    });
};

export const archiveEmail = async (id) => {
    await fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true,
        })
    });
};

export const unarchiveEmail = async (id) => {
    await fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false,
        })
    });
};

export const loadEmails = async (mailbox) => {
    const response = await fetch(`/emails/${mailbox}`);
    const emails = await response.json();
    return emails;
};

export const sendEmail = async (body) => {
    await fetch('/emails', {
        method: 'POST',
        body: JSON.stringify(body),
    });
};

