document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  // TODO: event listener for clicking on email
  // TODO: event listener for clicking on archive/unarchive button
  // TODO: event listener for clicking on reply button
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
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

  // TODO: load appropriate mailbox's content
  // GET request to /emails/<mailbox>
  // display emails info in emails-view separating by divs
  // read -> gray background, unread -> white background
}

function send_email() {
  // TODO: sends email
  // get user's composition form
  // POST request to /emails

  // load user's sent mailbox
  load_mailbox('sent')
}

function view_email() {
  // TODO: display content of email when clicked
  // GET request to /emails/<email_id>
  // display sender, recipients, subject, timestamp and body on email-view
  // hide emails-view and compose-view, show email-view 
  // PUT request to /emails/<email_id> to update read property
}

function archive () {
  // TODO: archive or unarchive emails
  // check if email is archived or not
  // PUT request to /emails/<email_id> to update archived property accordingly

  // loads user's inbox
  load_mailbox('inbox')
}

function reply () {
  // TODO: allow users to reply to an email
  // show compose-view, hide emails-view and email-view
  // pre-fill recipient field with sender of original email
  // if the original subject doens't starts with "Re: ":
  // pre-fill subject field with "Re: <original subject>"
  // pre-fill body with "On <timestamp>, <sender> wrote:"<original body>
}