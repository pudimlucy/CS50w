document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#all-posts').addEventListener('click', () => display_posts("#view-all", "/posts"));
  if (window.location.pathname === "/") {
    display_posts("#view-all", "/posts");
  } else if (window.location.pathname.substring(0, 9) === "/profile/") {
    display_posts("#view-user", "/userposts/", (window.location.pathname.substring(9,)));
  } else if (window.location.pathname.substring(0, 11) === "/following/") {
    display_posts("#view-following", "/follows/", (window.location.pathname.substring(11,)));
  }
});

/**
 * Displays posts of a given page.
 *
 * @param   selector The selector specifying where the content must be appended.
 * @param   href The link from which the posts must be fetched.
 * @param   username Username for user-specific pages (following and profile).
 */
function display_posts(selector, href, username = "") {
  fetch(href + username)
    .then(response => response.json())
    .then(posts => {
      if (posts.length > 0) {
        pages = Math.ceil(posts.length / 10)
        create_nav(pages);
        create_pages(pages, selector);
        append_posts(posts);
      } else {
        document.querySelector("#message").innerHTML = `
        <div class="alert alert-warning" role="alert">
          No posts here yet!
        </div>`
      }
    });
}

/**
 * Appends a post to a selected element.
 *
 * @param   post  A JSON response containing the post's data: id, author, content and publication date.
 * @param   selector The selector specifying where the content must be appended.
 */
function append_posts(posts) {
  index = 0;
  posts.forEach(post => {
    page = Math.floor(index / 10) + 1;
    const div = create_post_div(post);
    add_user_redirect(div, post);

    // Appends post to proper selector
    document.querySelector("#page-view-" + page).append(div);
    index++;
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
  <div class="card-body border border-1 post" data-post_id="${post['id']}" id="${post['id']}">
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

function create_nav(pages) {
  document.querySelector("#navigation").innerHTML = `
  <ul class="pagination">
      <li class="page-item"><a class="page-link" id="previous">Previous</a></li>
      <div>
          <ul class="pagination" id="pagination">
          </ul>
      </div>
      <li class="page-item"><a class="page-link" id="next">Next</a></li>
  </ul>
  `
  for (let i = 1; i <= pages; i++) {
    const li = document.createElement("li");
    li.classList.add("page-item", "page-number");
    li.id = "page-" + i
    li.innerHTML = `
    <a class="page-link">${i}</a>
    `;
    document.querySelector("#pagination").append(li);
  }
  document.querySelector("#page-1").classList.add("active");

  document.querySelectorAll(".page-number").forEach(page => {
    page.addEventListener("click", () => {
      document.querySelector(".active").classList.remove("active");
      page.classList.add("active");
      document.querySelector(".page-view[style*='block']").style.display = "none";
      const num = page.id.substring(5);
      document.querySelector("#page-view-" + num).style.display = "block";
    });
  });

  document.querySelector("#previous").addEventListener("click", () => {
    const num = Number(document.querySelector(".active").id.substring(5)) - 1
    if (num >= 1) {
      document.querySelector(".active").classList.remove("active");
      document.querySelector("#page-" + num).classList.add("active");
      document.querySelector(".page-view[style*='block']").style.display = "none";
      document.querySelector("#page-view-" + num).style.display = "block";
    }
  });
  document.querySelector("#next").addEventListener("click", () => {
    const num = Number(document.querySelector(".active").id.substring(5)) + 1
    if (num <= document.querySelectorAll(".page-number").length) {
      document.querySelector(".active").classList.remove("active");
      document.querySelector("#page-" + num).classList.add("active");
      document.querySelector(".page-view[style*='block']").style.display = "none";
      document.querySelector("#page-view-" + num).style.display = "block";
    }
  });
}

function create_pages(pages, selector) {
  for (let i = 1; i <= pages; i++) {
    const div = document.createElement("div");
    div.style.display = "none";
    div.classList.add("page-view");
    div.id = "page-view-" + i
    document.querySelector(selector).append(div);
  }
  document.querySelector("#page-view-1").style.display = "block";
}
