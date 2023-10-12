document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Select the inputs to be used later
    const composeRecipients = document.querySelector('#compose-recipients')
    const composeSubject = document.querySelector('#compose-subject')
    const composeBody = document.querySelector('#compose-body')

    // Clear out composition fields
    composeRecipients.value = '';
    composeSubject.value = '';
    composeBody.value = '';

    document.querySelector('#compose-form').onsubmit = () => {
        fetch('/emails', {
                method: 'POST',
                body: JSON.stringify({
                    recipients: composeRecipients.value,
                    subject: composeSubject.value,
                    body: composeBody.value
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);

                // Load the user’s sent mailbox
                load_mailbox('sent');
            });

        // Stop form from submitting
        return false;
    };
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            // Print emails
            console.log(emails);

            const ul = document.createElement('ul');
            const message_list = emails.map(({ sender, subject, timestamp }) => {
                return message_view(sender, subject, timestamp);
            });

            ul.append(...message_list);
            document.querySelector('#emails-view').append(ul);
        });
}

function message_view(from, subject, timestamp) {
    const element = document.createElement('li');
    element.innerHTML = `${from}, ${subject}, ${timestamp}`;
    element.addEventListener('click', () => {
        console.log('This element has been clicked!')
    });

    return element;
}