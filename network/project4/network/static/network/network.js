document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => display_posts("all"));
    display_posts("all");
});

function display_posts(posts, author=null) {

    // Shows email view and hide other views
    if (author) {
      document.querySelector('#view-posts').style.display = 'none';
      document.querySelector('#view-posts').innerHTML = "";
      document.querySelector('#view-user').style.display = 'block';
      document.querySelector('#view-user').innerHTML = "";
      get_user(author);
    } else {
      document.querySelector('#view-user').style.display = 'none';
      document.querySelector('#view-user').innerHTML = "";
      document.querySelector('#view-posts').style.display = 'block';
      document.querySelector('#view-posts').innerHTML = "";
    }

    // Fetches filtered posts
    fetch('/posts/' + posts)
    .then(response => response.json())
    .then(posts => {
      // Creates an div for each post
      // TODO: edit, like and dislike buttons
      posts.forEach(post => {
        const div = document.createElement('div');
        // If user page, loads user info
        // if (author) {
        //   div.innerHTML = get_user(author);
        // }
        div.innerHTML += `
        <div class="card-body border border-1" data-post_id="${post['id']}" id="${post['id']}">
            <strong><h5 class="card-title">${post['author']}</h5></strong>
            <div class="card-text">${post['content']}
            <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
        </div>
      `;

        // Adds event listener to display post
        div.addEventListener('click', () => display_posts('user-'+post['author'], post['author']))

        // Appends post to proper view
        if (author) {
          document.querySelector('#view-user').append(div); 
        } else {
          document.querySelector('#view-posts').append(div);
        }
      });
    });
}

function get_user(username) {
  fetch('/user/' + username)
  .then(response => response.json())
  .then(user => {
    console.log(user);
  });
}
