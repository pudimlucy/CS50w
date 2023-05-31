document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#all-posts').addEventListener('click', () => display_all());
  if (window.location.pathname === "/") {
    display_posts(selector="#view-all", "/posts/all");
  } else if (window.location.pathname.substring(0, 9) === "/profile/") {
    display_posts("#view-user", "/posts/", (window.location.pathname.substring(9, )));
  } else if (window.location.pathname.substring(0, 11) === "/following/") {
    display_posts("#view-following", "/follows/", (window.location.pathname.substring(11, )));
  }
});

/**
 * Displays posts of a given page.
 *
 * @param   selector The selector specifying where the content must be appended.
 * @param   href The link from which the posts must be fetched.
 * @param   username Username for user-specific pages (following and profile).
 */
function display_posts(selector, href, username="") {
  fetch(href + username)
    .then(response => response.json())
    .then(posts => {
      append_posts(posts, selector);
    });
}

/**
 * Appends a post to a selected element.
 *
 * @param   post  A JSON response containing the post's data: id, author, content and publication date.
 * @param   selector The selector specifying where the content must be appended.
 */
function append_posts(posts, selector) {
  posts.forEach(post => {
    const div = create_post_div(post);
    add_user_redirect(div, post)

    // Appends post to proper selector
    document.querySelector(selector).append(div);
  });
}

// TODO: edit, like and dislike buttons
/**
 * Creates a post template.
 *
 * @param   post  A JSON response containing the post's data: id, author, content and publication date.
 * @returns A div containg the post template.
 */
function create_post_div(post) {
  const div = document.createElement('div');
  div.innerHTML += `
  <div class="card-body border border-1" data-post_id="${post['id']}" id="${post['id']}">
    <strong><h5 class="card-title" href="user/${post['author']}">${post['author']}</h5></strong>
    <div class="card-text">${post['content']}
    <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
  </div>
  `;
  return div
}

// TODO: specify event listener to trigger when click on USERNAME, not the div.
/**
 * Adds an event listener to a post that redirects to author's profile.
 *
 * @param   div  A div containg the post template.
 * @param   post A JSON response containing the post's data: id, author, content and publication date.
 */
function add_user_redirect(div, post) {
  div.addEventListener('click', () => {
    fetch('/user/' + post['author'])
      .then(response => response.json())
      .then(user => {
        window.location.replace('/profile/' + user['username']);
      });
  })
}
