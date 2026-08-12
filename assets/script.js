const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});

document.querySelectorAll(".site-footer .footer-bottom").forEach((footer) => {
  if (!footer.querySelector("[data-credit]")) {
    const credit = document.createElement("span");
    credit.dataset.credit = "";
    credit.textContent = "Designed & Developed by JTB";
    footer.append(credit);
  }
});

const searchResults = document.querySelector("#search-results");
const searchSummary = document.querySelector("#search-summary");
const searchQuery = document.querySelector("#search-query");

if (searchResults && searchSummary && searchQuery) {
  const params = new URLSearchParams(window.location.search);
  const query = (params.get("q") || "").trim();
  searchQuery.value = query;

  if (!query) {
    searchSummary.textContent = "Enter a game, genre, platform, or gaming topic to search the site.";
  } else {
    fetch("assets/search-index.json")
      .then((response) => {
        if (!response.ok) throw new Error(`Search index request failed with ${response.status}`);
        return response.json();
      })
      .then((pages) => {
    const stopWords = new Set(["a", "an", "and", "for", "in", "of", "on", "the", "to", "with"]);
    const normalizedQuery = query.toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, " ");
    const allTerms = normalizedQuery.split(/\s+/).filter(Boolean);
    const terms = allTerms.filter((term) => !stopWords.has(term));
    const effectiveTerms = terms.length ? terms : allTerms;
    const matches = pages
      .map((page) => {
        const title = page.title.toLowerCase();
        const searchable = `${title} ${page.description.toLowerCase()} ${page.keywords}`;
        const everyTermMatches = effectiveTerms.every((term) => searchable.includes(term));
        const score = effectiveTerms.reduce((total, term) => {
          if (!searchable.includes(term)) return total;
          return total + (title.includes(term) ? 3 : 1);
        }, searchable.includes(normalizedQuery) ? 5 : 0);
        if (!everyTermMatches) return { ...page, score: 0 };
        return { ...page, score };
      })
      .filter((page) => page.score > 0)
      .sort((a, b) => b.score - a.score);

    searchSummary.textContent = matches.length
      ? `${matches.length} result${matches.length === 1 ? "" : "s"} for “${query}”`
      : `No published GameRank Hub page matches “${query}”.`;

    matches.forEach((page) => {
      const article = document.createElement("article");
      article.className = "search-result";
      const heading = document.createElement("h2");
      const link = document.createElement("a");
      const description = document.createElement("p");
      link.href = page.url;
      link.textContent = page.title;
      description.textContent = page.description;
      heading.append(link);
      article.append(heading, description);
      searchResults.append(article);
    });

    if (!matches.length) {
      const worldwide = document.createElement("div");
      worldwide.className = "worldwide-search";
      const heading = document.createElement("h2");
      const description = document.createElement("p");
      const link = document.createElement("a");
      heading.textContent = "Search worldwide";
      description.textContent = `Find current web results, official pages, news, videos, and guides for “${query}”.`;
      link.className = "button button-primary";
      link.href = `https://www.google.com/search?q=${encodeURIComponent(`${query} game`)}`;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "Search Google worldwide";
      worldwide.append(heading, description, link);
      searchResults.append(worldwide);
    }
      })
      .catch(() => {
        searchSummary.textContent = "Search is temporarily unavailable. Browse the Reviews, Guides, and Blog sections instead.";
      });
  }
}

const reviewMatch = window.location.pathname.match(/\/reviews\/([a-z0-9-]+)\.html$/);

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function apiRequest(url, options = {}) {
  return fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  }).then(async (response) => {
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(payload.error || "The community service could not complete the request.");
    return payload;
  });
}

function renderRating(container, rating) {
  container.textContent = rating.count
    ? `${rating.average} out of 5 from ${rating.count} player rating${rating.count === 1 ? "" : "s"}`
    : "No player ratings yet.";
}

function renderComments(container, comments) {
  container.replaceChildren();
  if (!comments.length) {
    container.append(element("p", "community-empty", "No approved comments yet. Start the discussion."));
    return;
  }
  comments.forEach((comment) => {
    const article = element("article", "player-comment");
    const heading = element("h3", "", comment.display_name);
    const date = element("time", "", new Date(`${comment.created_at}Z`).toLocaleDateString());
    const body = element("p", "", comment.body);
    article.append(heading, date);
    if (comment.page_slug) {
      const game = element(
        "a",
        "comment-game",
        `Comment on ${comment.page_title || comment.page_slug.replaceAll("-", " ")}`
      );
      game.href = `/reviews/${comment.page_slug}.html#community`;
      article.append(game);
    }
    article.append(body);
    container.append(article);
  });
}

function renderRecommendations(container, recommendations) {
  container.replaceChildren();
  recommendations.forEach((recommendation) => {
    const article = element("article", "recommendation-card");
    const heading = element("h3");
    const link = element("a", "", recommendation.title);
    link.href = recommendation.url;
    heading.append(link);
    article.append(heading, element("p", "", recommendation.description));
    container.append(article);
  });
}

if (reviewMatch) {
  const articleBody = document.querySelector(".article-body");
  const relatedBox = articleBody?.querySelector(".related-box");
  if (articleBody && relatedBox) {
    const slug = reviewMatch[1];
    const section = element("section", "community-panel");
    section.id = "community";
    section.innerHTML = `
      <div class="community-intro">
        <p class="eyebrow">PLAYER COMMUNITY</p>
        <h2>Rate this game and join the discussion</h2>
        <p class="community-note">Share a rating instantly or send a useful comment for moderation.</p>
      </div>
      <div class="rating-panel">
        <div class="rating-copy">
          <span class="community-step">01 · RATE THE GAME</span>
          <strong>Player rating</strong>
          <p data-rating-summary>Loading ratings…</p>
        </div>
        <div class="rating-buttons" role="group" aria-label="Rate this game from 1 to 5"></div>
      </div>
      <div class="community-columns">
        <section class="comments-panel">
          <div class="community-section-heading">
            <span>02</span>
            <div><h3>Player comments</h3><p>Read approved experiences from other players.</p></div>
          </div>
          <div data-comment-list aria-live="polite"><p>Loading comments…</p></div>
        </section>
        <form class="comment-form" data-comment-form>
          <div class="community-section-heading">
            <span>03</span>
            <div><h3>Submit a comment</h3><p>Help players with a specific, respectful experience.</p></div>
          </div>
          <label><span>Display name</span><input name="name" maxlength="40" required autocomplete="nickname" placeholder="Your player name"></label>
          <label><span>Comment</span><textarea name="body" minlength="10" maxlength="1000" rows="5" required placeholder="What should other players know?"></textarea></label>
          <label class="honeypot" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
          <label class="consent-check"><input type="checkbox" required> I agree to the <a href="/community-guidelines.html">community guidelines</a> and understand the <a href="/privacy.html">privacy notice</a>.</label>
          <button class="button button-primary" type="submit">Send for moderation</button>
          <p class="form-status" data-comment-status role="status"></p>
        </form>
      </div>
      <div class="recommendations-panel">
        <h3>Recommended next reviews</h3>
        <div class="recommendation-grid" data-recommendations></div>
      </div>`;
    articleBody.insertBefore(section, relatedBox);

    const ratingSummary = section.querySelector("[data-rating-summary]");
    const ratingButtons = section.querySelector(".rating-buttons");
    const commentList = section.querySelector("[data-comment-list]");
    const commentForm = section.querySelector("[data-comment-form]");
    const commentStatus = section.querySelector("[data-comment-status]");
    const recommendations = section.querySelector("[data-recommendations]");
    let csrf = "";
    const startedAt = Math.floor(Date.now() / 1000);

    for (let score = 1; score <= 5; score += 1) {
      const button = element("button", "rating-button", `${score}★`);
      button.type = "button";
      button.setAttribute("aria-label", `Rate ${score} out of 5`);
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", () => {
        button.disabled = true;
        apiRequest("/api/community.php", {
          method: "POST",
          body: JSON.stringify({ action: "rate", page: slug, score, csrf })
        })
          .then((payload) => {
            renderRating(ratingSummary, payload.rating);
            ratingButtons.querySelectorAll(".rating-button").forEach((ratingButton) => {
              const selected = ratingButton === button;
              ratingButton.classList.toggle("selected", selected);
              ratingButton.setAttribute("aria-pressed", String(selected));
            });
          })
          .catch((error) => { ratingSummary.textContent = error.message; })
          .finally(() => { button.disabled = false; });
      });
      ratingButtons.append(button);
    }

    apiRequest(`/api/community.php?page=${encodeURIComponent(slug)}`)
      .then((payload) => {
        csrf = payload.csrf;
        renderRating(ratingSummary, payload.rating);
        renderComments(commentList, payload.comments);
        renderRecommendations(recommendations, payload.recommendations);
      })
      .catch((error) => {
        ratingSummary.textContent = error.message;
        commentList.replaceChildren(element("p", "community-empty", error.message));
      });

    commentForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(commentForm);
      const submit = commentForm.querySelector("button[type=submit]");
      submit.disabled = true;
      commentStatus.textContent = "Submitting…";
      apiRequest("/api/community.php", {
        method: "POST",
        body: JSON.stringify({
          action: "comment",
          page: slug,
          name: data.get("name"),
          body: data.get("body"),
          website: data.get("website"),
          startedAt,
          csrf
        })
      })
        .then((payload) => {
          commentForm.reset();
          commentStatus.textContent = payload.message;
        })
        .catch((error) => { commentStatus.textContent = error.message; })
        .finally(() => { submit.disabled = false; });
    });
  }
}

const communityOverview = document.querySelector("#community-overview");
if (communityOverview) {
  const comments = communityOverview.querySelector("[data-recent-comments]");
  const ratings = communityOverview.querySelector("[data-top-ratings]");
  const gameFilter = communityOverview.querySelector("[data-community-game-filter]");
  const filterSummary = communityOverview.querySelector("[data-community-filter-summary]");
  let allComments = [];
  let allRatings = [];

  function renderCommunityOverview() {
    const selectedGame = gameFilter.value;
    const visibleComments = selectedGame
      ? allComments.filter((comment) => comment.page_slug === selectedGame)
      : allComments;
    const visibleRatings = selectedGame
      ? allRatings.filter((rating) => rating.page_slug === selectedGame)
      : allRatings;
    const selectedTitle = gameFilter.options[gameFilter.selectedIndex].textContent;

    renderComments(comments, visibleComments);
    if (!visibleComments.length) {
      comments.replaceChildren(element(
        "p",
        "community-empty",
        selectedGame ? `No approved comments for ${selectedTitle} yet.` : "No approved comments yet."
      ));
    }

    ratings.replaceChildren();
    if (!visibleRatings.length) {
      ratings.append(element(
        "p",
        "community-empty",
        selectedGame ? `No ratings for ${selectedTitle} yet.` : "No ratings have been submitted yet."
      ));
    }
    visibleRatings.forEach((rating) => {
      const link = element("a", "rating-leader");
      link.href = `/reviews/${rating.page_slug}.html#community`;
      link.append(
        element("strong", "", rating.page_title || rating.page_slug.replaceAll("-", " ")),
        element("span", "", `${rating.average}★ · ${rating.count} rating${rating.count === 1 ? "" : "s"}`)
      );
      ratings.append(link);
    });

    filterSummary.textContent = selectedGame
      ? `Showing community activity for ${selectedTitle}.`
      : "Showing community activity for all games.";
  }

  apiRequest("/api/community.php?overview=1")
    .then((payload) => {
      allComments = payload.recentComments;
      allRatings = payload.topRated;
      const games = new Map();
      [...allComments, ...allRatings].forEach((item) => {
        games.set(item.page_slug, item.page_title || item.page_slug.replaceAll("-", " "));
      });
      [...games.entries()]
        .sort((a, b) => a[1].localeCompare(b[1]))
        .forEach(([slug, title]) => {
          const option = element("option", "", title);
          option.value = slug;
          gameFilter.append(option);
        });
      renderCommunityOverview();
    })
    .catch((error) => {
      communityOverview.querySelector("[data-community-status]").textContent = error.message;
    });

  gameFilter.addEventListener("change", () => {
    renderCommunityOverview();
  });
}
