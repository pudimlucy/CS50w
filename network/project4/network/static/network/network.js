document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#all-posts').addEventListener('click', () => display_posts("all"));
    display_posts("all");
});

function display_posts(posts) {
    // Fetches filtered posts
    fetch('/posts/' + posts)
    .then(response => response.json())
    .then(posts => {
      // Creates an div for each post
      // TODO: edit, like and dislike buttons
      posts.forEach(post => {
        const div = document.createElement('div');
        div.innerHTML = `
        <div class="card-body border border-1" data-post_id="${post['id']}">
            <strong><h5 class="card-title">${post['author']}</h5></strong>
            <div class="card-text">${post['content']}
            <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
        </div>
      `;

        // Adds event listener to display post
        // div.addEventListener('click', () => display_post(post['id'], posts))
        document.querySelector('#view-posts').append(div);
      });
    });
}

// function display_post(post_id, posts) {
//     // TODO
// }
