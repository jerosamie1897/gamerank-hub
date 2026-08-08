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

const searchResults = document.querySelector("#search-results");
const searchSummary = document.querySelector("#search-summary");
const searchQuery = document.querySelector("#search-query");

if (searchResults && searchSummary && searchQuery) {
  const pages = [
    {
      title: "12 Best Free Games to Play in 2026",
      url: "best-free-games.html",
      description: "Compare free PC, console, and mobile games by genre, platform, session length, and monetization.",
      keywords: "free games multiplayer shooter strategy rpg pc console mobile fortnite valorant counter-strike rocket league warframe genshin apex legends league dota overwatch"
    },
    {
      title: "10 Best Browser Games Without Downloading",
      url: "browser-games.html",
      description: "Find multiplayer, puzzle, strategy, arcade, and mobile-friendly games that run in a browser.",
      keywords: "browser games no download multiplayer puzzle strategy arcade lichess skribbl slither shell shockers geoguessr board game arena"
    },
    {
      title: "Beginner Gaming Guide",
      url: "game-guides.html",
      description: "Improve settings, sensitivity, aim, movement, strategy, teamwork, performance, and practice habits.",
      keywords: "gaming guide beginner settings fps sensitivity aim movement strategy teamwork performance practice controls audio accessibility"
    },
    {
      title: "About GameRank Hub and Editorial Policy",
      url: "about.html",
      description: "Read how games are selected, reviewed, updated, corrected, and separated from commercial influence.",
      keywords: "about editorial policy methodology corrections disclosure ranking reviews contact"
    }
  ];

  const params = new URLSearchParams(window.location.search);
  const query = (params.get("q") || "").trim();
  searchQuery.value = query;

  if (!query) {
    searchSummary.textContent = "Enter a game, genre, platform, or gaming topic to search the site.";
  } else {
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
  }
}
