# GameRank Hub

A fast, dependency-free static gaming website built around sourced game-fit profiles and focused practical guides.

The library includes 30 sourced game profiles, practical guides, an editorial blog, an FAQ, original editorial illustrations, official privacy-enhanced video embeds, moderated comments, player ratings, dynamic recommendations, multilingual hubs, JSON-LD structured data, RSS, IndexNow, robots directives, and a sitemap.

## Preview

Open `index.html` directly, or run a local server from this folder:

```powershell
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Regenerate the content library

```powershell
python generate-content.py
python generate-locales.py
python generate-content.py
```

The generator rebuilds review, guide, blog, visual, search-index, sitemap, RSS, and content-report files. Run `python validate-site.py` afterward.

The community API requires PHP 8.3 with PDO SQLite. Its database and secrets belong outside the web root at `/var/lib/gamerankhub` and `/etc/gamerankhub`.

Production traffic reporting is available through `ops/traffic-report.py`. The Nginx virtual host should include `ops/nginx-cloudflare-real-ip.conf` when Cloudflare proxies the domain, then write a dedicated combined-format access log to `/var/log/nginx/gamerankhub.access.log`. The report counts visitors in memory without writing IP addresses to its JSON output.

## GitHub Pages deployment

The production canonical URL is:

`https://gamerankhub.com/`

After deployment, verify the URL in Google Search Console and submit:

`https://gamerankhub.com/sitemap.xml`

Game profiles must link their primary official source, show a checked date, distinguish sourced facts from editorial interpretation, and disclose when no hands-on testing was performed. Do not describe generated illustrations as screenshots or evidence of testing.

## Content requirements

Each new search page must have one primary intent, original analysis, accurate sourced platform information, a visible editorial owner, meaningful publication and checked dates, and an explicit limitation statement. Game list pages should explain selection criteria and include specific comparisons rather than generic category filler.

Do not publish thin pages only to target keyword variations or reuse paragraphs across nominally different articles. Organic rankings are not guaranteed; improve pages using Search Console query and engagement data rather than keyword stuffing, unsupported review schema, or artificial traffic.
