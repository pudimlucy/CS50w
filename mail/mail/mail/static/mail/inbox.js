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

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
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
      let div = document.createElement('div');
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
      div.addEventListener('click', () => view_email(email['id']))
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
  })

  // Displays sent mailbox
  .then(response => response.json())
  .then(response => {
    load_mailbox('sent');
  });
}

function view_email(id) {

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
  })

  // TODO: create archive, unarchive, reply buttons
}

function archive () {
  // TODO: archive or unarchive emails
  // check if email is archived or not
  // PUT request to /emails/<email_id> to update archived property accordingly

  // loads user's inbox
  load_mailbox('inbox');
}

function reply () {
  // TODO: allow users to reply to an email
  // show compose-view, hide emails-view and email-view
  // pre-fill recipient field with sender of original email
  // if the original subject doens't starts with "Re: ":
  // pre-fill subject field with "Re: <original subject>"
  // pre-fill body with "On <timestamp>, <sender> wrote:"<original body>
}