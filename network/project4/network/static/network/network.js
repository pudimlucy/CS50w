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
        div.style.class = 'card mb-3';
        div.innerHTML = `
        <div class="card-body" data-post_id="${post['id']}"
            <h5 class="card-title">${post['author']}</h5>
            <div class="card-text">${post['content']}
            <h6 class="card-subtitle text-muted">${post['date']}</h6>
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
