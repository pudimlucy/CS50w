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
        nav_template(pages);
        page_buttons();
        move_buttons();
        create_pages(pages, selector);
        append_posts(posts);
      } else {
        document.querySelector("#message").innerHTML = `
        <div class="alert alert-warning" role="alert">
          No posts here yet!
        </div>`;
      }
    });
}

/**
 * Appends posts to pages.
 *
 * @param   posts  An iterable containing the JSON responses of posts to be appended.
 */
function append_posts(posts) {
  // Counts index 
  index = 0;
  posts.forEach(post => {
    // Defines page to append the post, given 10 posts per page
    page = Math.floor(index / 10) + 1;

    // Creates a div to post and adds an event listener to display user's profile
    const div = create_post_div(post);
    create_edit_button(div, post);
    add_user_redirect(div, post);

    // Appends post to proper page
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
  div.classList.add("card-body", "border", "border-1", "post");
  div.id = post["id"]
  div.innerHTML += `
  <strong><h5 class="card-title" href="/profile/${post['author']}">${post['author']}</h5></strong>
  <div class="card-text">${post['content']}
  <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
  `;
  
  return div;
}

/**
 * Adds an event listener to a post's title that redirects to author's profile.
 *
 * @param   div  A div containg the post template.
 * @param   post A JSON response containing the post's data: id, author, content and publication date.
 */
function add_user_redirect(div, post) {
  div.children[0].addEventListener('click', () => {
    window.location.replace('/profile/' + post['author']);
  })
}

/**
 * Creates pagination nav template.
 *
 * @param   pages  Quantity of pages.
 */
function nav_template(pages) {
  // Creates pagination container and previous/next buttons
  document.querySelector("#navigation").innerHTML = `
  <ul class="pagination">
      <li class="page-item"><a class="page-link" id="previous">Previous</a></li>
      <div>
          <ul class="pagination" id="pagination">
          </ul>
      </div>
      <li class="page-item"><a class="page-link" id="next">Next</a></li>
  </ul>
  `;

  // For each page, creates a page button
  for (let i = 1; i <= pages; i++) {
    const li = document.createElement("li");
    li.classList.add("page-item", "page-number");
    li.id = "page-" + i;
    li.innerHTML = `
    <a class="page-link">${i}</a>
    `;
    document.querySelector("#pagination").append(li);
  }
  document.querySelector("#page-1").classList.add("active");
}

/**
 * Adds event listeners to page buttons.
 */
function page_buttons() {
  document.querySelectorAll(".page-number").forEach(page => {
    page.addEventListener("click", () => {
      const num = page.id.substring(5);
      document.querySelector(".active").classList.remove("active");
      page.classList.add("active");
      document.querySelector(".page-view[style*='block']").style.display = "none";
      document.querySelector("#page-view-" + num).style.display = "block";
    });
  });
}

/**
 * Adds event listeners to previous and next buttons.
 */
function move_buttons() {
  const num = Number(document.querySelector(".active").id.substring(5));
  document.querySelector("#previous").addEventListener("click", () => {
    if (num - 1 >= 1) {
      hide_show_pages(num - 1);
    }
  });

  document.querySelector("#next").addEventListener("click", () => {
    if (num + 1 <= document.querySelectorAll(".page-number").length) {
      hide_show_pages(num + 1);
    }
  });
}

/**
 * Handles page display.
 * @param   num Number of the page to be displayed.
 */
function hide_show_pages(num) {
  document.querySelector(".active").classList.remove("active");
  document.querySelector("#page-" + num).classList.add("active");
  document.querySelector(".page-view[style*='block']").style.display = "none";
  document.querySelector("#page-view-" + num).style.display = "block";
}

/**
 * Creates page divs.
 * @param   pages Number of pages.
 * @param   selector View div to append pages.
 */
function create_pages(pages, selector) {
  for (let i = 1; i <= pages; i++) {
    const div = document.createElement("div");
    div.style.display = "none";
    div.classList.add("page-view");
    div.id = "page-view-" + i;
    document.querySelector(selector).append(div);
  }
  document.querySelector("#page-view-1").style.display = "block";
}

function create_edit_button(div, post) {
  fetch("/logged_user")
    .then(response => response.json())
    .then(user => {
      if (user) {
        if (user["username"] === post["author"]) {
          const button = document.createElement('button');
          button.type = "button";
          button.classList.add("btn", "btn-outline-info", "btn-sm");
          button.innerHTML = "Edit";
  
          button.addEventListener('click', () => edit_post(post, user));
          
          div.append(button);
        }
      }
    });
}

function edit_post(post, user) {
  // TODO: edit post assync.
}