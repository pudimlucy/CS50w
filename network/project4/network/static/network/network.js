document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => display_all());
    if (window.location.pathname === "/") {
      display_all();
    } else if (window.location.pathname.substring(0, 9) === "/profile/") {
      display_user_posts(window.location.pathname.substring(9, ));
    } else if (window.location.pathname.substring(0, 11) === "/following/") {
      display_follow_posts(window.location.pathname.substring(11, ));
    }
});

function display_all() {

    // Fetches filtered posts
    fetch('/posts/all')
    .then(response => response.json())
    .then(posts => {
      // Creates an div for each post
      // TODO: edit, like and dislike buttons
      posts.forEach(post => {
        const div = document.createElement('div');
        div.innerHTML += `
        <div class="card-body border border-1" data-post_id="${post['id']}" id="${post['id']}">
            <strong><h5 class="card-title" href="user/${post['author']}">${post['author']}</h5></strong>
            <div class="card-text">${post['content']}
            <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
        </div>
      `;

        // Adds event listener to display post
        div.addEventListener('click', () => {
          fetch('/user/'+post['author'])
          .then(response => response.json())
          .then(user => {
            window.location.replace('/profile/'+user['username']);
          });
        })
        
        // Appends post to proper view
        document.querySelector('#view-all').append(div);
      });
    });
}

function display_user_posts(username) {
   
  // Fetches filtered posts
  fetch('/posts/'+username)
  .then(response => response.json())
  .then(posts => {
    // Creates an div for each post
    posts.forEach(post => {
      const div = document.createElement('div');
      div.innerHTML += `
      <div class="card-body border border-1" data-post_id="${post['id']}" id="${post['id']}">
          <strong><h5 class="card-title" href="user/${post['author']}">${post['author']}</h5></strong>
          <div class="card-text">${post['content']}</div>
          <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
      </div>
    `;

      // Adds event listener to display post
      div.addEventListener('click', () => {
        fetch('/user/'+post['author'])
        .then(response => response.json())
        .then(user => {
          window.location.replace('/profile/'+user['username']);
        });
      })
      
      // Appends post to proper view
      document.querySelector('#view-user').append(div);
    });
  });
}

// TODO: order by date
function display_follow_posts(username){
  fetch('/follows/'+username)
  .then(response => response.json())
  .then(posts => {
    posts.forEach(post => {
      const div = document.createElement('div');
      div.innerHTML += `
      <div class="card-body border border-1" data-post_id="${post['id']}" id="${post['id']}">
          <strong><h5 class="card-title" href="user/${post['author']}">${post['author']}</h5></strong>
          <div class="card-text">${post['content']}
          <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
      </div>
    `;

      // Adds event listener to display post
      div.addEventListener('click', () => {
        fetch('/user/'+post['author'])
        .then(response => response.json())
        .then(user => {
          window.location.replace('/profile/'+user['username']);
        });
      })
      
      // Appends post to proper view
      document.querySelector('#view-following').append(div);
    });
  });
}
