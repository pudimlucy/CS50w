function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#all-posts').addEventListener('click', () => displayPosts("#view-all", "/posts"));
  if (window.location.pathname === "/") {
    displayPosts("#view-all", "/posts");
  } else if (window.location.pathname.substring(0, 9) === "/profile/") {
    displayPosts("#view-user", "/userposts/", (window.location.pathname.substring(9,)));
  } else if (window.location.pathname.substring(0, 11) === "/following/") {
    displayPosts("#view-following", "/follows/", (window.location.pathname.substring(11,)));
  }
});

/**
 * Displays posts of a given page.
 *
 * @param   selector The selector specifying where the content must be appended.
 * @param   href The link from which the posts must be fetched.
 * @param   username Username for user-specific pages (following and profile).
 */
function displayPosts(selector, href, username = "") {
  fetch(href + username)
    .then(response => response.json())
    .then(posts => {
      if (posts.length > 0) {
        pages = Math.ceil(posts.length / 10)
        navTemplate(pages);
        pageButtons();
        moveButtons();
        createPages(pages, selector);
        appendPosts(posts);
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
function appendPosts(posts) {
  let user;
  fetch("/logged_user")
    .then(response => response.json())
    .then(user => {
      user = user
    });
  // Counts index 
  index = 0;
  posts.forEach(post => {
    // Defines page to append the post, given 10 posts per page
    page = Math.floor(index / 10) + 1;

    // Creates a div to post 
    const div = createPostDiv(post);
    createEditButton(div, post);
    createInteract(div, post);

    // Adds an event listener to display user's profile
    div.children[0].addEventListener('click', () => {
      window.location.replace('/profile/' + post['author']);
    })

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
function createPostDiv(post) {
  let div;
  if (document.getElementById(post["id"]) === null) {
    div = document.createElement('div');
    div.classList.add("card-body", "border", "border-1", "post");
    div.id = post["id"]
  } else {
    div = document.getElementById(post["id"]);
  }
  div.innerHTML += `
  <strong><h5 class="card-title" href="/profile/${post['author']}">${post['author']}</h5></strong>
  <div class="card-text">${post['content']}</div class="card-text">
  <div class="interact"></div>
  <em><h6 class="card-subtitle text-muted">${post['date']}</h6></em>
  `;

  return div;
}

/**
 * Creates pagination nav template.
 *
 * @param   pages  Quantity of pages.
 */
function navTemplate(pages) {
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
function pageButtons() {
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
function moveButtons() {
  const num = Number(document.querySelector(".active").id.substring(5));

  document.querySelector("#previous").addEventListener("click", () => {
    if (num - 1 >= 1) {
      filterPages(num - 1);
    }
  });
  document.querySelector("#next").addEventListener("click", () => {
    if (num + 1 <= document.querySelectorAll(".page-number").length) {
      filterPages(num + 1);
    }
  });
}

/**
 * Handles page display.
 * @param   num Number of the page to be displayed.
 */
function filterPages(num) {
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
function createPages(pages, selector) {
  for (let i = 1; i <= pages; i++) {
    const div = document.createElement("div");
    div.style.display = "none";
    div.classList.add("page-view");
    div.id = "page-view-" + i;
    document.querySelector(selector).append(div);
  }
  document.querySelector("#page-view-1").style.display = "block";
}

function createEditButton(div, post) {
  fetch("/logged_user")
    .then(response => response.json())
    .then(user => {
      if (user) {
        if (user["username"] === post["author"]) {
          const button = document.createElement('button');
          button.type = "button";
          button.classList.add("btn", "btn-outline-info", "btn-sm");
          button.innerHTML = "Edit";

          button.addEventListener('click', () => eventEdit(post, button));

          div.append(button);
        }
      }
    });
}

function eventEdit(post, button) {
  const template = document.getElementById(post["id"]).children[1];
  if (button.innerHTML === "Edit") {
    template.innerHTML = `
    <textarea class="editor" rows="3">${template.innerHTML}</textarea>
    <p></p>
    `;
    button.innerHTML = `Save`;
  } 
  else if (button.innerHTML === "Save") {
    const content = document.getElementById(post["id"]).children[1].querySelector('.editor').value;
    fetch('/edit_post/' + post["id"], {
      method: "PUT",
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin',
      body: JSON.stringify({
        'content': content,
      }),
    })
    .then(() => {
      template.innerHTML = content;
      button.innerHTML = `Edit`;
    });
  }
}

function createInteract(div, post) {
  const interact = div.children[2];
  const types = ['likes', 'dislikes'];
  let button = undefined;
  for (let i = 0; i < types.length; i++) {
    button = document.createElement('button');
    button.type = "button";
    button.classList.add("btn", "btn-sm", "btn-outline-info");
    button.style.borderColor = 'transparent';
    button.innerHTML = post[types[i]] + `  <i class="bi bi-hand-thumbs-` + ((i === 0) ? `up"></i>` : `down"></i>`);
    interact.append(button)
  }
  eventInteract(div, post);
}

function eventInteract(div, post) {
  const interact = div.children[2];
  const types = ['like', 'dislike'];
  for (let i = 0; i < types.length; i++) {
    interact.children[i].addEventListener('click', () => {
      fetch('/interact', {
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
          'id': post['id'],
          'type': types[i],
        }),
      })
        .then(response => response.json())
        .then(update => {
          updateInteract(update, div);
        });
    });
  }
}

function updateInteract(update, div) {
  const interact = div.children[2];
  const types = ['likes', 'dislikes'];
  for (let i = 0; i < types.length; i++) {
    interact.children[i].innerHTML = `
    ${update[types[i]]}
    `;
    icon = `<i class="bi bi-hand-thumbs-` + ((types[i] === "likes") ? `up"></i>` : `down"></i>`);
    interact.children[i].innerHTML += icon;
  }
}
