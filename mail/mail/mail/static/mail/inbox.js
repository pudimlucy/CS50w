document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(is_reply=false, id) {

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // checks if it's a reply
  if (is_reply) {
    // Fetches original email
    fetch('/emails/' + id)
    .then(response => response.json())
    .then(email => {
      // Prepopulates fields with appropriate values
      document.querySelector('#compose-recipients').value = email.recipients;
      document.querySelector('#compose-subject').value = (email.subject.slice(0, 4) === 'Re: ') ? email.subject : `Re: ${email.subject}`;
      document.querySelector('#compose-body').value = `>> On ${email.timestamp}, ${email.sender} wrote: \n\n > ${email.body} \n\n`;
  });}
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load  mailbox's content
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const div = document.createElement('div');
      div.style.border = 'thin solid black';
      if (email['read']) {
        div.style.backgroundColor = 'grey'
      }
      div.innerHTML = `
        <ul>
          <li><b>From: ${email['sender']}</b></li>
          <li><b>Subject: ${email['subject']}</b></li>
          <li><b>Time: ${email['timestamp']}</b></li>
        </ul>
      `;

      // Adds event listener to display email
      div.addEventListener('click', () => view_email(email['id'], mailbox))
      document.querySelector('#emails-view').append(div);
    });
  });
}

function send_email(event) {
  // Prevents from displaying inbox
  event.preventDefault()

  // Creates email with form's contents
  fetch('/emails' , {
    method: 'POST',
    body: JSON.stringify
    ({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  });

  // Displays sent mailbox
  load_mailbox('sent');
}

function view_email(id, mailbox) {

  // Shows email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Fetches email
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {

    // Displays email's content
    document.querySelector('#email-view').innerHTML = `
    <div id="buttons"></div>
    <ul>
      <li><b>From: ${email['sender']}</b></li>
      <li><b>To: ${email['recipients']}</b></li>
      <li><b>Subject: ${email['subject']}</b></li>
      <li><b>Time: ${email['timestamp']}</b></li>
    </ul>
    <p class="m-2">${email['body']}</p>
    `

    // Marks email as read if not read
    if (!email['read']) {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })      
    }

    if (mailbox != 'sent') {
      // Creates archive/unarchive button
      const archiveButton = document.createElement('button');
      archiveButton.type = 'button';
      archiveButton.innerHTML = (email.archived == false) ? 'Archive' : 'Unarchive';

      // Appends archive/unarchive button to buttons div
      document.querySelector('#buttons').append(archiveButton);

      // Adds event listener to archive/unarchive email
      archiveButton.addEventListener('click', () => archive_unarchive(email['id']))

      // Creates reply button
      const replyButton = document.createElement('button');
      replyButton.type = 'button';
      replyButton.innerHTML = 'Reply';

      // Appends reply button to buttons div
      document.querySelector('#buttons').append(replyButton);

      // Adds event listener to reply to email
      replyButton.addEventListener('click', () => compose_email(true, email['id']))
    }
  });
}

function archive_unarchive (id) {

  // Fetches email
  fetch('/emails/' + id)
  .then(response => response.json())
  .then(email => {
    // Updates email's archived property
    fetch('/emails/' + email['id'], {
      method: 'PUT',
      body: JSON.stringify({
        // If archived, unarchive email; if unarchived, archive email
        archived: (email.archived == false)
      })
    })      
  });

  // Loads user's inbox
  load_mailbox('inbox');
}