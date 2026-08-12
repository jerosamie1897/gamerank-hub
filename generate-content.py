from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
BASE_URL = "https://gamerankhub.com"
TODAY = date(2026, 8, 12)
TODAY_STR = str(TODAY)
RFC822_DATE = "Wed, 12 Aug 2026 00:00:00 GMT"
SITE_AUTHOR = "GameRank Hub Editorial Team"
STYLES_VERSION = "20260812-5"
SCRIPT_VERSION = "20260812-6"
STATIC_LASTMOD = "2026-08-11"
MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def words(value: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", re.sub(r"<[^>]+>", " ", value)))


def friendly_date(value: date) -> str:
    return f"{MONTH_NAMES[value.month - 1]} {value.day}, {value.year}"


def assert_unique_strings(name: str, items: tuple[str, ...]) -> None:
    if len(set(items)) != len(items):
        raise ValueError(f"{name} must not contain duplicates: {items}")


def trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    shortened = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return shortened + "…"


@dataclass(frozen=True)
class SourceRef:
    label: str
    url: str


@dataclass(frozen=True)
class NamedText:
    title: str
    text: str


@dataclass(frozen=True)
class BlogSection:
    heading: str
    paragraphs: tuple[str, ...]
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class PageMeta:
    title: str
    url: str
    canonical_path: str
    description: str
    keywords: str
    kind: str
    published: str = ""
    checked: str = ""


@dataclass(frozen=True)
class GameProfile:
    slug: str
    name: str
    genre: str
    official_url: str
    platforms: tuple[str, ...]
    platform_tags: tuple[str, ...]
    business_model: str
    session_length: str
    session_bucket: str
    play_style: str
    hub_group: str
    core_loop: str
    best_for: str
    not_for: str
    learning_barrier: str
    social_shape: str
    progression_notes: str
    spending_notes: str
    first_session_plan: tuple[str, ...]
    fit_questions: tuple[str, ...]
    source_label: str
    source_url: str
    checked_date: date
    title: str
    description: str
    summary: str
    onboarding_notes: str
    commitment_notes: str
    what_can_change: tuple[str, ...]
    review_hub_summary: str
    related_guides: tuple[str, ...]
    visual_points: tuple[str, str, str]

    def __post_init__(self) -> None:
        assert_unique_strings(f"{self.slug}.first_session_plan", self.first_session_plan)
        assert_unique_strings(f"{self.slug}.fit_questions", self.fit_questions)
        assert_unique_strings(f"{self.slug}.what_can_change", self.what_can_change)
        if len(self.visual_points) != 3:
            raise ValueError(f"{self.slug}.visual_points must contain exactly three items")


@dataclass(frozen=True)
class GuideItem:
    slug: str
    title: str
    category: str
    summary: str
    description: str
    quick_answer: str
    introduction: tuple[str, ...]
    checklist: tuple[str, ...]
    checklist_note: str
    scenario_title: str
    scenario: tuple[str, ...]
    steps: tuple[NamedText, ...]
    follow_through: str
    mistakes: tuple[NamedText, ...]
    success_criteria: tuple[str, ...]
    success_note: str
    source_keys: tuple[str, ...]
    extra_sources: tuple[SourceRef, ...] = ()
    limitations: tuple[str, ...] = ()
    visual_points: tuple[str, str, str] = ("", "", "")

    def __post_init__(self) -> None:
        assert_unique_strings(f"{self.slug}.checklist", self.checklist)
        assert_unique_strings(f"{self.slug}.success_criteria", self.success_criteria)
        assert_unique_strings(f"{self.slug}.limitations", self.limitations)
        if len(self.visual_points) != 3:
            raise ValueError(f"{self.slug}.visual_points must contain exactly three items")


@dataclass(frozen=True)
class BlogPost:
    slug: str
    title: str
    category: str
    summary: str
    description: str
    intro: tuple[str, ...]
    sections: tuple[BlogSection, ...]
    takeaways: tuple[str, ...]
    conclusion: str
    source_keys: tuple[str, ...]
    extra_sources: tuple[SourceRef, ...] = ()
    limitations: tuple[str, ...] = ()
    visual_points: tuple[str, str, str] = ("", "", "")

    def __post_init__(self) -> None:
        assert_unique_strings(f"{self.slug}.takeaways", self.takeaways)
        assert_unique_strings(f"{self.slug}.limitations", self.limitations)
        if len(self.visual_points) != 3:
            raise ValueError(f"{self.slug}.visual_points must contain exactly three items")


def note(title: str, text: str) -> NamedText:
    return NamedText(title, text)


def section_block(heading: str, *paragraphs: str, bullets: tuple[str, ...] = ()) -> BlogSection:
    return BlogSection(heading=heading, paragraphs=paragraphs, bullets=bullets)


def game(**kwargs) -> GameProfile:
    return GameProfile(checked_date=TODAY, **kwargs)


def guide(**kwargs) -> GuideItem:
    return GuideItem(**kwargs)


def blog(**kwargs) -> BlogPost:
    return BlogPost(**kwargs)


SOURCE_PACKS: dict[str, tuple[SourceRef, ...]] = {
    "controls": (
        SourceRef("Xbox support", "https://support.xbox.com/"),
        SourceRef("PlayStation support", "https://www.playstation.com/support/"),
        SourceRef("Steam Support", "https://help.steampowered.com/"),
    ),
    "performance": (
        SourceRef("Microsoft Windows support", "https://support.microsoft.com/windows"),
        SourceRef("NVIDIA Reflex overview", "https://www.nvidia.com/en-us/geforce/technologies/reflex/"),
        SourceRef("AMD software support", "https://www.amd.com/en/products/software/adrenalin.html"),
    ),
    "teamwork": (
        SourceRef("Xbox multiplayer support", "https://support.xbox.com/"),
        SourceRef("PlayStation multiplayer support", "https://www.playstation.com/support/"),
        SourceRef("Discord Safety Center", "https://discord.com/safety"),
    ),
    "safety": (
        SourceRef("Epic Games parental controls", "https://www.epicgames.com/site/en-US/parental-controls"),
        SourceRef("Xbox Family Safety", "https://support.xbox.com/help/family-online-safety"),
        SourceRef("PlayStation family management", "https://www.playstation.com/support/account/playstation-family-account-set-up/"),
    ),
    "setup": (
        SourceRef("Steam Support", "https://help.steampowered.com/"),
        SourceRef("Epic Games support", "https://www.epicgames.com/help/"),
        SourceRef("Xbox network support", "https://support.xbox.com/"),
    ),
    "cloud": (
        SourceRef("Xbox Cloud Gaming support", "https://support.xbox.com/help/games-apps/cloud-gaming/about-cloud-gaming"),
        SourceRef("NVIDIA GeForce NOW", "https://www.nvidia.com/en-us/geforce-now/"),
        SourceRef("Amazon Luna", "https://luna.amazon.com/"),
    ),
    "browser": (
        SourceRef("Google Chrome Help", "https://support.google.com/chrome/"),
        SourceRef("Microsoft Edge support", "https://support.microsoft.com/microsoft-edge"),
        SourceRef("Mozilla Support", "https://support.mozilla.org/"),
    ),
    "wellbeing": (
        SourceRef("Microsoft accessibility", "https://www.microsoft.com/accessibility"),
        SourceRef("PlayStation accessibility", "https://www.playstation.com/en-us/accessibility/"),
        SourceRef("Nintendo support", "https://www.nintendo.com/us/support/"),
    ),
    "editorial": (
        SourceRef("GameRank Hub editorial policy", f"{BASE_URL}/about.html"),
        SourceRef("Google helpful content guidance", "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"),
        SourceRef("Schema.org", "https://schema.org/"),
    ),
}


GAMES: list[GameProfile] = []
GUIDES: list[GuideItem] = []
BLOG_POSTS: list[BlogPost] = []


GAMES.extend(
    [
        game(
            slug="fortnite",
            name="Fortnite",
            genre="Battle royale / creator platform",
            official_url="https://www.fortnite.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch", "Supported mobile options"),
            platform_tags=("pc", "playstation", "xbox", "switch", "mobile"),
            business_model="Free-to-play live service with cosmetic spending and battle passes.",
            session_length="10-25 minute matches, plus extra creator-mode time if you want it.",
            session_bucket="short",
            play_style="social squad shooter",
            hub_group="competitive",
            core_loop="Drop in, gather weapons, survive the storm, and decide when to fight, rotate, or disengage.",
            best_for="friends who want one free game that can flip between battle royale, social events, and creator-made modes",
            not_for="players who want a quiet interface, a fixed meta, or a very serious one-mode shooter",
            learning_barrier="Zero Build is approachable quickly, but the broader Fortnite ecosystem can still feel noisy and fast-changing.",
            social_shape="Fortnite works solo, but its flexibility and event cadence land better when you have a duo or squad to return with.",
            progression_notes="Season quests and battle-pass goals create short-term direction, yet the reward track resets with each season.",
            spending_notes="Core play is free. Spending is mostly cosmetic, but the shop and pass structure reward people who check in often.",
            first_session_plan=(
                "Start in Zero Build before deciding whether the wider Fortnite ecosystem is for you.",
                "Check cross-play, subtitle, visual-audio, and input settings before the second match.",
                "Use one reliable drop route for several games instead of sampling the whole island at once.",
                "Ignore creator islands and the store until the basic loop of looting, rotating, and surviving feels fun.",
            ),
            fit_questions=(
                "Do you want one launcher that can double as a recurring social hangout?",
                "Will constant seasonal events feel energizing or exhausting after a month?",
                "Can you enjoy the game without treating every cosmetic or quest as mandatory?",
            ),
            source_label="Official download and mode overview",
            source_url="https://www.fortnite.com/download",
            title="Fortnite Before You Play: A Fit Guide for Social Squads and Zero-Build Newcomers",
            description="Use this sourced Fortnite fit profile to decide if its short sessions, squad focus, seasonal churn, and cosmetic economy match what you want.",
            summary="Fortnite fits players who want short social sessions and a rotating mix of battle royale, creator islands, and seasonal goals.",
            onboarding_notes="The first question is not whether Fortnite is universally good. It is whether you want an all-purpose game space that changes constantly. Starting in Zero Build and ignoring side modes for a few sessions makes the fit clearer much faster.",
            commitment_notes="You can keep Fortnite casual, but the seasonal reward structure works best for people who are comfortable letting some limited-time cosmetics pass by.",
            what_can_change=(
                "Seasonal loot pools and limited-time playlists move regularly.",
                "Collaboration events and quest structures can reshape what the game foregrounds.",
                "Supported mobile or cloud access options can vary by store or region.",
            ),
            review_hub_summary="Best for short squad sessions and constant novelty; weaker if you want one stable competitive routine.",
            related_guides=("crossplay-guide", "free-to-play-spending"),
            visual_points=("10-25 min", "Solo or squads", "Cosmetics + pass"),
        ),
        game(
            slug="valorant",
            name="VALORANT",
            genre="Tactical hero shooter",
            official_url="https://playvalorant.com/",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-to-play competitive shooter with cosmetic bundles and battle passes.",
            session_length="30-50 minute matches with a real time block for queueing and focus.",
            session_bucket="medium",
            play_style="round-based tactical shooter",
            hub_group="competitive",
            core_loop="Win structured rounds by combining precise gunplay, map control, economy decisions, and agent utility.",
            best_for="players who like patient round tension and are willing to improve with a regular small agent pool",
            not_for="players who want casual drop-in chaos or dislike communication-heavy team shooters",
            learning_barrier="Basic objectives are easy to read, but recoil control, timing, and map vocabulary matter early.",
            social_shape="Solo queue works, yet the game improves when you can communicate calmly or queue with at least one friend.",
            progression_notes="The durable progression is player skill and agent familiarity more than account power.",
            spending_notes="Competitive access is free. Monetization is centered on premium skins, bundles, and seasonal cosmetics.",
            first_session_plan=(
                "Finish the tutorial and spend a few minutes in the range before touching matchmade modes.",
                "Pick one straightforward agent and learn what your utility is supposed to do in plain language.",
                "Play unrated while focusing on crosshair placement and sound cues instead of highlight plays.",
                "Learn two useful callouts per map rather than trying to memorize everything immediately.",
            ),
            fit_questions=(
                "Do you enjoy long rounds where a single mistake can matter?",
                "Are you happy specializing in a small agent pool for a while?",
                "Can you accept practice time before ranked begins to feel comfortable?",
            ),
            source_label="Official how-to-play overview",
            source_url="https://playvalorant.com/en-us/how-to-play/",
            title="VALORANT Before You Play: Is It a Fit for Patient Team Shooters?",
            description="This sourced VALORANT fit profile helps you weigh long matches, agent roles, communication needs, and cosmetic-only monetization before you commit.",
            summary="VALORANT fits players who enjoy deliberate team rounds and do not mind a slower path to competence.",
            onboarding_notes="VALORANT asks whether you enjoy the tension between short bursts of action and longer stretches of setup, sound reading, and angle discipline. If that sounds appealing, the game rewards study. If not, the downtime can feel punishing.",
            commitment_notes="A single match already needs a real chunk of time, and improvement usually means accepting slow repetition instead of looking for instant momentum.",
            what_can_change=(
                "Map pools and mode availability can rotate between acts.",
                "Agent balance and role expectations shift with live patches.",
                "Skin bundles and battle-pass offerings change on a seasonal cadence.",
            ),
            review_hub_summary="A strong fit for patient competitive players who want readable objectives and a long skill runway.",
            related_guides=("choose-gaming-sensitivity", "clear-team-communication"),
            visual_points=("30-50 min", "Team comms", "Cosmetic shop"),
        ),
        game(
            slug="counter-strike-2",
            name="Counter-Strike 2",
            genre="Tactical shooter",
            official_url="https://www.counter-strike.net/cs2",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free-to-play tactical shooter with cosmetic market and case-driven spending.",
            session_length="30-45 minute matches once you include full rounds and queue time.",
            session_bucket="medium",
            play_style="classic tactical shooter",
            hub_group="competitive",
            core_loop="Manage money, control space, trade cleanly, and use utility well enough to win bomb-plant rounds.",
            best_for="PC players who want classic tactical shooting and almost endless room to refine fundamentals",
            not_for="anyone who wants forgiving recoil, heavy class variety, or short low-stakes sessions",
            learning_barrier="Counter-Strike 2 is mechanically simple to read and still very demanding to execute well.",
            social_shape="You can queue solo, but the game shines with a duo or team that can trade and call without panic.",
            progression_notes="There is very little account-driven progression; the reward loop is mostly skill growth, rank, and cosmetics.",
            spending_notes="Core play is free. Spending is mostly cosmetic, though the market layer can become a hobby of its own.",
            first_session_plan=(
                "Use Deathmatch or casual play to learn recoil feel before asking ranked to teach you everything.",
                "Learn one map's bombsites, rotate routes, and two common angles per side.",
                "Stick to a narrow buy routine so economy decisions do not overload your early rounds.",
                "Focus on trading with teammates instead of trying to carry fights alone.",
            ),
            fit_questions=(
                "Do you want skill expression without class abilities or hero kits?",
                "Are you willing to learn maps slowly rather than rely on reaction speed alone?",
                "Will minimal account progression feel refreshingly clean or emotionally flat?",
            ),
            source_label="Official Steam store page",
            source_url="https://store.steampowered.com/app/730/CounterStrike_2/",
            title="Counter-Strike 2 Before You Play: A Fit Guide for Competitive PC Players",
            description="Read this sourced Counter-Strike 2 fit profile before you commit to its PC-only ladder, map learning curve, and cosmetic-market business model.",
            summary="Counter-Strike 2 fits players who want stripped-down tactical depth and do not need unlock-heavy progression to stay interested.",
            onboarding_notes="If you want a bare-bones ruleset where tiny positioning and utility errors matter, CS2 still delivers. If you need class variety or constant unlocks, it can feel almost austere.",
            commitment_notes="Even before you care about rank, learning the map pool and economy rhythm asks for repeated, focused sessions.",
            what_can_change=(
                "Premier rules, maps, and matchmaking priorities can shift over time.",
                "Weapon balance and utility timings move with competitive patches.",
                "Storefront and cosmetic market conditions are separate from the gameplay fit described here.",
            ),
            review_hub_summary="A strong fit for players who want depth from clean fundamentals rather than classes, loadouts, or endless unlocks.",
            related_guides=("choose-gaming-sensitivity", "optimize-fps-settings"),
            visual_points=("30-45 min", "Duo helps", "Cosmetic market"),
        ),
    ]
)
GAME_ORDER = [
    "fortnite",
    "valorant",
    "counter-strike-2",
    "apex-legends",
    "warframe",
    "genshin-impact",
    "rocket-league",
    "league-of-legends",
    "dota-2",
    "overwatch-2",
    "destiny-2",
    "path-of-exile",
    "roblox",
    "fall-guys",
    "halo-infinite",
    "the-finals",
    "marvel-rivals",
    "pubg-battlegrounds",
    "hearthstone",
    "teamfight-tactics",
    "brawlhalla",
    "efootball",
    "trackmania",
    "the-sims-4",
    "guild-wars-2",
    "lost-ark",
    "runescape",
    "eve-online",
    "dauntless",
    "world-of-tanks",
]

GUIDE_ORDER = [
    "choose-gaming-sensitivity",
    "improve-aim-without-grinding",
    "optimize-fps-settings",
    "reduce-input-lag",
    "multiplayer-beginner-checklist",
    "clear-team-communication",
    "controller-settings-guide",
    "keyboard-mouse-basics",
    "free-to-play-spending",
    "family-gaming-safety",
    "crossplay-guide",
    "cloud-gaming-guide",
    "browser-game-performance",
    "healthy-gaming-setup",
    "how-we-review-games",
]

BLOG_ORDER = [
    "how-we-update-rankings",
    "best-game-for-short-sessions",
    "what-makes-a-good-free-game",
    "before-you-download-a-new-game",
]

GAME_BY_SLUG: dict[str, GameProfile] = {}
GUIDE_BY_SLUG: dict[str, GuideItem] = {}
BLOG_BY_SLUG: dict[str, BlogPost] = {}


def canonical_url(path: str) -> str:
    return f"{BASE_URL}/{path}" if path else f"{BASE_URL}/"


def collect_sources(keys: tuple[str, ...], extras: tuple[SourceRef, ...] = ()) -> tuple[SourceRef, ...]:
    seen: set[tuple[str, str]] = set()
    collected: list[SourceRef] = []
    for key in keys:
        for source in SOURCE_PACKS[key]:
            pair = (source.label, source.url)
            if pair not in seen:
                seen.add(pair)
                collected.append(source)
    for source in extras:
        pair = (source.label, source.url)
        if pair not in seen:
            seen.add(pair)
            collected.append(source)
    return tuple(collected)


def join_platforms(platforms: tuple[str, ...]) -> str:
    return ", ".join(platforms)


def render_feature_list(items: tuple[str, ...]) -> str:
    return "<ul class=\"feature-list\">" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_step_list(items: tuple[str, ...]) -> str:
    return "<ol class=\"step-list\">" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ol>"


def render_plain_list(items: tuple[str, ...], class_name: str = "step-list") -> str:
    return f"<ul class=\"{class_name}\">" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_source_list(items: tuple[SourceRef, ...]) -> str:
    return "<ul class=\"step-list\">" + "".join(
        f'<li><a href="{esc(item.url)}">{esc(item.label)}</a></li>' for item in items
    ) + "</ul>"


def render_named_cards(items: tuple[NamedText, ...], label: str) -> str:
    return "<div class=\"guide-cards\">" + "".join(
        f"<article><span>{esc(label)} {index}</span><h3>{esc(item.title)}</h3><p>{esc(item.text)}</p></article>"
        for index, item in enumerate(items, 1)
    ) + "</div>"


def build_visual_svg(title: str, subtitle: str, accent: str, chips: tuple[str, str, str]) -> str:
    chip_markup = []
    for y, chip in zip((182, 230, 278), chips):
        chip_markup.append(
            f'<rect x="70" y="{y-20}" width="500" height="36" rx="18" fill="#ffffff" opacity=".92"/>'
            f'<text x="95" y="{y+4}" fill="#161326" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="700">{esc(trim(chip, 44))}</text>'
        )
    chip_block = "".join(chip_markup)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360" role="img" '
        'aria-labelledby="title desc">'
        f'<title id="title">{esc(title)} editorial illustration</title>'
        f'<desc id="desc">{esc(subtitle)}</desc>'
        '<rect width="640" height="360" rx="24" fill="#151225"/>'
        f'<rect x="30" y="30" width="580" height="300" rx="20" fill="{accent}" opacity=".24"/>'
        '<circle cx="520" cy="88" r="62" fill="#c8f56a" opacity=".88"/>'
        '<path d="M82 120 C140 70 250 62 338 108" fill="none" stroke="#ffffff" stroke-width="14" stroke-linecap="round" opacity=".86"/>'
        f'<text x="70" y="94" fill="#ffffff" font-family="Segoe UI,Arial,sans-serif" font-size="24" font-weight="800">{esc(trim(title, 34))}</text>'
        f'<text x="70" y="128" fill="#ddd7ef" font-family="Segoe UI,Arial,sans-serif" font-size="16">{esc(trim(subtitle, 58))}</text>'
        f"{chip_block}"
        '<text x="70" y="324" fill="#ffffff" font-family="Segoe UI,Arial,sans-serif" font-size="12">EDITORIAL ILLUSTRATION · NOT GAMEPLAY FOOTAGE</text>'
        "</svg>"
    )


def visual_figure(prefix: str, image_path: str, alt: str, caption: str) -> str:
    return (
        '<div class="visual-grid"><figure>'
        f'<img src="{prefix}{image_path}" alt="{esc(alt)}" width="640" height="360">'
        f"<figcaption>{esc(caption)}</figcaption>"
        "</figure></div>"
    )


def breadcrumbs(items: list[tuple[str, str | None]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                **({"item": canonical_url(path)} if path is not None else {}),
            }
            for index, (name, path) in enumerate(items, 1)
        ],
    }


def nav(prefix: str = "", active: str = "") -> str:
    links = [
        ("Home", "index.html", "home"),
        ("Game Profiles", "reviews/index.html", "reviews"),
        ("Guides", "guides/index.html", "guides"),
        ("Blog", "blog/index.html", "blog"),
        ("Community", "community.html", "community"),
        ("FAQ", "faq.html", "faq"),
    ]
    rendered = "".join(
        f'<a{" class=active" if key == active else ""} href="{prefix}{href}">{label}</a>'
        for label, href, key in links
    )
    return f"""
  <header class="site-header">
    <div class="shell nav-wrap">
      <a class="brand" href="{prefix}index.html" aria-label="GameRank Hub home"><span class="brand-mark" aria-hidden="true">G</span><span>GameRank <strong>Hub</strong></span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="sr-only">Toggle navigation</span><span></span><span></span><span></span></button>
      <nav id="site-nav" class="site-nav" aria-label="Primary navigation">{rendered}
        <form class="site-search" action="{prefix}search.html" method="get" role="search"><label class="sr-only" for="nav-search">Search GameRank Hub</label><input id="nav-search" name="q" type="search" placeholder="Search" required><button type="submit">Search</button></form>
      </nav>
    </div>
  </header>"""


def footer(prefix: str = "") -> str:
    return f"""
  <footer class="site-footer">
    <div class="shell footer-grid">
      <div><a class="brand footer-brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true">G</span><span>GameRank <strong>Hub</strong></span></a><p>Sourced game-fit profiles, practical guides, and player-first editorial notes.</p></div>
      <div><h2>Explore</h2><a href="{prefix}reviews/index.html">Game fit profiles</a><a href="{prefix}guides/index.html">Player guides</a><a href="{prefix}blog/index.html">Editorial blog</a></div>
      <div><h2>About</h2><a href="{prefix}community.html">Community</a><a href="{prefix}updates.html">Update log</a><a href="{prefix}faq.html">FAQ</a><a href="{prefix}about.html">Editorial policy</a><a href="{prefix}feed.xml">RSS feed</a></div>
    </div>
    <div class="shell footer-bottom"><span>© <span data-year>2026</span> GameRank Hub</span><span>Built for players, not algorithms.</span><span data-credit>Designed &amp; Developed by JTB</span></div>
  </footer>
  <script src="{prefix}assets/script.js?v={SCRIPT_VERSION}" defer></script>"""


def head(
    title: str,
    description: str,
    canonical_path: str,
    schema: dict,
    prefix: str = "",
    og_type: str = "article",
    image_path: str = "assets/editorial-cover.svg",
    image_alt: str = "GameRank Hub editorial illustration",
    published: str = TODAY_STR,
    modified: str = TODAY_STR,
) -> str:
    canonical = canonical_url(canonical_path)
    image = canonical_url(image_path)
    article_tags = (
        f'\n  <meta property="article:published_time" content="{published}">'
        f'\n  <meta property="article:modified_time" content="{modified}">'
        if published
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="author" content="{esc(SITE_AUTHOR)}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="alternate" type="application/rss+xml" title="GameRank Hub updates" href="{BASE_URL}/feed.xml">
  <link rel="stylesheet" href="{prefix}assets/styles.css?v={STYLES_VERSION}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="GameRank Hub">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:alt" content="{esc(image_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:image:alt" content="{esc(image_alt)}">{article_tags}
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>"""


def review_visual_path(slug: str) -> str:
    return f"assets/visuals/review-{slug}-fit.svg"


def guide_visual_path(slug: str) -> str:
    return f"assets/visuals/guide-{slug}.svg"


def blog_visual_path(slug: str) -> str:
    return f"assets/visuals/blog-{slug}.svg"


def related_guide_links(prefix: str, slugs: tuple[str, ...]) -> str:
    return " · ".join(
        f'<a href="{prefix}guides/{slug}.html">{esc(GUIDE_BY_SLUG[slug].title)}</a>' for slug in slugs
    )


def render_review_card(prefix: str, profile: GameProfile) -> str:
    href = f"{prefix}{profile.slug}.html"
    meta = f"{profile.session_length} · {profile.play_style} · {join_platforms(profile.platforms)}"
    return (
        '<article class="library-card">'
        f'<p class="eyebrow">{esc(profile.play_style.upper())}</p>'
        f'<h2><a href="{href}">{esc(profile.title)}</a></h2>'
        f"<p>{esc(profile.review_hub_summary)}</p>"
        f'<p class="article-meta">{esc(meta)}</p>'
        f'<a class="text-link-static" href="{href}">Open profile →</a>'
        "</article>"
    )


def render_review(profile: GameProfile) -> tuple[str, PageMeta]:
    path = f"reviews/{profile.slug}.html"
    prefix = "../"
    image_path = review_visual_path(profile.slug)
    sources = collect_sources((), (SourceRef("Official site", profile.official_url), SourceRef(profile.source_label, profile.source_url)))
    top_sources = " · ".join(f'<a href="{esc(source.url)}">{esc(source.label)}</a>' for source in sources)
    body = f"""
      <section id="disclosure"><p class="eyebrow">BEFORE YOU PLAY</p><h2>What this page is and is not</h2>
        <div class="answer-box warning"><strong>{esc(profile.summary)}</strong><p>This is a sourced editorial fit profile. It is designed to help with a yes-or-no play decision, and it does not claim a scored hands-on review.</p></div>
        <p>{esc(profile.onboarding_notes)}</p>
        <p>The first-session loop to judge is simple: {esc(profile.core_loop)}</p>
        <p>{esc(profile.progression_notes)}</p>
      </section>
      {visual_figure(prefix, image_path, f"Editorial fit map for {profile.name}", "Editorial fit map summarizing session length, social shape, and spending model. This illustration is not gameplay footage.")}
      <section id="snapshot"><p class="eyebrow">FIT SNAPSHOT</p><h2>{esc(profile.name)} at a glance</h2>
        <div class="comparison-table-wrap"><table><tbody>
          <tr><th>Genre</th><td>{esc(profile.genre)}</td></tr>
          <tr><th>Platforms</th><td>{esc(join_platforms(profile.platforms))}</td></tr>
          <tr><th>Business model</th><td>{esc(profile.business_model)}</td></tr>
          <tr><th>Typical session</th><td>{esc(profile.session_length)}</td></tr>
          <tr><th>Play style</th><td>{esc(profile.play_style)}</td></tr>
          <tr><th>Learning barrier</th><td>{esc(profile.learning_barrier)}</td></tr>
          <tr><th>Social shape</th><td>{esc(profile.social_shape)}</td></tr>
        </tbody></table></div>
      </section>
      <section id="fit"><p class="eyebrow">WHO IT FITS</p><h2>Best fit, likely friction, and the social reality</h2>
        <div class="check-grid">
          <div><strong>Best for</strong><p>{esc(profile.best_for)}</p></div>
          <div><strong>Probably not for</strong><p>{esc(profile.not_for)}</p></div>
          <div><strong>How the social load feels</strong><p>{esc(profile.social_shape)}</p></div>
          <div><strong>Why people stay</strong><p>{esc(profile.progression_notes)}</p></div>
        </div>
      </section>
      <section id="first-session"><p class="eyebrow">FIRST SESSION PLAN</p><h2>How to test the fit in one evening</h2>
        {render_step_list(profile.first_session_plan)}
        <p>Use the first session to answer these fit questions instead of judging rank, win rate, or store value immediately.</p>
        {render_feature_list(profile.fit_questions)}
      </section>
      <section id="commitment"><p class="eyebrow">TIME, COST, AND COMMITMENT</p><h2>What you are really signing up for</h2>
        <div class="comparison-table-wrap"><table><tbody>
          <tr><th>Session budget</th><td>{esc(profile.session_length)}</td></tr>
          <tr><th>Social demand</th><td>{esc(profile.social_shape)}</td></tr>
          <tr><th>Progression shape</th><td>{esc(profile.progression_notes)}</td></tr>
          <tr><th>Spending pressure</th><td>{esc(profile.spending_notes)}</td></tr>
        </tbody></table></div>
        <p>{esc(profile.commitment_notes)}</p>
        <p>{esc(profile.spending_notes)}</p>
      </section>
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>What was checked, and what can change</h2>
        <div class="check-grid">
          <div><strong>Official sources checked on {esc(friendly_date(profile.checked_date))}</strong>{render_source_list(sources)}</div>
          <div><strong>Details that can move after publication</strong>{render_plain_list(profile.what_can_change)}</div>
        </div>
        <p>This profile uses official game pages and defensible general product knowledge to frame the player fit. It does not claim live testing across every platform, accessibility need, or current event rotation.</p>
      </section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical_url(path)}#webpage",
                "name": profile.title,
                "url": canonical_url(path),
                "description": profile.description,
                "datePublished": TODAY_STR,
                "dateModified": TODAY_STR,
                "about": {"@id": f"{canonical_url(path)}#game"},
            },
            {
                "@type": "Article",
                "@id": f"{canonical_url(path)}#article",
                "headline": profile.title,
                "description": profile.description,
                "datePublished": TODAY_STR,
                "dateModified": TODAY_STR,
                "author": {"@type": "Organization", "name": SITE_AUTHOR, "url": f"{BASE_URL}/about.html"},
                "publisher": {"@type": "Organization", "name": "GameRank Hub"},
                "mainEntityOfPage": {"@id": f"{canonical_url(path)}#webpage"},
                "image": canonical_url(image_path),
                "about": {"@id": f"{canonical_url(path)}#game"},
            },
            {
                "@type": "VideoGame",
                "@id": f"{canonical_url(path)}#game",
                "name": profile.name,
                "genre": profile.genre,
                "url": profile.official_url,
                "description": profile.summary,
                "gamePlatform": list(profile.platforms),
            },
            breadcrumbs([("Home", ""), ("Game Profiles", "reviews/index.html"), (profile.name, None)]),
        ],
    }
    page = f"""{head(profile.title, profile.description, path, schema, prefix, image_path=image_path, image_alt=f"{profile.name} fit profile illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "reviews")}
<main id="main">
  <section class="article-hero purple-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="index.html">Game Profiles</a><span>/</span><span>{esc(profile.name)}</span></nav><p class="eyebrow">GAME FIT PROFILE</p><h1>{esc(profile.title)}</h1><p class="hero-lede">{esc(profile.summary)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(profile.checked_date)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p><p class="article-byline">Official sources: {top_sources}</p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>On this page</strong><a href="#disclosure">What this page is</a><a href="#snapshot">Fit snapshot</a><a href="#fit">Who it fits</a><a href="#first-session">First session plan</a><a href="#commitment">Time and cost</a><a href="#sources">Sources and limits</a></aside><article class="article-body">{body}<div class="related-box"><span>NEXT STEP</span><h2>Compare the fit or solve the setup question</h2><p>Use {related_guide_links(prefix, profile.related_guides)} or go back to the <a href="index.html">game fit hub</a>.</p></div></article></div>
</main>{footer(prefix)}</body></html>"""
    keywords = f"{profile.name.lower()} review before you play fit guide {profile.play_style.lower()} {profile.genre.lower()} free game"
    return page, PageMeta(profile.title, path, path, profile.description, keywords, "review", TODAY_STR, TODAY_STR)


def render_guide(item: GuideItem) -> tuple[str, PageMeta]:
    path = f"guides/{item.slug}.html"
    prefix = "../"
    image_path = guide_visual_path(item.slug)
    sources = collect_sources(item.source_keys, item.extra_sources)
    body = f"""
      <section id="answer"><p class="eyebrow">QUICK ANSWER</p><h2>The short version</h2>
        <div class="answer-box"><strong>{esc(item.summary)}</strong><p>{esc(item.quick_answer)}</p></div>
        <p>{esc(item.introduction[0])}</p><p>{esc(item.introduction[1])}</p>
      </section>
      {visual_figure(prefix, image_path, f"Editorial checklist illustration for {item.title}", "Editorial checklist illustration for this guide. It is not a benchmark chart or captured settings screen.")}
      <section id="checklist"><p class="eyebrow">CHECKLIST</p><h2>What to confirm before you change anything</h2>{render_feature_list(item.checklist)}<p>{esc(item.checklist_note)}</p></section>
      <section id="scenario"><p class="eyebrow">SCENARIO</p><h2>{esc(item.scenario_title)}</h2><p>{esc(item.scenario[0])}</p><p>{esc(item.scenario[1])}</p></section>
      <section id="process"><p class="eyebrow">PROCESS</p><h2>A repeatable way to work through it</h2>{render_named_cards(item.steps, "STEP")}<p>{esc(item.follow_through)}</p></section>
      <section id="mistakes"><p class="eyebrow">COMMON MISTAKES</p><h2>What usually makes the problem worse</h2>{render_named_cards(item.mistakes, "WATCH OUT")}</section>
      <section id="success"><p class="eyebrow">SUCCESS CRITERIA</p><h2>How to know the change actually worked</h2>{render_feature_list(item.success_criteria)}<p>{esc(item.success_note)}</p></section>
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>Where to verify live details</h2><div class="check-grid"><div><strong>Useful official source surfaces</strong>{render_source_list(sources)}</div><div><strong>Important limitations</strong>{render_plain_list(item.limitations)}</div></div><p>Menu names, defaults, and device behavior can change after updates. Use the linked official support surfaces for the current live details and keep this guide for the process around them.</p></section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{canonical_url(path)}#article",
                "headline": item.title,
                "description": item.description,
                "datePublished": TODAY_STR,
                "dateModified": TODAY_STR,
                "author": {"@type": "Organization", "name": SITE_AUTHOR, "url": f"{BASE_URL}/about.html"},
                "publisher": {"@type": "Organization", "name": "GameRank Hub"},
                "mainEntityOfPage": canonical_url(path),
                "image": canonical_url(image_path),
            },
            {
                "@type": "HowTo",
                "@id": f"{canonical_url(path)}#howto",
                "name": item.title,
                "description": item.summary,
                "step": [{"@type": "HowToStep", "position": index, "name": step.title, "text": step.text} for index, step in enumerate(item.steps, 1)],
            },
            breadcrumbs([("Home", ""), ("Guides", "guides/index.html"), (item.title, None)]),
        ],
    }
    page = f"""{head(f"{item.title} | GameRank Hub", item.description, path, schema, prefix, image_path=image_path, image_alt=f"{item.title} editorial illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "guides")}
<main id="main">
  <section class="article-hero orange-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="index.html">Guides</a><span>/</span><span>{esc(item.title)}</span></nav><p class="eyebrow">{esc(item.category.upper())} GUIDE</p><h1>{esc(item.title)}</h1><p class="hero-lede">{esc(item.summary)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>In this guide</strong><a href="#answer">Quick answer</a><a href="#checklist">Checklist</a><a href="#scenario">Scenario</a><a href="#process">Process</a><a href="#mistakes">Mistakes</a><a href="#success">Success</a><a href="#sources">Sources</a></aside><article class="article-body">{body}<div class="related-box"><span>KEEP GOING</span><h2>Apply the method or compare games</h2><p>Return to the <a href="index.html">guide library</a> or use the <a href="../reviews/index.html">game fit hub</a> to make the advice concrete.</p></div></article></div>
</main>{footer(prefix)}</body></html>"""
    keywords = f"{item.title.lower()} gaming guide {item.category.lower()} checklist practical"
    return page, PageMeta(item.title, path, path, item.description, keywords, "guide", TODAY_STR, TODAY_STR)


def render_blog(post: BlogPost) -> tuple[str, PageMeta]:
    path = f"blog/{post.slug}.html"
    prefix = "../"
    image_path = blog_visual_path(post.slug)
    sources = collect_sources(post.source_keys, post.extra_sources)
    section_html = []
    for section in post.sections:
        bullets = render_feature_list(section.bullets) if section.bullets else ""
        paragraphs = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in section.paragraphs)
        section_html.append(f'<section><p class="eyebrow">ANALYSIS</p><h2>{esc(section.heading)}</h2>{paragraphs}{bullets}</section>')
    body = (
        f'<section id="intro"><p class="eyebrow">WHY THIS MATTERS</p><h2>{esc(post.summary)}</h2>'
        f'<div class="answer-box"><strong>{esc(post.summary)}</strong><p>{esc(post.intro[0])}</p></div><p>{esc(post.intro[1])}</p></section>'
        + visual_figure(prefix, image_path, f"Editorial analysis illustration for {post.title}", "Editorial analysis illustration summarizing the article's decision points. It is not gameplay footage.")
        + "".join(section_html)
        + f'<section id="takeaways"><p class="eyebrow">TAKEAWAYS</p><h2>The practical shortlist</h2>{render_feature_list(post.takeaways)}<p>{esc(post.conclusion)}</p></section>'
        + f'<section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>What this analysis leans on</h2><div class="check-grid"><div><strong>Source surfaces</strong>{render_source_list(sources)}</div><div><strong>Limits to remember</strong>{render_plain_list(post.limitations)}</div></div><p>This article is an editorial analysis, not a substitute for current store terms, patch notes, or support pages. Use the links above when the live fact itself is the thing you need.</p></section>'
    )
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": f"{canonical_url(path)}#post",
                "headline": post.title,
                "description": post.description,
                "datePublished": TODAY_STR,
                "dateModified": TODAY_STR,
                "author": {"@type": "Organization", "name": SITE_AUTHOR, "url": f"{BASE_URL}/about.html"},
                "publisher": {"@type": "Organization", "name": "GameRank Hub"},
                "mainEntityOfPage": canonical_url(path),
                "image": canonical_url(image_path),
            },
            breadcrumbs([("Home", ""), ("Blog", "blog/index.html"), (post.title, None)]),
        ],
    }
    page = f"""{head(f"{post.title} | GameRank Hub Blog", post.description, path, schema, prefix, image_path=image_path, image_alt=f"{post.title} editorial illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "blog")}
<main id="main">
  <section class="article-hero green-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="index.html">Blog</a><span>/</span><span>{esc(post.title)}</span></nav><p class="eyebrow">{esc(post.category.upper())}</p><h1>{esc(post.title)}</h1><p class="hero-lede">{esc(post.summary)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>In this article</strong><a href="#intro">Why this matters</a><a href="#takeaways">Takeaways</a><a href="#sources">Sources</a><a href="index.html">More posts</a></aside><article class="article-body">{body}<div class="related-box"><span>KEEP READING</span><h2>Use the analysis on a real decision</h2><p>Go to the <a href="../reviews/index.html">game fit hub</a> or the <a href="../guides/index.html">guide library</a> for the practical follow-through.</p></div></article></div>
</main>{footer(prefix)}</body></html>"""
    keywords = f"{post.title.lower()} gaming editorial analysis free games fit profiles"
    return page, PageMeta(post.title, path, path, post.description, keywords, "blog", TODAY_STR, TODAY_STR)


def render_review_index(review_entries: list[PageMeta]) -> tuple[str, PageMeta]:
    path = "reviews/index.html"
    prefix = "../"
    image_path = "assets/visuals/hub-reviews.svg"
    session_groups = {
        "short": ("Quick sessions", "Usually 1 to 20 minutes of real play."),
        "medium": ("Planned match blocks", "Set aside a focused chunk and expect one or two full games."),
        "long": ("Long competitive blocks", "These games usually become the main activity of the night."),
        "flex": ("Flexible hobby worlds", "Short tasks are possible, but the broader game can easily absorb more time."),
    }
    bucket_cards = []
    for bucket, (label, copy) in session_groups.items():
        games = [game for game in GAMES if game.session_bucket == bucket]
        examples = ", ".join(game.name for game in games[:3])
        bucket_cards.append(f"<article><span>{len(games)} GAMES</span><h3>{esc(label)}</h3><p>{esc(copy)} Examples: {esc(examples)}.</p></article>")
    by_group_intro = {
        "competitive": "These are the pages to open when you care about repeated matches, clear win conditions, and whether the social or mechanical load matches your appetite.",
        "progression": "These profiles focus on longer hobby games where the real question is not just moment-to-moment fun, but whether the surrounding progression structure suits your time and spending habits.",
        "strategy": "Use this cluster when you want planning, deckbuilding, economy, or macro decisions to matter as much as or more than raw reflexes.",
        "social": "These pages cover variety platforms, party games, and creative sandboxes where curation, group mood, or self-directed play matter more than one strict ladder.",
    }
    grouped_cards = []
    for group, heading in (
        ("competitive", "Competitive matches and quick-fire skill loops"),
        ("progression", "Longer hobby progression and MMO-style commitments"),
        ("strategy", "Strategy, cards, and slower-thinking competition"),
        ("social", "Creative, party, and family-friendly variety"),
    ):
        cards = "".join(render_review_card("", game) for game in GAMES if game.hub_group == group)
        grouped_cards.append(f'<section id="{group}"><p class="eyebrow">PLAY STYLE</p><h2>{esc(heading)}</h2><p>{esc(by_group_intro[group])}</p><div class="library-grid">{cards}</div></section>')
    mobile_links = tuple(f"{game.name} — {game.session_length}" for game in GAMES if "mobile" in game.platform_tags)
    pc_only_links = tuple(f"{game.name} — {game.play_style}" for game in GAMES if game.platform_tags == ("pc",))
    couch_links = (
        "Fortnite — quick squad sessions",
        "Fall Guys — easy mixed-skill party rounds",
        "Rocket League — immediate local or online play",
        "Brawlhalla — short fighting-game bursts",
        "Halo Infinite Multiplayer — readable arena matches",
    )
    compare_rows = "".join(
        f"<tr><th><a href=\"{game.slug}.html\">{esc(game.name)}</a></th><td>{esc(game.session_length)}</td><td>{esc(game.best_for)}</td><td>{esc(game.social_shape)}</td><td>{esc(game.spending_notes)}</td></tr>"
        for game in GAMES
    )
    next_checks = (
        "Open the individual profile for official source links.",
        "Check the business model before buying passes or expansions.",
        "Use the related guides when setup, cross-play, or spending is the real blocker.",
    )
    includes = (
        "Visible published and checked dates.",
        "Official source links for the game's live facts.",
        "A first-session plan, fit questions, and spending notes.",
        "A note on what can change after publication.",
    )
    does_not = (
        "A scored hands-on review across every platform.",
        "A guarantee that live-service details stayed unchanged after the checked date.",
        "A universal verdict for every type of player.",
        "Current store terms that should replace the official source pages.",
    )
    body = f"""
      <section id="how-to-use"><p class="eyebrow">HOW TO USE THIS HUB</p><h2>Start with the shape of your time, not the loudest trailer</h2>
        <div class="answer-box"><strong>This is a decision hub, not a popularity list.</strong><p>Use it to compare how much time a game wants, how social it really is, what the spending pressure looks like, and whether the first session teaches the right things.</p></div>
        <p>The original page URLs stay in place for compatibility, but each page is now a before-you-play profile. The goal is not to score every game the same way. It is to surface the tradeoffs that actually change a person's decision.</p>
        <p>Start with session length and play style, then check platform and business model. If two games sound equally good, the better fit is usually the one whose social load and progression pressure make more sense for your current life.</p>
      </section>
      {visual_figure(prefix, image_path, "Editorial illustration for the game fit hub", "Editorial hub illustration showing the three main comparison lenses: time, play style, and platform.")}
      <section id="by-time"><p class="eyebrow">FILTER BY SESSION LENGTH</p><h2>First ask how much uninterrupted time you actually have</h2><div class="guide-cards">{''.join(bucket_cards)}</div></section>
      {''.join(grouped_cards)}
      <section id="platforms"><p class="eyebrow">FILTER BY PLATFORM</p><h2>Shortcuts for common device questions</h2><div class="check-grid"><div><strong>Mobile-friendly options</strong>{render_plain_list(mobile_links)}</div><div><strong>PC-first deep dives</strong>{render_plain_list(pc_only_links)}</div><div><strong>Good couch or mixed-device group picks</strong>{render_plain_list(couch_links)}</div><div><strong>What to verify next</strong>{render_plain_list(next_checks)}</div></div></section>
      <section id="compare"><p class="eyebrow">COMPARE THE FULL LIBRARY</p><h2>One-table view of the 30 current profiles</h2><div class="comparison-table-wrap"><table><thead><tr><th>Game</th><th>Typical session</th><th>Best for</th><th>Social shape</th><th>Spending notes</th></tr></thead><tbody>{compare_rows}</tbody></table></div></section>
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>How to read these profiles responsibly</h2><div class="check-grid"><div><strong>What each profile includes</strong>{render_plain_list(includes)}</div><div><strong>What each profile does not claim</strong>{render_plain_list(does_not)}</div></div><p>When the live fact itself is the question—price, account requirements, platform support, or current event terms—open the profile and use the official source links first.</p></section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": "Game Fit Profiles", "description": "Decision hub for 30 free or free-entry game fit profiles grouped by time, play style, and platform.", "url": canonical_url(path)},
            {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": index, "url": canonical_url(meta.url), "name": meta.title} for index, meta in enumerate(review_entries, 1)]},
            breadcrumbs([("Home", ""), ("Game Profiles", None)]),
        ],
    }
    title = "Free Game Fit Profiles: Choose by Session Length, Social Shape, and Platform"
    description = "Use this decision hub to compare 30 free or free-entry games by time commitment, play style, platform support, and spending friction."
    page = f"""{head(title, description, path, schema, prefix, og_type="website", image_path=image_path, image_alt="Game fit hub illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "reviews")}
<main id="main">
  <section class="article-hero neutral-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><span>Game Profiles</span></nav><p class="eyebrow">GAME FIT HUB</p><h1>Free Game Fit Profiles</h1><p class="hero-lede">{esc(description)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(5, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>Jump to</strong><a href="#by-time">By time</a><a href="#competitive">Competitive</a><a href="#progression">Progression</a><a href="#strategy">Strategy</a><a href="#social">Social & sandbox</a><a href="#platforms">Platform shortcuts</a><a href="#compare">Full compare</a><a href="#sources">Sources</a></aside><article class="article-body">{body}</article></div>
</main>{footer(prefix)}</body></html>"""
    return page, PageMeta(title, path, path, description, "game reviews fit profiles free games session length platform", "review-hub", TODAY_STR, TODAY_STR)


def render_guides_index(guide_entries: list[PageMeta]) -> tuple[str, PageMeta]:
    path = "guides/index.html"
    prefix = "../"
    image_path = "assets/visuals/hub-guides.svg"
    category_copy = {
        "Controls": "Use these when input feel, binds, or aim habits are the real blocker.",
        "Performance": "Open these when stutter, latency, or browser overhead matter more than raw skill.",
        "Teamwork": "These are the practical reads for the first ten matches, group nights, and calmer comms.",
        "Safety": "Read these before spending money or handing a social live-service game to a family member.",
        "Setup": "Use these when cross-play, cloud access, or mixed-device planning is the actual problem.",
        "Wellbeing": "Comfort and accessibility belong in the same decision stack as performance.",
        "Editorial": "This is where the site's publishing model and limits are explained clearly.",
    }
    starter_cards = (
        ("New to PC controls", GUIDE_BY_SLUG["keyboard-mouse-basics"]),
        ("Settings feel wrong", GUIDE_BY_SLUG["choose-gaming-sensitivity"]),
        ("Performance feels unstable", GUIDE_BY_SLUG["optimize-fps-settings"]),
        ("Joining friends online", GUIDE_BY_SLUG["multiplayer-beginner-checklist"]),
    )
    starter_html = "".join(
        f'<article><span>START HERE</span><h3><a href="{guide.slug}.html">{esc(label)}</a></h3><p>{esc(guide.summary)}</p></article>'
        for label, guide in starter_cards
    )
    guides_do = (
        "Explain a repeatable process.",
        "Link out to official support surfaces for live settings and policies.",
        "Call out limits so you know what still depends on your device or game.",
        "Prefer practical checklists over abstract theory.",
    )
    guides_do_not = (
        "Replace current official support documentation.",
        "Promise one magic setting for every player.",
        "Act as medical or legal advice.",
        "Assume every game or platform exposes identical options.",
    )
    grouped = []
    for category in ("Controls", "Performance", "Teamwork", "Safety", "Setup", "Wellbeing", "Editorial"):
        cards = "".join(
            f'<article class="library-card"><p class="eyebrow">{esc(category.upper())}</p><h2><a href="{guide.slug}.html">{esc(guide.title)}</a></h2><p>{esc(guide.summary)}</p><a class="text-link-static" href="{guide.slug}.html">Read guide →</a></article>'
            for guide in GUIDES
            if guide.category == category
        )
        grouped.append(f'<section id="{category.lower()}"><p class="eyebrow">CATEGORY</p><h2>{esc(category)}</h2><p>{esc(category_copy[category])}</p><div class="library-grid">{cards}</div></section>')
    body = f"""
      <section id="how-to-use"><p class="eyebrow">USEFUL FIRST READS</p><h2>Start with the blocker you can name clearly</h2><div class="guide-cards">{starter_html}</div><p>The guide library is organized around problems rather than around game genres. That keeps the advice portable: a better setup process or clearer spending rule should help you across more than one game.</p></section>
      {visual_figure(prefix, image_path, "Editorial illustration for the guide hub", "Editorial hub illustration highlighting controls, performance, and safety as the main guide lanes.")}
      {''.join(grouped)}
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>What these guides are for</h2><div class="check-grid"><div><strong>These guides do</strong>{render_plain_list(guides_do)}</div><div><strong>These guides do not</strong>{render_plain_list(guides_do_not)}</div></div></section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": "Practical Gaming Guides", "description": "Grouped library of practical gaming guides for controls, performance, teamwork, safety, setup, and editorial method.", "url": canonical_url(path)},
            {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": index, "url": canonical_url(meta.url), "name": meta.title} for index, meta in enumerate(guide_entries, 1)]},
            breadcrumbs([("Home", ""), ("Guides", None)]),
        ],
    }
    title = "Practical Gaming Guides: Solve Controls, Performance, Safety, and Setup Problems"
    description = "Use these practical gaming guides to fix settings, plan multiplayer sessions, handle free-to-play spending, and understand the site's editorial method."
    page = f"""{head(title, description, path, schema, prefix, og_type="website", image_path=image_path, image_alt="Practical gaming guides illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "guides")}
<main id="main">
  <section class="article-hero neutral-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><span>Guides</span></nav><p class="eyebrow">GUIDE LIBRARY</p><h1>Practical Gaming Guides</h1><p class="hero-lede">{esc(description)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>Jump to</strong><a href="#controls">Controls</a><a href="#performance">Performance</a><a href="#teamwork">Teamwork</a><a href="#safety">Safety</a><a href="#setup">Setup</a><a href="#wellbeing">Wellbeing</a><a href="#editorial">Editorial</a><a href="#sources">Sources</a></aside><article class="article-body">{body}</article></div>
</main>{footer(prefix)}</body></html>"""
    return page, PageMeta(title, path, path, description, "gaming guides controls performance safety setup", "guide-hub", TODAY_STR, TODAY_STR)


def render_blog_index(blog_entries: list[PageMeta]) -> tuple[str, PageMeta]:
    path = "blog/index.html"
    prefix = "../"
    image_path = "assets/visuals/hub-blog.svg"
    site_work = [BLOG_BY_SLUG["how-we-update-rankings"]]
    player_choice = [BLOG_BY_SLUG["best-game-for-short-sessions"], BLOG_BY_SLUG["what-makes-a-good-free-game"], BLOG_BY_SLUG["before-you-download-a-new-game"]]
    work_cards = "".join(f'<article class="library-card"><p class="eyebrow">{esc(post.category.upper())}</p><h2><a href="{post.slug}.html">{esc(post.title)}</a></h2><p>{esc(post.summary)}</p><a class="text-link-static" href="{post.slug}.html">Read article →</a></article>' for post in site_work)
    choice_cards = "".join(f'<article class="library-card"><p class="eyebrow">{esc(post.category.upper())}</p><h2><a href="{post.slug}.html">{esc(post.title)}</a></h2><p>{esc(post.summary)}</p><a class="text-link-static" href="{post.slug}.html">Read article →</a></article>' for post in player_choice)
    table_rows = "".join(f"<tr><th><a href=\"{post.slug}.html\">{esc(post.title)}</a></th><td>{esc(post.summary)}</td></tr>" for post in BLOG_POSTS)
    best_use_cases = (
        "Choose what to read before a download or return-to-play decision.",
        "Understand the site's publishing model before assuming what a date means.",
        "Compare free-to-play pressures at a higher level than one game page allows.",
    )
    not_replacement = (
        "Official store terms or support pages.",
        "The individual profile when you need game-specific source links.",
        "Hands-on technical testing across every platform.",
    )
    body = f"""
      <section id="why"><p class="eyebrow">WHY THIS BLOG EXISTS</p><h2>Short editorial pieces for questions that do not belong on one game page</h2><div class="answer-box"><strong>The blog fills the gaps between the hubs and the guides.</strong><p>These articles explain how we update pages, how to evaluate free games, and how to make better install decisions before a game ever reaches your hard drive.</p></div><p>The point is not to publish filler commentary. Each post is meant to answer a practical question that can improve the rest of the site: how to judge short-session fit, what free-to-play fairness looks like, and how update integrity should actually work.</p></section>
      {visual_figure(prefix, image_path, "Editorial illustration for the blog hub", "Editorial blog-hub illustration highlighting site method, free-game analysis, and better download decisions.")}
      <section id="site-method"><p class="eyebrow">SITE METHOD</p><h2>How this publishing model stays honest</h2><div class="library-grid">{work_cards}</div></section>
      <section id="player-choice"><p class="eyebrow">PLAYER DECISIONS</p><h2>How to choose games and free-to-play models more clearly</h2><div class="library-grid">{choice_cards}</div></section>
      <section id="compare"><p class="eyebrow">AT A GLANCE</p><h2>What each article helps you answer</h2><div class="comparison-table-wrap"><table><thead><tr><th>Article</th><th>Main question answered</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>How these articles should be used</h2><div class="check-grid"><div><strong>Best use cases</strong>{render_plain_list(best_use_cases)}</div><div><strong>Not a replacement for</strong>{render_plain_list(not_replacement)}</div></div></section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "name": "GameRank Hub Blog", "description": "Editorial notes about fit profiles, free-to-play fairness, short-session choices, and update integrity.", "url": canonical_url(path)},
            {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": index, "url": canonical_url(meta.url), "name": meta.title} for index, meta in enumerate(blog_entries, 1)]},
            breadcrumbs([("Home", ""), ("Blog", None)]),
        ],
    }
    title = "GameRank Hub Blog: Better Ways to Judge Free Games and Your Next Download"
    description = "Read short editorial pieces about free-game fairness, short-session fit, smarter download decisions, and how GameRank Hub updates its profiles."
    page = f"""{head(title, description, path, schema, prefix, og_type="website", image_path=image_path, image_alt="GameRank Hub blog illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "blog")}
<main id="main">
  <section class="article-hero neutral-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><span>Blog</span></nav><p class="eyebrow">EDITORIAL BLOG</p><h1>GameRank Hub Blog</h1><p class="hero-lede">{esc(description)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="../about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>Jump to</strong><a href="#site-method">Site method</a><a href="#player-choice">Player decisions</a><a href="#compare">At a glance</a><a href="#sources">Sources</a></aside><article class="article-body">{body}</article></div>
</main>{footer(prefix)}</body></html>"""
    return page, PageMeta(title, path, path, description, "gaming blog free games short sessions editorial updates", "blog-hub", TODAY_STR, TODAY_STR)


def render_faq() -> tuple[str, PageMeta]:
    path = "faq.html"
    prefix = ""
    image_path = "assets/visuals/hub-faq.svg"
    qa = (
        ("What is a game fit profile?", "A fit profile is a sourced editorial page built to answer whether a game matches a player's time, platform, budget, and social preferences. It is not a scored hands-on review."),
        ("Why do the URLs still live under /reviews/?", "The old URLs were preserved for compatibility, but the pages now behave like before-you-play profiles rather than generic review templates."),
        ("Do these pages claim hands-on testing?", "Not unless a page explicitly says what was tested and when. The generated profiles in this overhaul rely on official sources and careful, defensible general product knowledge."),
        ("What do the published and checked dates mean?", "Published marks this editorial version. Checked tells you when the visible source-backed facts on the page were last reviewed together."),
        ("How do you handle changing live-service details?", "Each profile links to official sources, names what can change, and uses the checked date as the boundary of the editorial claim."),
        ("Why do free games still get spending warnings?", "Because cost risk is part of fit. A free download can still create banner, pass, pack, or convenience pressure that changes the recommendation."),
        ("Should families use these pages by themselves for child safety choices?", "No. Use them as a starting point, then verify the current platform or game safety controls through official parental and account settings."),
        ("How can I request a correction?", "The public correction route is not published yet in this static preview. When it exists, it will be listed on the About page."),
    )
    faq_details = "".join(f"<details><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>" for question, answer in qa)
    sources = (
        SourceRef("GameRank Hub editorial policy", f"{BASE_URL}/about.html"),
        SourceRef("Game fit hub", f"{BASE_URL}/reviews/index.html"),
        SourceRef("How updates work", f"{BASE_URL}/blog/how-we-update-rankings.html"),
    )
    faq_limits = (
        "This static preview does not yet publish a live public correction inbox.",
        "Official game terms can change after the checked date on any one profile.",
        "Profiles are sourced editorial decisions, not hands-on testing claims unless stated otherwise.",
    )
    body = f"""
      <section id="how"><p class="eyebrow">HOW TO READ THE SITE</p><h2>Use the FAQ as the frame around the profiles</h2>
        <div class="answer-box"><strong>These pages are built to reduce generic filler.</strong><p>The fit profiles answer install decisions. The guides solve recurring setup or safety problems. The blog explains the editorial model and the decisions that sit above any one game page.</p></div>
        <p>The FAQ exists so you do not have to infer the method. If a page is sourced, it should say so. If a date moved, it should mean something. If a game can change faster than an editorial page, that limit should stay visible instead of being hidden in the tone.</p>
      </section>
      {visual_figure(prefix, image_path, "Editorial illustration for the FAQ page", "Editorial FAQ illustration highlighting sources, dates, and limitations.")}
      <section id="questions"><p class="eyebrow">COMMON QUESTIONS</p><h2>Questions about profiles, updates, and limits</h2>{faq_details}</section>
      <section id="sources"><p class="eyebrow">SOURCES AND LIMITS</p><h2>Where the policy questions point next</h2><div class="check-grid"><div><strong>Useful source pages</strong>{render_source_list(sources)}</div><div><strong>Current limitations</strong>{render_plain_list(faq_limits)}</div></div></section>"""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}} for question, answer in qa]},
            breadcrumbs([("Home", ""), ("FAQ", None)]),
        ],
    }
    title = "GameRank Hub FAQ: Fit Profiles, Updates, Sources, and Limits"
    description = "Answers about GameRank Hub's fit profiles, update dates, official sources, spending warnings, and editorial limitations."
    page = f"""{head(title, description, path, schema, prefix, image_path=image_path, image_alt="GameRank Hub FAQ illustration")}
<body><a class="skip-link" href="#main">Skip to content</a>{nav(prefix, "faq")}
<main id="main">
  <section class="article-hero neutral-hero"><div class="shell narrow"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>FAQ</span></nav><p class="eyebrow">FAQ</p><h1>GameRank Hub FAQ</h1><p class="hero-lede">{esc(description)}</p><p class="article-meta">Published {friendly_date(TODAY)} · Checked {friendly_date(TODAY)} · {max(4, round(words(body) / 220))} minute read</p><p class="article-byline">By the <a href="about.html">GameRank Hub Editorial Team</a></p></div></section>
  <div class="shell article-layout"><aside class="toc"><strong>Jump to</strong><a href="#how">How to read the site</a><a href="#questions">Questions</a><a href="#sources">Sources</a></aside><article class="article-body">{body}<div class="related-box"><span>NEXT STEP</span><h2>Read the policy or use the hub</h2><p>Open the <a href="about.html">editorial policy</a> or jump into the <a href="reviews/index.html">game fit hub</a>.</p></div></article></div>
</main>{footer(prefix)}</body></html>"""
    return page, PageMeta(title, path, path, description, "faq fit profiles update policy editorial limits", "faq", TODAY_STR, TODAY_STR)


def static_pages() -> list[PageMeta]:
    return [
        PageMeta("GameRank Hub", "index.html", "", "Use sourced game fit profiles, practical guides, and editorial explainers to choose what to play next.", "game hub free games fit profiles gaming guides", "static", checked=STATIC_LASTMOD),
        PageMeta("Best Free Games", "best-free-games.html", "best-free-games.html", "Compare free games by genre and platform.", "best free games free online games", "static", checked=STATIC_LASTMOD),
        PageMeta("Browser Games", "browser-games.html", "browser-games.html", "Find browser games that work without downloads.", "browser games no download", "static", checked=STATIC_LASTMOD),
        PageMeta("About GameRank Hub", "about.html", "about.html", "Read the editorial policy and publishing principles behind GameRank Hub.", "about editorial policy gamerank hub", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub Community", "community.html", "community.html", "Read moderated player comments and community ratings.", "community ratings player comments", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub Update Log", "updates.html", "updates.html", "Track material site and editorial updates.", "update log editorial changes", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub Privacy Notice", "privacy.html", "privacy.html", "Understand privacy, moderation, and retention information.", "privacy cookies moderation retention", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub Community Guidelines", "community-guidelines.html", "community-guidelines.html", "Rules for constructive ratings and comments.", "community guidelines moderation comments", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub 简体中文", "zh-cn/", "zh-cn/", "简体中文游戏评测与攻略入口。", "中文 游戏 评测 攻略", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub 日本語", "ja/", "ja/", "日本語のゲームレビューとガイド。", "日本語 ゲーム レビュー ガイド", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub 한국어", "ko/", "ko/", "한국어 게임 리뷰와 가이드.", "한국어 게임 리뷰 가이드", "static", checked=STATIC_LASTMOD),
        PageMeta("GameRank Hub العربية", "ar/", "ar/", "مراجعات ألعاب وأدلة باللغة العربية.", "العربية ألعاب مراجعات أدلة", "static", checked=STATIC_LASTMOD),
    ]


def priority_for(meta: PageMeta) -> str:
    if meta.canonical_path == "":
        return "1.0"
    if meta.kind in {"review-hub", "guide-hub", "blog-hub", "faq"}:
        return "0.9"
    if meta.kind == "static":
        return "0.8"
    return "0.7"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    global GAMES, GUIDES, BLOG_POSTS, GAME_BY_SLUG, GUIDE_BY_SLUG, BLOG_BY_SLUG
    GAME_BY_SLUG = {item.slug: item for item in GAMES}
    GUIDE_BY_SLUG = {item.slug: item for item in GUIDES}
    BLOG_BY_SLUG = {item.slug: item for item in BLOG_POSTS}
    if len(GAME_BY_SLUG) != len(GAME_ORDER):
        raise ValueError(f"Expected {len(GAME_ORDER)} unique games, found {len(GAME_BY_SLUG)}")
    if len(GUIDE_BY_SLUG) != len(GUIDE_ORDER):
        raise ValueError(f"Expected {len(GUIDE_ORDER)} unique guides, found {len(GUIDE_BY_SLUG)}")
    if len(BLOG_BY_SLUG) != len(BLOG_ORDER):
        raise ValueError(f"Expected {len(BLOG_ORDER)} unique blog posts, found {len(BLOG_BY_SLUG)}")
    GAMES = [GAME_BY_SLUG[slug] for slug in GAME_ORDER]
    GUIDES = [GUIDE_BY_SLUG[slug] for slug in GUIDE_ORDER]
    BLOG_POSTS = [BLOG_BY_SLUG[slug] for slug in BLOG_ORDER]

    visuals_dir = ROOT / "assets" / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)
    for svg in visuals_dir.glob("*.svg"):
        svg.unlink()

    for profile in GAMES:
        write(ROOT / review_visual_path(profile.slug), build_visual_svg(profile.name, "Before you play fit snapshot", "#7057ff", profile.visual_points))
    for guide_item in GUIDES:
        write(ROOT / guide_visual_path(guide_item.slug), build_visual_svg(guide_item.title, "Practical checklist illustration", "#ff8643", guide_item.visual_points))
    for post in BLOG_POSTS:
        write(ROOT / blog_visual_path(post.slug), build_visual_svg(post.title, "Editorial analysis illustration", "#0f9f7a", post.visual_points))
    write(ROOT / "assets" / "visuals" / "hub-reviews.svg", build_visual_svg("Game Fit Hub", "Compare by time, style, and platform", "#7057ff", ("By time", "By style", "By platform")))
    write(ROOT / "assets" / "visuals" / "hub-guides.svg", build_visual_svg("Guide Library", "Solve controls, setup, safety, and performance problems", "#ff8643", ("Controls", "Performance", "Safety")))
    write(ROOT / "assets" / "visuals" / "hub-blog.svg", build_visual_svg("Editorial Blog", "Site method, free-game fairness, and smarter downloads", "#0f9f7a", ("Site method", "Free games", "Downloads")))
    write(ROOT / "assets" / "visuals" / "hub-faq.svg", build_visual_svg("FAQ", "Sources, dates, and limitations", "#64748b", ("Sources", "Dates", "Limits")))

    review_entries: list[PageMeta] = []
    for profile in GAMES:
        page, meta = render_review(profile)
        write(ROOT / meta.url, page)
        review_entries.append(meta)

    guide_entries: list[PageMeta] = []
    for guide_item in GUIDES:
        page, meta = render_guide(guide_item)
        write(ROOT / meta.url, page)
        guide_entries.append(meta)

    blog_entries: list[PageMeta] = []
    for post in BLOG_POSTS:
        page, meta = render_blog(post)
        write(ROOT / meta.url, page)
        blog_entries.append(meta)

    review_hub_html, review_hub_meta = render_review_index(review_entries)
    write(ROOT / review_hub_meta.url, review_hub_html)
    guides_hub_html, guides_hub_meta = render_guides_index(guide_entries)
    write(ROOT / guides_hub_meta.url, guides_hub_html)
    blog_hub_html, blog_hub_meta = render_blog_index(blog_entries)
    write(ROOT / blog_hub_meta.url, blog_hub_html)
    faq_html, faq_meta = render_faq()
    write(ROOT / faq_meta.url, faq_html)

    generated_entries = review_entries + guide_entries + blog_entries + [review_hub_meta, guides_hub_meta, blog_hub_meta, faq_meta]
    search_entries = static_pages() + generated_entries
    search_payload = [
        {
            "title": meta.title,
            "url": meta.url,
            "canonical": canonical_url(meta.canonical_path),
            "description": meta.description,
            "keywords": meta.keywords,
            "kind": meta.kind,
            "published": meta.published,
            "checked": meta.checked,
        }
        for meta in search_entries
    ]
    write(ROOT / "assets" / "search-index.json", json.dumps(search_payload, ensure_ascii=False, indent=2))

    sitemap_entries = static_pages() + generated_entries
    urls = "\n".join(
        f"  <url><loc>{canonical_url(meta.canonical_path)}</loc><lastmod>{meta.checked or meta.published or STATIC_LASTMOD}</lastmod><priority>{priority_for(meta)}</priority></url>"
        for meta in sitemap_entries
    )
    write(ROOT / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')

    feed_items = "\n".join(
        f"    <item><title>{esc(meta.title)}</title><link>{canonical_url(meta.canonical_path)}</link><guid>{canonical_url(meta.canonical_path)}</guid><pubDate>{RFC822_DATE}</pubDate><description>{esc(meta.description)}</description><category>{esc(meta.kind)}</category></item>"
        for meta in generated_entries
    )
    write(
        ROOT / "feed.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>GameRank Hub Updates</title><link>{BASE_URL}/</link><description>New game fit profiles, practical guides, and editorial explainers.</description><language>en-us</language><lastBuildDate>{RFC822_DATE}</lastBuildDate>{feed_items}\n</channel></rss>\n""",
    )

    page_files = list(ROOT.rglob("*.html"))
    total_words = sum(words(page.read_text(encoding="utf-8")) for page in page_files)
    report = {
        "generated": TODAY_STR,
        "publishing_model": "intent-driven sourced profiles",
        "html_pages": len(page_files),
        "review_pages": len(review_entries),
        "fit_profile_pages": len(review_entries),
        "guide_pages": len(guide_entries),
        "blog_posts": len(blog_entries),
        "editorial_visuals": len(list(visuals_dir.glob("*.svg"))),
        "approximate_html_words": total_words,
    }
    write(ROOT / "content-report.json", json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

GUIDES.extend(
    [
        guide(
            slug="choose-gaming-sensitivity",
            title="How to Choose a Gaming Sensitivity You Can Keep",
            category="Controls",
            summary="Pick a mouse or stick sensitivity you can keep for weeks instead of changing it after every rough match.",
            description="A practical sensitivity guide with a repeatable checklist, one real-world scenario, common mistakes, success criteria, and source links.",
            quick_answer="Start with your current setting, change one variable at a time, and keep the winner long enough to judge it in normal play.",
            introduction=(
                "Sensitivity advice becomes generic fast because desk space, stick tension, FOV, game speed, and posture all change what \"comfortable\" actually means. A copied pro number is only useful if the context around it matches yours.",
                "The practical goal is not to find a famous setting. It is to find one that lets you make the same turn twice without panic-correcting, overshooting, or tensing your hand every few minutes.",
            ),
            checklist=(
                "Write down your current DPI, in-game sensitivity, ADS settings, and response-curve options before touching anything.",
                "Measure whether your mouse space or controller grip is actually comfortable enough to support a lower or higher setting.",
                "Pick one repeatable drill, route, or training target instead of testing in random matches only.",
                "Decide whether the real problem is turning speed, micro-adjustments, scope control, or general tension.",
                "Turn off unrelated experiments so you are not changing multiple input variables at once.",
            ),
            checklist_note="This prep stops you from blaming a map, a mood swing, or a bad lobby for what is really a repeatable control issue.",
            scenario_title="When every fight feels either too twitchy or too floaty",
            scenario=(
                "A common pattern is raising sensitivity because 180-degree turns feel slow, then discovering that micro-corrections become shaky and scopes feel worse. The answer is not another giant jump. It is isolating which action truly failed and whether positioning could have solved part of it.",
                "Testing a small range around your baseline in the same environment makes the real problem visible. Often the issue is not raw sensitivity at all; it is poor crosshair starting position, bad anticipation, or too little physical space for the style you want to play.",
            ),
            steps=(
                note("Define the failure in plain language", "Use phrases like 'I over-flick close targets' or 'I cannot finish a 180 without lifting too often.' That creates a testable problem instead of a vague feeling."),
                note("Move in small controlled steps", "Adjust one sensitivity variable at a time in a narrow range. Huge jumps feel dramatic but usually hide whether the setting really helped."),
                note("Test hip-fire and scoped control separately", "If a game exposes separate sliders, diagnose each one with a specific task. A good hip-fire setting can still pair badly with scoped multipliers."),
                note("Lock the winner for several sessions", "A setting needs time under ordinary pressure. If you reset it after one bad game, you learn nothing about whether consistency is improving."),
            ),
            follow_through="Keep short notes for a week: what changed, what improved, and what still felt wrong. That record becomes more useful than your memory the next time a new patch or device tempts you to start over.",
            mistakes=(
                note("Changing settings after every loss", "Match outcomes contain too many variables to diagnose a sensitivity by themselves. Look for repeated control symptoms across comparable tasks."),
                note("Changing DPI, in-game sens, and ADS together", "When three numbers move at once, you cannot tell which part actually helped or hurt."),
                note("Ignoring physical setup", "A smaller mouse pad, thumbstick wear, or awkward arm position can make a perfectly reasonable setting feel wrong."),
            ),
            success_criteria=(
                "You can repeat your most common turn or tracking movement without a large correction.",
                "Scope or ADS control feels related to the base setting instead of like a separate fight.",
                "You stop wanting to change the number after every uneven night.",
                "Your hands and shoulders stay calmer because the setting fits your space and reach.",
            ),
            success_note="A good sensitivity fades into the background. You still miss sometimes, but the misses are understandable and you stop treating the settings menu as emergency therapy.",
            source_keys=("controls",),
            limitations=(
                "No single cm-per-360 or stick value works for every game, device, or posture.",
                "Aim assist, FOV, scope multipliers, and input acceleration vary by game.",
                "Persistent pain, numbness, or strain is a health issue, not a settings puzzle.",
            ),
            visual_points=("Record baseline", "One variable", "Lock for a week"),
        ),
        guide(
            slug="improve-aim-without-grinding",
            title="How to Improve Aim Without Endless Grinding",
            category="Controls",
            summary="Build useful aim through short deliberate drills, target selection, and review instead of endless warm-ups.",
            description="A practical guide to aim improvement that favors short drills, live transfer, realistic review, and sustainable routines over grind-for-grind's-sake.",
            quick_answer="Train one aiming problem at a time, cap the drill length, and prove the change in real matches instead of living in warm-up tools forever.",
            introduction=(
                "Aim improvement is partly mechanical and partly informational. Players often blame accuracy when the earlier problem was crosshair placement, bad peeking, or choosing the wrong target under pressure.",
                "That is why a shorter routine often works better than a marathon. A focused ten-minute block with one clear question teaches more than an hour of autopilot repetitions that never transfer into live play.",
            ),
            checklist=(
                "Choose one aim problem for the week: tracking, flick timing, target switching, or crosshair placement.",
                "Set a time limit for drills before you start so fatigue does not become the default training plan.",
                "Use the same drill or match scenario long enough to spot a real pattern.",
                "Write down one recurring type of miss rather than chasing raw score alone.",
                "Decide how you will test transfer in live games before the practice block ends.",
            ),
            checklist_note="This checklist keeps aim work tied to an actual gameplay need. If the routine cannot answer a live problem, it becomes entertainment instead of training.",
            scenario_title="When your drills look better than your real matches",
            scenario=(
                "Many players can produce decent aim-trainer numbers and still lose ordinary fights because the live failure is not flick speed. It is entering fights with the crosshair too low, peeking without information, or shooting the wrong threat first.",
                "A useful routine therefore begins with one missed moment from a real game and asks what smaller skill would have changed it. Sometimes the answer is tracking. Just as often it is patience, target priority, or where your camera was before the duel started.",
            ),
            steps=(
                note("Name the exact miss", "A miss like 'I lose targets when they strafe close' is actionable. 'My aim is bad' is not."),
                note("Use the shortest drill that matches the miss", "If the problem is crosshair placement, a pathing or angle drill may matter more than a pure flick routine."),
                note("Transfer the same question into live games", "Play a few ordinary matches while only watching for the chosen aiming issue. Ignore the urge to solve every problem simultaneously."),
                note("Review one clip or memory while it is fresh", "A two-minute review after the match is enough to tell whether the drill changed the live decision or only the isolated exercise."),
            ),
            follow_through="Aim improves faster when your routine is boringly sustainable. A short daily habit you keep beats an intense routine you abandon after three nights.",
            mistakes=(
                note("Training only raw flick speed", "Many shooters reward preparation, positioning, and target order as much as the final snap."),
                note("Ignoring movement and peeking habits", "Your aim often looks worse when your body enters the fight from a bad place or at the wrong timing."),
                note("Practicing deep into fatigue", "Once your attention collapses, extra repetitions mostly teach tension and sloppiness."),
            ),
            success_criteria=(
                "Your crosshair starts closer to the next target before the fight fully begins.",
                "You panic less when more than one target appears.",
                "You can explain what part of the duel improved instead of only citing a score.",
                "The routine feels small enough to keep alongside ordinary play.",
            ),
            success_note="Useful aim work changes how fights feel, not just how a drill score looks. The clearest sign is when your live decisions become calmer before your highlight clips become flashier.",
            source_keys=("controls",),
            limitations=(
                "Some games reward positioning and utility usage more than raw aiming output.",
                "Controller aim-assist behavior changes the best drill shape and evaluation criteria.",
                "Visual strain or physical discomfort should be addressed before adding more repetition.",
            ),
            visual_points=("Short drills", "Live transfer", "Review one miss"),
        ),
        guide(
            slug="optimize-fps-settings",
            title="How to Optimize Game Settings for Stable FPS",
            category="Performance",
            summary="Find the settings that smooth busy fights without destroying visibility or turning every patch into a full re-tune.",
            description="A practical FPS optimization guide with a checklist, one scenario, stable-setting process, mistakes, success criteria, and sources.",
            quick_answer="Measure the busy scenes that actually stutter, lower the most expensive settings first, and stop when stability improves without making the game unreadable.",
            introduction=(
                "Average FPS alone is a poor goal. A configuration that looks strong in menus can still feel bad in the exact moments when effects, players, and rapid camera movement all show up together.",
                "The better target is stability you can trust. That means acceptable frame time during the scenes that matter while still preserving the visual information you need to read enemies, objectives, and interfaces.",
            ),
            checklist=(
                "Update the game and graphics software through normal supported tools before tweaking anything else.",
                "Record the current preset so the whole process is reversible.",
                "Choose one effects-heavy scene, map, or replay segment as your repeatable test bed.",
                "Close background downloads, launchers, or tabs that can distort the comparison.",
                "Define your acceptable floor before testing so you know when to stop chasing numbers.",
            ),
            checklist_note="Without a clear test scene and a target floor, it is easy to mistake random variance for improvement and keep stripping settings long after the useful gains are done.",
            scenario_title="When menus feel smooth but real matches fall apart",
            scenario=(
                "A common trap is lowering settings based on a quiet range or lobby, then discovering the big frame drops still happen the moment smoke, particles, streaming assets, or multiple players arrive together. That tells you the quiet scene was never the real test.",
                "By picking one repeatable heavy scene, you can compare meaningful changes. The goal is not the biggest number on the counter. It is predictable behavior in the exact moments when the game usually betrays your setup.",
            ),
            steps=(
                note("Identify the expensive categories first", "Shadows, post-processing, reflections, view distance, and effects often move the needle more than texture settings on a system with enough VRAM."),
                note("Lower visibility-safe settings before readability-critical ones", "Preserve silhouettes, subtitles, interface clarity, and any setting that helps you interpret the action unless it clearly causes the slowdown."),
                note("Set a sane frame cap if needed", "A moderate cap can produce more stable frame time than chasing every possible peak, especially on uneven hardware."),
                note("Retest in the same heavy scene", "If the improvement does not show up where the problem actually lived, it was not the right change."),
            ),
            follow_through="Once the busy-scene result is good enough, stop. A stable preset you understand is more valuable than a slightly higher number produced by constant second-guessing.",
            mistakes=(
                note("Benchmarking only quiet areas", "Menus, empty lobbies, and static scenes rarely reflect the moments where the game becomes unreadable."),
                note("Dropping everything to the lowest setting", "The most aggressive preset can erase useful information without solving the real bottleneck."),
                note("Changing game, driver, and OS behavior simultaneously", "When too many layers move together, you cannot tell which change created the benefit or the new problem."),
            ),
            success_criteria=(
                "Busy fights no longer collapse into obvious frame-time spikes or hitching.",
                "Enemy readability, UI clarity, and subtitle legibility stay good enough for normal play.",
                "The final preset is simple enough to recreate after a patch or reinstall.",
                "You can describe which setting changes helped and which ones were placebo.",
            ),
            success_note="A good performance preset protects your decisions. You should stop thinking about the counter and start trusting the game to stay readable when the screen gets busy.",
            source_keys=("performance",),
            limitations=(
                "Thermal throttling, failing hardware, or power-mode issues may dominate the problem no matter what the in-game preset says.",
                "Network lag and input delay are different issues even when they feel similar in the moment.",
                "Laptop, handheld, and desktop constraints differ too much for one universal settings chart.",
            ),
            visual_points=("Test busy scenes", "Protect visibility", "Document preset"),
        ),
    ]
)

BLOG_POSTS.extend(
    [
        blog(
            slug="how-we-update-rankings",
            title="How GameRank Hub Updates Rankings and Fit Profiles Without Fake Freshness",
            category="Editorial",
            summary="What counts as a material update, why date integrity matters, and why not every seasonal patch deserves a brand-new verdict.",
            description="A transparent look at how GameRank Hub updates fit profiles, ranking hubs, and dates without pretending every minor patch changed the whole decision.",
            intro=(
                "A site can look busy by changing timestamps constantly, but that does not mean the information became more useful. Live-service games change often, yet not every change deserves a fresh headline or a new position in a decision hub.",
                "Our update model therefore separates material changes from surface churn. A page date should move because the reader-facing decision changed, the sources were materially rechecked, or a false statement needed correction—not because we wanted the page to look newer than it really is.",
            ),
            sections=(
                section_block(
                    "What earns a material update",
                    "A date changes when the page body needs new facts or a new recommendation frame. That includes platform-support changes, business-model shifts, a meaningful onboarding change, a major new-player route, or a revision to the fit conclusion itself.",
                    "On the hub pages, a ranking or grouping should change when the comparison between games changes. A fresh crossover skin or one weekly event is not enough. A new console launch, a new paid gate, or a big shift in onboarding probably is.",
                ),
                section_block(
                    "What does not move the date on its own",
                    "Typos, small wording cleanup, and tiny presentational edits do not automatically deserve a new public update date. They improve quality, but they do not pretend that the whole editorial judgment was re-run.",
                    "The same rule applies to many live-service patch notes. If a change affects a weapon number or one timed event without changing the player-fit decision, we would rather say less than overstate the importance of the patch.",
                ),
                section_block(
                    "Why ranking movement should be slower than patch noise",
                    "A decision hub is supposed to help a reader compare stable tradeoffs such as session length, social load, spending pressure, or onboarding burden. Those tradeoffs move slower than balance patches most of the time.",
                    "When lists bounce every week, the movement usually reflects editorial anxiety rather than reader value. We would rather keep a hub stable until the underlying comparison changed in a way a new player would actually notice.",
                ),
                section_block(
                    "How corrections differ from updates",
                    "A correction fixes a false or unclear fact as fast as possible even if the ranking, grouping, or date summary does not change much. The point is accuracy first, not drama.",
                    "This static preview does not publish a live correction inbox yet, so the public-facing correction route is still deferred to the About page before launch. That limit is part of the transparency too.",
                ),
            ),
            takeaways=(
                "Fresh dates should mean material editorial work, not cosmetic activity.",
                "A live-service patch matters only if it changes the decision the page is helping with.",
                "Comparison hubs should move slower than ordinary balance noise.",
                "Corrections and updates are related, but they are not the same editorial event.",
            ),
            conclusion="The goal is simple: a reader should be able to trust that a visible date means something. If a page looks updated, it should be updated for a reason that matters to the decision in front of them.",
            source_keys=("editorial",),
            extra_sources=(SourceRef("GameRank Hub update log", f"{BASE_URL}/updates.html"),),
            limitations=(
                "This preview cannot yet accept public correction submissions because the contact route is still unpublished.",
                "Some live-service changes happen between official checks, so a profile can still age between review dates.",
                "Ranking movement is editorial judgment, not a mathematical score that updates automatically.",
            ),
            visual_points=("Change dates honestly", "Move lists slowly", "Fix facts fast"),
        ),
        blog(
            slug="best-game-for-short-sessions",
            title="How to Choose a Game for Short Sessions That Still Feels Worth It",
            category="Discovery",
            summary="Use queue time, restart friction, interruption tolerance, and long-term goal fit instead of just looking at match length.",
            description="A practical article on choosing games for short sessions by looking past the advertised match timer and toward the real time cost around each play block.",
            intro=(
                "A short-session game is not simply a game with a short match timer. The real question is how much total friction sits around the part where you actually play: queues, load-in steps, party setup, warm-up needs, and whether the game punishes you for leaving after one round.",
                "That is why some games with five-minute matches still feel like commitment monsters, while others with longer individual activities remain easy to dip into. The full session envelope matters more than the marketing line.",
            ),
            sections=(
                section_block(
                    "Count setup and reset time, not only match length",
                    "A five-minute race or duel is only truly short if the queue, party flow, or restart loop stays clean. Trackmania works because resets are instant. Rocket League works because the match ends cleanly and the next one begins without a giant ritual.",
                    "By contrast, a game with a nominally short match can still waste your whole window if friends need ten minutes to link accounts, the queue pool is slow, or the loadout dance feels mandatory before every round.",
                ),
                section_block(
                    "Interruption tolerance matters more than most lists admit",
                    "Some short-session players need games they can stop between rounds with almost no penalty. Others can handle one longer match if the start and end points are clearly bounded. Knowing which type you are changes the right recommendation immediately.",
                    "Hearthstone, Fall Guys, and many Roblox experiences are easy to cut off cleanly. A longer match in TFT or a deep Destiny 2 activity can still work—but only if your real-life interruptions are predictable enough to let you finish.",
                ),
                section_block(
                    "Beware progression that turns short windows into chores",
                    "Short sessions feel worst when the game uses them only to maintain a streak. If the whole point of logging in is to clear dailies before they expire, the session may be technically brief and emotionally expensive.",
                    "That is why battle passes, resin, or event checklists matter to this choice. Fortnite can feel great in short bursts if you ignore the pass pressure. Genshin and Warframe can fit small windows too, but only if their long-term systems do not convert every login into homework for you.",
                ),
                section_block(
                    "Social load is its own time cost",
                    "A game that needs two friends, cross-play confirmation, voice setup, and a shared mood is not truly short-session friendly for every player even if the rounds themselves are brief.",
                    "If your available time is inconsistent, solo-friendly short games usually travel better than squad-dependent ones. That does not make the squad games worse; it just means their real session budget includes the people around them.",
                ),
            ),
            takeaways=(
                "A real short-session game has low setup, low reset friction, or both.",
                "Interruption tolerance is often more important than the listed match timer.",
                "Progression systems can make a short login feel like homework instead of relief.",
                "Social setup time counts as session length whether a list admits it or not.",
            ),
            conclusion="The best short-session game is the one that respects the whole shape of your evening. If the setup, pressure, or social coordination dwarfs the fun part, the clock on the match card never told the whole truth.",
            source_keys=("editorial",),
            extra_sources=(
                SourceRef("Trackmania official page", "https://www.ubisoft.com/en-us/game/trackmania/trackmania"),
                SourceRef("Rocket League official page", "https://www.rocketleague.com/"),
                SourceRef("Hearthstone official page", "https://hearthstone.blizzard.com/"),
                SourceRef("Fortnite official page", "https://www.fortnite.com/"),
            ),
            limitations=(
                "Short-session fit is highly personal because interruptions, family context, and skill comfort vary widely.",
                "Live-service games can change queue times and progression pressure after this article is published.",
                "This article compares decision patterns, not hands-on performance across every platform.",
            ),
            visual_points=("Queue time counts", "Restart friction", "Avoid homework loops"),
        ),
    ]
)

BLOG_POSTS.extend(
    [
        blog(
            slug="what-makes-a-good-free-game",
            title="What Makes a Free Game Actually Player-Friendly?",
            category="Analysis",
            summary="A free game earns trust when access is generous, monetization is legible, and the best loop still works when you spend nothing.",
            description="A practical framework for judging whether a free game is truly player-friendly, from access and onboarding to monetization clarity and return-player respect.",
            intro=(
                "The word free is descriptive but incomplete. A truly player-friendly free game does not only cost zero at the download button; it also explains what money changes, keeps the core loop enjoyable before payment, and lets you step away without feeling trapped by the next event timer.",
                "That is why two free games can feel completely different in practice. One uses optional cosmetics around a satisfying loop. Another uses free access mainly as the door into a store you must understand immediately. Player-friendly design is the difference.",
            ),
            sections=(
                section_block(
                    "A good free game still makes a complete first promise",
                    "The first sessions should already show why the game is worth your time. Fortnite, Rocket League, Brawlhalla, and many Roblox experiences succeed here because the core loop is visible before you spend.",
                    "A weaker free design hides the real game behind grind walls, unclear unlock pressure, or an onboarding path so thin that you cannot tell what you would actually be investing in.",
                ),
                section_block(
                    "Player-friendly monetization is legible",
                    "Free games become risky when you cannot quickly tell whether money buys cosmetics, convenience, access, or competitive advantage. Clarity matters even when you personally plan not to spend.",
                    "Genshin Impact shows why discipline and banner clarity matter. Warframe shows how convenience pressure can still be manageable if the underlying game is generous enough. The key question is always the same: what changes when money enters the picture, and is that change easy to understand?",
                ),
                section_block(
                    "Respect for breaks is part of fairness",
                    "A game that punishes absence too hard stops feeling generous even if the first download was free. Players need room to skip a season, miss a weekend, or return after a break without feeling that the game resents them.",
                    "Catch-up systems, evergreen content, and a playable core loop matter more than constant urgency. If the whole model relies on making you afraid to miss one week, the free access may be less friendly than it looks.",
                ),
                section_block(
                    "Safety and spending tools belong in the conversation",
                    "Parental controls, purchase friction, and clear account settings are not side topics. They are part of whether the game respects the player enough to make consent and boundaries possible.",
                    "This matters most in games with children, social spaces, or randomized spending. A generous game should still be judged on how responsibly it handles those surrounding systems.",
                ),
            ),
            takeaways=(
                "Free access is meaningful only if the core loop is enjoyable before spending.",
                "You should be able to explain exactly what money changes in the game.",
                "A player-friendly free game does not punish breaks so hard that logging out feels expensive.",
                "Safety tools and purchase friction are part of fairness, not separate from it.",
            ),
            conclusion="The most trustworthy free games are not the ones that cost the least money in theory. They are the ones that make the tradeoffs easiest to understand and the core experience easiest to enjoy without pressure.",
            source_keys=("editorial", "safety"),
            extra_sources=(
                SourceRef("Fortnite official page", "https://www.fortnite.com/"),
                SourceRef("Warframe official page", "https://www.warframe.com/"),
                SourceRef("Genshin Impact official page", "https://genshin.hoyoverse.com/"),
                SourceRef("The Sims 4 official page", "https://www.ea.com/games/the-sims/the-sims-4"),
            ),
            limitations=(
                "Player-friendly design can still feel different across regions, platforms, and age groups.",
                "Live-service monetization and catch-up systems can change faster than evergreen design fundamentals.",
                "This article evaluates fairness as a player decision, not as a legal or regulatory judgment.",
            ),
            visual_points=("Complete free start", "Clear monetization", "Skip without penalty"),
        ),
        blog(
            slug="before-you-download-a-new-game",
            title="Seven Checks Before You Download a New Game",
            category="Checklist",
            summary="Run through compatibility, time, social, spend, and accessibility checks before a big install or a one-night friend plan.",
            description="A practical pre-download article covering compatibility, time cost, social requirements, accessibility, spending model, update burden, and exit cost.",
            intro=(
                "Most bad downloads feel bad before the first real match. The signs were already there: unclear platform support, a bigger install than expected, a required launcher, a group plan that never actually fit everyone's setup, or a monetization model no one discussed until the store opened.",
                "A short pre-download checklist catches many of those surprises. You do not need to research forever. You just need enough information to know whether this game deserves the install, the account creation, and the first evening of your time.",
            ),
            sections=(
                section_block(
                    "Check compatibility and setup reality",
                    "Start with the boring facts: platform support, account requirements, storage, controller needs, anti-cheat, and whether your group is actually playing the same version. Cross-play assumptions are one of the fastest ways to waste a night.",
                    "If the setup is already annoying before the game begins, that friction becomes part of the recommendation. A fun loop cannot always repay a needlessly messy launch path.",
                    bullets=(
                        "Can your device really run the version your friends are using?",
                        "Will you need a publisher account or a second launcher?",
                        "Is the actual update size small enough for tonight's window?",
                    ),
                ),
                section_block(
                    "Check the session and social shape",
                    "A game that is perfect for a weekend group may be terrible for a Tuesday night alone. Match length, safe stop points, and whether the game expects a squad are all part of the download decision.",
                    "This is where fit profiles help most. They translate marketing blurbs into time, social, and commitment language you can compare honestly.",
                    bullets=(
                        "Can you stop after one match without feeling punished?",
                        "Does the game want a full group to feel good?",
                        "Will the first night be orientation or immediate competition?",
                    ),
                ),
                section_block(
                    "Check the business model before the honeymoon",
                    "A store is easier to judge before the game's excitement makes every bundle seem urgent. Free-to-play, passes, expansions, and access tiers all feel different once you know what they change.",
                    "The right download question is simple: if I like this game, what will it ask from me next—money, time, calendar attention, or all three?",
                    bullets=(
                        "Does money buy cosmetics, convenience, major content, or power-adjacent advantages?",
                        "Will the game still make sense if you spend nothing for the first month?",
                        "What happens if you like it but your friends stop playing?",
                    ),
                ),
                section_block(
                    "Check accessibility and exit cost",
                    "Look for subtitles, remapping, camera options, input support, and any known issue that could turn a fun idea into an avoidable barrier. Accessibility is part of fit, not a post-install luxury.",
                    "Then ask about exit cost. If the game disappoints, can you leave cleanly? Some titles are easy to uninstall and forget. Others leave behind subscriptions, group expectations, or sunk-cost pressure that deserve a second thought before you ever click download.",
                ),
            ),
            takeaways=(
                "Compatibility, time budget, social load, and spend model are all part of the same download decision.",
                "Cross-play and account assumptions deserve verification before the install finishes.",
                "A generous first session matters more than marketing scale or one flashy trailer.",
                "Exit cost is a real factor: know how easily you can stop if the fit is wrong.",
            ),
            conclusion="A smart download is not the one with the fewest questions. It is the one where you answered the right questions before the launcher made the decision for you.",
            source_keys=("setup", "safety", "wellbeing"),
            limitations=(
                "Platform terms, install sizes, and live-service bundles can change after publication.",
                "Accessibility and performance can still vary by device even when official support exists.",
                "This checklist reduces surprises; it does not replace reading the current official store and support pages for a specific title.",
            ),
            visual_points=("Compatibility", "Commitment", "Exit cost"),
        ),
    ]
)

GUIDES.extend(
    [
        guide(
            slug="browser-game-performance",
            title="How to Make Browser Games Run Better",
            category="Performance",
            summary="Make browser games smoother by attacking tabs, extensions, acceleration, and network clutter in the right order.",
            description="A practical browser-game performance guide with checklist, scenario, process, mistakes, success criteria, and sources.",
            quick_answer="Treat the browser like part of the game client: clear the extra load, test acceleration and extensions one by one, and compare in the same tab conditions.",
            introduction=(
                "Browser games compete with every other tab, extension, notification, and media stream you leave open. That makes performance troubleshooting messier than a single installed game where the client controls most of the environment.",
                "The upside is that the safest fixes are often simple: less tab clutter, fewer conflicting extensions, and a clean test of whether hardware acceleration helps or hurts the specific game you care about.",
            ),
            checklist=(
                "Update the browser and restart it cleanly before testing anything else.",
                "Close heavy media tabs, streams, or web apps that share the same browser process.",
                "Test once with extensions disabled or in a clean profile if the browser supports it.",
                "Check whether hardware acceleration is on and compare one state against the other.",
                "Use the same game, same scene, and same browser window size for every comparison.",
            ),
            checklist_note="A browser game can look unstable simply because the browser is carrying too much unrelated work. Good testing strips that background noise first.",
            scenario_title="When a no-download game runs worse than a fully installed game",
            scenario=(
                "Players often assume browser games should be lighter by default because they are smaller or easier to launch. In reality, a browser title can feel worse if the browser is juggling many tabs, extensions, or multimedia tasks at the same time.",
                "That makes the first useful question simple: does the game improve in a fresh, quiet browser state? If it does, you are solving browser overhead more than you are solving the game itself.",
            ),
            steps=(
                note("Isolate browser overhead", "Start with a clean session so you can tell whether the game is slow or the browser environment is overloaded."),
                note("Compare acceleration and extension states", "Some systems improve with hardware acceleration while others conflict with drivers, overlays, or specific browser features."),
                note("Keep the display conditions fixed", "Changing resolution, zoom, or window size can help, but only if you test them in a consistent way."),
                note("Retest after a full restart", "Browsers accumulate temporary junk and memory pressure. A clean restart is a legitimate part of the diagnosis."),
            ),
            follow_through="Once you find the smallest helpful fix, document it. Browser updates and extension changes can quietly undo the result later, and a note saves you from rediscovering the same answer from scratch.",
            mistakes=(
                note("Testing with twenty tabs still open", "The browser is a shared environment, so unrelated tabs can absolutely be the reason the game stutters."),
                note("Installing random cleaners or boosters", "Most of those tools explain little and add more variables than they solve."),
                note("Assuming lag is always the game's servers", "Input delay, browser hitching, and network issues can all feel similar unless you compare carefully."),
            ),
            success_criteria=(
                "The browser game stops hitching in the same scene that used to stutter.",
                "Input feel becomes more predictable because tab or extension overhead is reduced.",
                "You can explain whether acceleration helped, hurt, or simply changed nothing.",
                "The final fix is simple enough to repeat after an update or restart.",
            ),
            success_note="Better browser performance is often less dramatic than installed-game tweaking. The win is a quieter environment where the game stops competing with everything else you forgot was open.",
            source_keys=("browser",),
            limitations=(
                "School, work, or managed devices may block some browser settings or updates.",
                "Some web games are simply demanding and cannot be transformed by cleanup alone.",
                "Network issues and server load can still dominate the experience even after local cleanup.",
            ),
            visual_points=("Close tab clutter", "Test extensions", "Check acceleration"),
        ),
        guide(
            slug="healthy-gaming-setup",
            title="Healthy Gaming Setup: Comfort, Breaks, Audio and Posture",
            category="Wellbeing",
            summary="Make gaming easier on hands, back, eyes, and ears with small setup habits that survive real life.",
            description="A practical healthy gaming setup guide with checklist, scenario, process, mistakes, success criteria, and sources.",
            quick_answer="Set up for neutral posture, build in short movement and volume habits, and treat discomfort as useful feedback instead of something to outplay.",
            introduction=(
                "Performance advice that hurts your body is bad advice. A perfect sensitivity or frame rate is not actually successful if the setup leaves you tense, numb, or exhausted enough that the hobby becomes harder to enjoy.",
                "The goal is not a showroom desk. It is a boringly sustainable position, a reasonable audio level, and a few habits that still work on an ordinary weeknight when you are tired and tempted to skip the basics.",
            ),
            checklist=(
                "Place the screen and chair so your neck can stay neutral instead of craning forward.",
                "Keep wrists and shoulders in a position that does not force constant tension.",
                "Check headphone or speaker volume before the session gets loud enough to normalize excess.",
                "Plan short movement breaks instead of waiting until pain forces a long stop.",
                "Know which accessibility or remapping options reduce strain in the games you play most.",
            ),
            checklist_note="You do not need a perfect ergonomic lab. You need enough setup clarity that discomfort stops being invisible until it becomes a bigger problem.",
            scenario_title="When long sessions feel fine until the soreness shows up later",
            scenario=(
                "A lot of strain builds quietly. The first hour feels normal, the second feels competitive, and only afterward do the wrist, neck, or ears tell you the setup was costing more than you noticed in the moment.",
                "That delayed feedback is why structure matters. A planned volume check or movement break protects you better than relying on whether the current game is exciting enough to hide the warning signs.",
            ),
            steps=(
                note("Remove the obvious strain points", "Fix seat height, screen angle, wrist compression, and any audio default that is louder than it needs to be."),
                note("Plan the smallest possible break habit", "A one-minute stretch or stand-up interval is easier to keep than a heroic reset you never actually take."),
                note("Use easier inputs where possible", "Remaps, toggles, subtitles, or simplified interaction options can reduce strain without harming the experience."),
                note("Treat symptoms as information", "Pain, numbness, headaches, or hearing fatigue are data saying the setup needs help, not proof you should tough it out."),
            ),
            follow_through="A healthy setup pays off because it is repeatable. If the solution only works when you remember an elaborate ritual, it probably needs to be simplified again.",
            mistakes=(
                note("Locking into one posture for too long", "Even a decent posture becomes a problem if you freeze there for hours without movement."),
                note("Using volume to overpower a bad mix", "Louder is not the same as clearer, and ears do not warn you as loudly as sore muscles do."),
                note("Ignoring recurring symptoms because performance seems good", "Short-term results can hide long-term strain surprisingly well."),
            ),
            success_criteria=(
                "You finish sessions with less wrist, shoulder, neck, or ear fatigue.",
                "Breaks happen automatically enough that they do not require heroic self-control.",
                "Accessibility or remap choices feel like smart defaults, not admissions of failure.",
                "The setup is simple enough to maintain on an ordinary busy day.",
            ),
            success_note="The best healthy setup disappears into the background. You notice it mostly because the old aches or habits show up less often.",
            source_keys=("wellbeing",),
            limitations=(
                "This guide is not medical advice, and chronic symptoms deserve qualified professional help.",
                "Furniture, body size, disability, and room constraints change what a good setup looks like.",
                "Hearing, vision, or pain symptoms can have causes beyond the immediate gaming setup.",
            ),
            visual_points=("Neutral posture", "Plan micro-breaks", "Protect hearing"),
        ),
        guide(
            slug="how-we-review-games",
            title="How We Build a Game Fit Profile Without Pretending It Is a Scored Review",
            category="Editorial",
            summary="Understand how a sourced fit profile differs from a hands-on scored review and what evidence we publish on purpose.",
            description="An editorial methodology guide covering reader intent, official-source use, visible limitations, and why the old URL now points to a fit-profile process.",
            quick_answer="Start with the player's decision, use official sources for live facts, separate stable design from changeable service details, and publish the limits instead of hiding them.",
            introduction=(
                "This site used to generate generic review-style pages because the format was easy to repeat. The overhaul keeps the old URL for compatibility, but the method is different now: each page begins with the reader's decision rather than with a fake scored verdict.",
                "That means a game page should tell you what kind of player the game fits, what the first session is really asking for, what the business model does, and what facts may change after publication. It should never pretend we tested every platform hands-on when we did not.",
            ),
            checklist=(
                "Define the install or return-to-play question a real player is trying to answer.",
                "Collect official links for the game's live facts before drafting editorial interpretation.",
                "Separate stable design fit from changeable service details such as passes, rotations, and platform support.",
                "Publish a visible source section and a visible limitations section on the page itself.",
                "Use dates honestly so readers can see when the page was last materially checked.",
            ),
            checklist_note="Method beats volume here. A smaller number of clear, sourced profiles creates more trust than a larger number of generic pseudo-reviews that all sound alike.",
            scenario_title="When a live game changes season but the player-fit question stays the same",
            scenario=(
                "A battle pass update or new event can matter, but it does not automatically make the whole game a different fit for every reader. The profile should change when the decision context changes, not merely because a patch note exists.",
                "That is why the method separates the durable loop from the fast-moving service wrapper. Readers need both. They also need to know which side of the page is more likely to age first.",
            ),
            steps=(
                note("Start with the player's intent", "Ask what the reader is trying to decide: time fit, social fit, spending risk, onboarding burden, platform support, or something else."),
                note("Build page sections from game-specific fields", "Use structured fields such as session length, social shape, spending notes, and first-session plan so pages do not collapse into interchangeable boilerplate."),
                note("Write the limitations before you publish", "If you know what was not tested or what could change quickly, say so plainly rather than burying the uncertainty."),
                note("Move dates only with material updates", "A new timestamp should mean the body, source checks, or structured facts were meaningfully refreshed."),
            ),
            follow_through="The value of a fit profile is not that it sounds authoritative. It is that the reader can see why the conclusion exists, where the live facts came from, and where uncertainty still remains.",
            mistakes=(
                note("Writing verdict-first filler", "Generic praise or criticism that could apply to dozens of games is a sign the model is drifting back toward mass production."),
                note("Implying firsthand testing you did not do", "Authority collapses fast when a page sounds hands-on but cannot prove what was actually checked."),
                note("Hiding live-service volatility", "Battle passes, store terms, and platform features can change; pretending they are stable only makes the page less useful."),
            ),
            success_criteria=(
                "A reader can understand the game's likely fit in a few sections without reading generic filler.",
                "Official links and checked dates are visible instead of implied.",
                "The page explains what may change after publication.",
                "The title matches the real question being answered rather than defaulting to a boilerplate review formula.",
            ),
            success_note="Good editorial structure removes the need for fake certainty. The page becomes more useful because it is specific about what it knows and honest about what it cannot claim.",
            source_keys=("editorial",),
            limitations=(
                "A sourced fit profile is not a substitute for hands-on accessibility testing across every device or assistive need.",
                "Official pages are the best source for live terms, but they are also the place where changes can happen fastest.",
                "No one article format solves every decision, which is why related guides and hubs still matter.",
            ),
            visual_points=("Intent first", "Visible sources", "Publish limits"),
        ),
    ]
)

GUIDES.extend(
    [
        guide(
            slug="family-gaming-safety",
            title="Family Gaming Safety and Parental Controls Guide",
            category="Safety",
            summary="Set privacy, chat, time, and purchase controls before a child or teen explores public game spaces.",
            description="A family gaming safety guide with a setup checklist, household scenario, practical process, mistakes, success criteria, and source links.",
            quick_answer="Configure the account before the game session, explain how chat and reporting work, and revisit the rules whenever the game or child changes.",
            introduction=(
                "Gaming safety works best as a mix of settings and conversation. A perfect parental-control menu does not help much if the child has no idea why a setting exists or what to do when a social moment feels wrong.",
                "The goal is not to make every game risk-free. It is to reduce obvious exposure, slow down spending, and give a young player a simple script for what to do when something unexpected happens.",
            ),
            checklist=(
                "Set device-level and account-level family controls before the first public session.",
                "Require approval or friction for every purchase path, even if the game claims it is free.",
                "Walk through mute, block, and report tools together instead of assuming they are obvious.",
                "Create a short list of approved games or modes rather than relying on open discovery feeds.",
                "Explain one rule for friend requests and one rule for private messages in plain language.",
            ),
            checklist_note="This checklist moves the first conversation upstream. It is easier to explain limits before a favorite game or friend request makes the moment emotionally loaded.",
            scenario_title="When one new social game suddenly becomes the whole household's request",
            scenario=(
                "Popular social games often arrive as a bundle of questions: voice chat, purchases, age ratings, user-generated content, and group pressure from school or friends. Saying only yes or no rarely teaches much. A setup conversation does.",
                "That conversation should cover what the player can do on their own, what needs an adult, how to leave a bad interaction, and what kinds of spending or strangers are automatically off-limits in your house.",
            ),
            steps=(
                note("Configure the account first", "Privacy, communication, and spending controls are easiest to set before the child is already inside the game."),
                note("Preview the social surfaces together", "Show where chat lives, who can send requests, and how to leave a room or block a person."),
                note("Create small house rules", "Simple rules such as 'ask before accepting friend requests' work better than giant speeches."),
                note("Revisit after updates", "Games change, children change, and a setting that made sense last year may not fit the current version or maturity level."),
            ),
            follow_through="Good family safety is iterative. The settings reduce obvious risk, and the conversation teaches judgment that settings alone cannot provide.",
            mistakes=(
                note("Relying on one platform toggle", "A device setting helps, but many games add their own communication or store layers inside the app."),
                note("Talking about spending only after a purchase happens", "Store pressure works better against surprise than against a calm pre-game rule."),
                note("Assuming children will report discomfort immediately", "Many young players need permission and language to describe what felt wrong."),
            ),
            success_criteria=(
                "The child can show you where to mute, block, report, and leave without guessing.",
                "Purchases require an adult step or at least obvious friction.",
                "You know what game spaces are being visited and why they are acceptable.",
                "Rules still make sense after a patch, school trend, or new device enters the picture.",
            ),
            success_note="A safe setup is not the one with the most restrictions. It is the one that the household can actually understand, remember, and maintain after the first week.",
            source_keys=("safety",),
            limitations=(
                "User-generated spaces and live events change faster than any one checklist can track.",
                "Age ratings and legal expectations vary by region and platform.",
                "No tool catches every social risk, so judgment and follow-up conversations still matter.",
            ),
            visual_points=("Configure first", "Explain chat", "Review after updates"),
        ),
        guide(
            slug="crossplay-guide",
            title="Cross-Play Guide: Playing With Friends Across Platforms",
            category="Setup",
            summary="Check accounts, parties, and progression rules before assuming every version of a game can play nicely together.",
            description="A cross-play guide with checklist, friend-group scenario, practical process, mistakes, success criteria, and source links.",
            quick_answer="Treat cross-play, cross-progression, and cross-voice as three separate questions, then test them before the real game night.",
            introduction=(
                "Players often say \"the game has cross-play\" as if that answers everything. It does not. You still need to confirm who can party together, whether saves or purchases move with you, and which voice tools the group will actually use.",
                "Those details matter most when a mixed-platform group is excited and already waiting. A five-minute setup test ahead of time is much cheaper than a launch-night surprise.",
            ),
            checklist=(
                "Confirm which platforms the developer officially supports in the current version.",
                "Check whether input pools or ranked playlists separate players even when cross-play exists.",
                "Link publisher or game accounts early if the game requires them.",
                "Verify whether cosmetics, saves, or passes move across devices or stay locked to one platform.",
                "Agree on a backup voice or text plan before the first full session.",
            ),
            checklist_note="The most common failure is assuming that one successful login means the rest of the system will just work. Party, save, and voice rules are often separate.",
            scenario_title="When two friends own the same game on different devices and assume saves will follow",
            scenario=(
                "A lot of friction appears after the install. One friend launches on console, another on PC, and both assume their progress or purchases will simply appear because the publisher account is shared. That is not always true, and discovering it late turns a fun plan into support research.",
                "By testing party creation, one quick queue, and one progression check in advance, you learn what the group can rely on and what needs a fallback. That keeps expectations honest before money or time gets committed.",
            ),
            steps=(
                note("Verify the official support matrix", "Cross-play features are only real if the developer says the current version supports them for your platforms."),
                note("Link accounts before the big download ends", "If a publisher account is needed, set it up early while the stakes are low."),
                note("Run a five-minute party test", "Create the party, queue one low-pressure mode, and confirm invites, voice, and matchmaking all behave as expected."),
                note("Document what does not transfer", "Knowing that progress or cosmetics stay local is useful information if the group needs to choose a lead platform."),
            ),
            follow_through="A clean cross-play setup reduces social friction more than any one hardware upgrade. Once the group trusts the process, starting a session becomes ordinary again.",
            mistakes=(
                note("Assuming the same publisher means the same save rules", "Cross-play and cross-progression are often related but not identical features."),
                note("Ignoring region or input restrictions", "A group can technically play together and still land in a compromised playlist that one person hates."),
                note("Buying on multiple platforms before testing", "A short setup check can stop an expensive duplication mistake."),
            ),
            success_criteria=(
                "The group can invite, queue, and talk without last-minute troubleshooting.",
                "Everyone knows where progression and purchases do or do not carry over.",
                "There is a backup voice or chat option ready if the in-game tool fails.",
                "Choosing the lead platform for the group feels deliberate instead of accidental.",
            ),
            success_note="Cross-play success is really compatibility confidence. Once the group knows the boundaries, the feature stops being marketing language and starts being practical.",
            source_keys=("setup",),
            limitations=(
                "Developers can change cross-play and cross-progression rules after updates or regional launches.",
                "Ranked matchmaking and input-pool rules often remain more restrictive than casual modes.",
                "Platform-store refunds and entitlements are outside the control of general setup advice.",
            ),
            visual_points=("Queue together?", "Progress carries?", "Test voice backup"),
        ),
        guide(
            slug="cloud-gaming-guide",
            title="Cloud Gaming Guide for Beginners",
            category="Setup",
            summary="Use cloud gaming when convenience beats perfect latency, and know exactly where the tradeoffs start.",
            description="A cloud gaming guide with checklist, travel or low-spec scenario, decision process, mistakes, success criteria, and source links.",
            quick_answer="Test with a forgiving game first, check the network honestly, and treat cloud play as a convenience tool—not a universal replacement for local hardware.",
            introduction=(
                "Cloud gaming solves some real problems: storage limits, weak local hardware, and quick access on secondary devices. It also adds new constraints such as server distance, compression artifacts, and network dependency.",
                "The right question is not whether cloud gaming is good or bad. It is whether the convenience it gives you is worth the performance ceiling it imposes for the kinds of games you actually play.",
            ),
            checklist=(
                "Test the connection on the actual device and network you plan to use, not on a better one nearby.",
                "Confirm controller, keyboard, browser, or app support before you subscribe.",
                "Estimate data use and whether your connection is shared with other heavy traffic.",
                "Check which games are really in the library rather than assuming catalog parity.",
                "Choose one forgiving title for the first test instead of a twitch-sensitive competitive shooter.",
            ),
            checklist_note="This checklist turns cloud gaming into an honest comparison instead of a fantasy about perfect play from anywhere.",
            scenario_title="When you want to play a big live game on weak hardware or while traveling",
            scenario=(
                "Cloud play is tempting when your local device is underpowered or the install would eat too much storage. In those moments, the service feels like a shortcut around every problem. It is a shortcut around some of them, but never around latency itself.",
                "Testing with a lower-stakes title first reveals whether the connection is predictable enough for your habits. If the image stutters or the controls feel floaty there, a more demanding game will only exaggerate the problem.",
            ),
            steps=(
                note("Start with the connection, not the graphics", "Stable latency and low packet loss matter more than the marketing resolution target."),
                note("Pick the right first game", "A turn-based, solo, or slower-paced game gives you a fair baseline before you test higher-pressure genres."),
                note("Compare convenience against ownership", "A cloud catalog or subscription only helps if the games you care about are actually there and usable the way you want."),
                note("Know when local play is still better", "Fast shooters, unreliable travel Wi-Fi, or highly competitive play often expose the service ceiling quickly."),
            ),
            follow_through="Cloud gaming succeeds when you understand exactly what role it fills: backup device, travel option, quick access, or main platform for a specific slice of your library.",
            mistakes=(
                note("Evaluating from the best-case network only", "The home office connection might be perfect while your usual room or travel setup is not."),
                note("Testing a twitch shooter first", "If you lead with the hardest genre to satisfy, you learn only that the ceiling exists."),
                note("Ignoring recurring cost creep", "A cheap monthly service can overlap with several other subscriptions before you notice."),
            ),
            success_criteria=(
                "The controls feel predictable enough for the genres you actually play there.",
                "Visual artifacts stay within your tolerance instead of constantly distracting you.",
                "You know which games belong in the cloud and which should stay local.",
                "The subscription or service cost still feels sensible after the novelty wears off.",
            ),
            success_note="Cloud gaming becomes useful the moment you stop asking it to do everything. Once you assign it a clear role, the tradeoffs feel manageable instead of mysterious.",
            source_keys=("cloud",),
            limitations=(
                "Distance to servers and network quality set a hard ceiling that local tweaks cannot remove.",
                "Competitive latency demands may remain incompatible with your connection even if casual play is fine.",
                "Service libraries and device support can change after launch or region updates.",
            ),
            visual_points=("Connection first", "Convenience wins", "Not every genre fits"),
        ),
    ]
)

GUIDES.extend(
    [
        guide(
            slug="controller-settings-guide",
            title="Controller Settings Guide for New Players",
            category="Controls",
            summary="Tune dead zones, button layout, and aim behavior without rebuilding your controls every day.",
            description="A practical controller settings guide with checklist, scenario, process, mistakes, success criteria, and source links.",
            quick_answer="Fix reach and drift issues first, then make small response changes, and keep the setting long enough to judge it in normal play.",
            introduction=(
                "Controller settings usually go wrong in two ways: players leave obvious comfort problems unsolved, or they copy a high-level profile that assumes a different game, stick feel, hand size, or grip style. Both routes create frustration that looks like a skill problem.",
                "A useful controller setup makes common actions easier to repeat. It does not need to look impressive on paper or match what a creator posted last night.",
            ),
            checklist=(
                "Save or photograph the current layout before you change anything.",
                "Identify the real issue: stick drift, over-aiming, awkward button reach, fatigue, or camera speed.",
                "Check whether vibration, motion settings, or hold-versus-toggle options are distracting you.",
                "Use one repeatable training or low-pressure mode to compare changes.",
                "Keep a note of any remap that reduces hand strain even if it is not a popular layout.",
            ),
            checklist_note="Many controller problems are ergonomic before they are competitive. If a button is hard to reach or the stick never truly centers, no response curve can fully rescue it.",
            scenario_title="When you keep over-correcting and misfiring abilities under pressure",
            scenario=(
                "A lot of new players think they need a dramatic sensitivity shift when the real problem is layout conflict. They are lifting a thumb from the stick at bad moments, squeezing a trigger too late, or fighting drift that forces constant micro-corrections.",
                "Once those reach or hardware issues are reduced, smaller camera changes become easier to evaluate. You stop testing a dozen variables at once and start seeing which adjustment actually improved control.",
            ),
            steps=(
                note("Eliminate hardware noise first", "If the stick drifts or a trigger feels unreliable, set a sane dead zone or fix the hardware path before chasing fine tuning."),
                note("Solve reach and layout conflicts", "Move high-frequency actions to comfortable buttons before you touch advanced response options."),
                note("Adjust response in small steps", "Tiny changes to look speed, dead zone, or aim curve tell you more than dramatic jumps."),
                note("Test in a role you actually play", "A setting only matters if it works while you manage the real actions and pressure of your preferred mode."),
            ),
            follow_through="Once a layout solves a real problem, protect it from impulse editing. Muscle memory needs stability more than it needs novelty.",
            mistakes=(
                note("Copying a pro response curve blindly", "Top players optimize for their game, hardware, and hand habits—not yours."),
                note("Setting dead zones unrealistically low", "A tiny dead zone can feel precise for a minute and exhausting for a whole night if the stick never fully settles."),
                note("Ignoring fatigue because the setup is technically faster", "A good setting that hurts to use is not actually good for most players."),
            ),
            success_criteria=(
                "You misfire fewer abilities or accidental jumps because the layout matches your reach.",
                "Camera adjustments feel easier to predict rather than either sticky or wild.",
                "Longer sessions create less hand tension or thumb panic.",
                "You can keep the profile stable for several days without constant doubt.",
            ),
            success_note="The right controller setup feels ordinary during a match. That is success: your attention returns to decisions because the hardware stops demanding so much of it.",
            source_keys=("controls",),
            limitations=(
                "Controller quality varies, so two people using the same numbers may still get different results.",
                "Aim assist and response options are deeply game-specific.",
                "Persistent pain or numbness is a health issue and should not be treated as a pure settings experiment.",
            ),
            visual_points=("Fix reach first", "Small curve changes", "Comfort counts"),
        ),
        guide(
            slug="keyboard-mouse-basics",
            title="Keyboard and Mouse Basics for New PC Players",
            category="Controls",
            summary="Set up movement, aim, and keybind habits that make new PC play less awkward and much less tiring.",
            description="A practical keyboard-and-mouse guide with checklist, scenario, process, mistakes, success criteria, and source links.",
            quick_answer="Simplify your keybinds, keep important actions reachable, and separate movement comfort from advanced mechanical ambitions until the basics feel natural.",
            introduction=(
                "Switching from controller to keyboard and mouse often feels harder than the internet admits. The problem is not only the extra keys. It is learning to split movement, camera control, and utility timing across different parts of the body at once.",
                "The fastest way through that awkward phase is to reduce complexity. Reachable binds, calm mouse movement, and one consistent layout beat flashy advanced setups you cannot yet use under pressure.",
            ),
            checklist=(
                "Give yourself enough mouse space and a seat height that does not lock your wrist upward.",
                "Bind push-to-talk, ping, or map controls somewhere easy before team games begin.",
                "Keep the highest-frequency actions on easy keys rather than far reaches.",
                "Learn your reset keys for reload, interact, crouch, and inventory before adding extras.",
                "Save a screenshot of the initial layout so future experiments stay reversible.",
            ),
            checklist_note="The goal is to remove avoidable friction. If simple movement already feels awkward, adding fancy binds early only buries the real problem.",
            scenario_title="When a controller player keeps mis-hitting abilities on PC",
            scenario=(
                "The first temptation is to search for a famous bind setup. That rarely works because the player has not yet learned which fingers naturally own which jobs. What looks optimal on paper may still feel impossible in a real match.",
                "A calmer approach is to map only the actions you truly need, then practice moving, aiming, and one utility layer at a time. Once the base movement is automatic, extra binds become much easier to place intelligently.",
            ),
            steps=(
                note("Make the default map smaller, not larger", "Reduce duplicate or novelty binds until the core actions are obvious and easy to reach."),
                note("Train movement and camera separately at first", "A few quiet minutes of strafing, cornering, and menuing teaches more than rushing into a complex fight."),
                note("Use secondary binds for awkward stretches", "If an action is important but uncomfortable, a second accessible bind can be better than forcing a reach."),
                note("Add one advanced mechanic at a time", "Jumping straight into every lean, grenade, ping, wheel, and gadget shortcut slows the whole transition."),
            ),
            follow_through="After the layout feels stable, small refinements make sense. Before that, consistency matters more than theoretical optimization.",
            mistakes=(
                note("Copying esports binds verbatim", "A competitive setup built around years of habit may be actively unhelpful for a new PC player."),
                note("Putting too many actions on stretch keys", "If your hand has to search or strain, the bind is not actually efficient."),
                note("Practicing while your posture is bad", "A cramped seat or tiny mouse space can make the entire transition feel harder than it really is."),
            ),
            success_criteria=(
                "You can move, look around, and use the most important action keys without conscious search.",
                "Misinputs become rare enough that match mistakes feel understandable.",
                "The layout still feels usable after fatigue, not only in the first five minutes.",
                "You know which one or two advanced binds would be worth improving next.",
            ),
            success_note="The keyboard-and-mouse transition starts paying off when the inputs stop feeling like separate tasks. You do not need perfection. You need a baseline that no longer argues with you.",
            source_keys=("controls",),
            limitations=(
                "Keyboard size, hand size, and desk space change what counts as a reachable bind map.",
                "Different genres reward very different priorities for crouch, abilities, inventory, and map keys.",
                "Physical discomfort should be solved before you judge your potential on the input method itself.",
            ),
            visual_points=("Reachable binds", "Separate skills", "Posture matters"),
        ),
        guide(
            slug="free-to-play-spending",
            title="How to Enjoy Free-to-Play Games Without Overspending",
            category="Safety",
            summary="Enjoy live-service games with a plan for passes, packs, gacha, and convenience offers before emotion makes the choice for you.",
            description="A practical free-to-play spending guide with checklist, scenario, process, mistakes, success criteria, and source links.",
            quick_answer="Set a budget before you browse, know exactly what money changes, and add enough friction that purchases happen because you chose them—not because the store cornered you.",
            introduction=(
                "A free game is never truly free of incentives. The real question is whether its store, battle pass, pack system, or convenience layer fits your habits and your tolerance for friction.",
                "The safest spending plan is boring on purpose: a budget, a pause, and a rule for what kinds of purchases are acceptable. That dull structure protects you from high-emotion moments much better than willpower alone.",
            ),
            checklist=(
                "Set an entertainment budget before the season, banner, or event begins.",
                "Write down whether a purchase affects cosmetics, convenience, access, or actual power.",
                "Turn on password or approval friction for every payment route you can.",
                "Check the local-currency price instead of relying on funny-money store points only.",
                "Decide what counts as a stop condition: one pass, one skin, no randomized spending, or no repeat charges this month.",
            ),
            checklist_note="The point is to decide in a neutral moment. Stores are designed to make later moments feel more urgent, generous, or fleeting than they really are.",
            scenario_title="When a new season suddenly makes the store feel urgent",
            scenario=(
                "A live game often pairs new content with fear of missing out: exclusive skins, limited banners, expiring currencies, or progress tracks that only pay off if you start immediately. In that moment, the store stops feeling optional and starts feeling like part of the game loop.",
                "That is exactly when a written rule helps. If the purchase fits the budget and the category you already approved, buy it calmly. If not, the answer is already no, and you do not need a fresh emotional debate every time the store updates.",
            ),
            steps=(
                note("Wait one full session before buying", "A short pause separates real interest from frustration, hype, or social pressure."),
                note("Describe what the purchase actually changes", "If you cannot explain the value clearly, you are probably buying a feeling instead of a plan."),
                note("Compare recurring cost, not only one click", "A cheap monthly pass can become an expensive habit if you repeat it across several games."),
                note("Review after the event ends", "The best audit question is simple: did the purchase improve how you played, or only how you felt while buying?"),
            ),
            follow_through="A spending plan succeeds when missed offers no longer feel catastrophic. You should still be able to enjoy the game on the days you buy nothing at all.",
            mistakes=(
                note("Buying to fix frustration", "A rough losing streak or a confusing progression wall is a bad moment to decide what deserves money."),
                note("Treating sunk cost as proof you should keep going", "Past purchases do not obligate future purchases."),
                note("Ignoring randomized odds or bundle leftovers", "Leftover currencies and chance-based rewards are built to blur the real price."),
            ),
            success_criteria=(
                "You can explain why a purchase fit your plan in one sentence.",
                "Store updates do not force you into fresh budget decisions every time.",
                "The game remains enjoyable even when you skip a sale or event.",
                "You know which monetization models are personal red flags for you now.",
            ),
            success_note="Healthy free-to-play spending is not about never paying. It is about knowing why you paid, what changed, and whether the game still works for you when the answer is no.",
            source_keys=("safety",),
            limitations=(
                "Household rules and legal protections vary by region and payment provider.",
                "Children and teens need account-level safeguards beyond simple personal discipline.",
                "Compulsive spending patterns may need help beyond general gaming advice.",
            ),
            visual_points=("Budget first", "Know the model", "Add friction"),
        ),
    ]
)

GUIDES.extend(
    [
        guide(
            slug="reduce-input-lag",
            title="How to Reduce Input Lag Safely",
            category="Performance",
            summary="Lower end-to-end latency by removing obvious bottlenecks before chasing risky tweaks or misinformation.",
            description="A practical input-lag guide with checklist, scenario, safe process, mistakes, success criteria, and sources.",
            quick_answer="Check the display chain, frame cap, controller path, and background load first. Only then decide whether the delay is local, network-based, or simply low frame rate masquerading as lag.",
            introduction=(
                "Input lag is a chain, not one setting. Display mode, refresh rate, frame pacing, controller polling, USB behavior, wireless conditions, and network stability can all contribute a piece of the delay you feel.",
                "That is why \"one weird trick\" advice ages badly. The safe path is to locate the slow part of the chain and fix it directly instead of piling on unsupported registry edits or risky software claims.",
            ),
            checklist=(
                "Write down the symptom: delayed camera, late shots, muddy menu response, or online desync.",
                "Confirm your display is running at the refresh rate you think it is using.",
                "Note whether the problem appears with both controller and mouse or only one input path.",
                "Pause large downloads, overlays, or capture tools before you test.",
                "Set aside one repeatable action such as a flick, jump, or menu timing check for comparison.",
            ),
            checklist_note="This step turns a feeling into a chain of suspects. Without that, every tweak competes to explain the same vague frustration.",
            scenario_title="When the game feels late even though the FPS counter looks fine",
            scenario=(
                "High average FPS can still feel sluggish if frame time is uneven, the display is running in the wrong mode, or the network is the real bottleneck. Players often keep lowering graphics because that is the most visible control they have, even when it is not the layer causing the delay.",
                "A better test is to separate local responsiveness from server response. Menu navigation, camera turns, and private training modes reveal local issues. Late hit registration or rubber-banding point toward network conditions instead.",
            ),
            steps=(
                note("Fix the display path first", "Use the intended refresh rate, correct fullscreen mode for the game, and supported sync options before touching fringe tweaks."),
                note("Align frame pacing with the display", "A sane frame cap or performance preset can feel better than unstable peaks that constantly collide with the refresh ceiling."),
                note("Reduce input-path noise", "Test a direct-wired controller or stable mouse connection so wireless quirks or hubs are not hiding in the chain."),
                note("Separate local delay from online delay", "If menus feel crisp but fights do not, the next investigation belongs to your network, region, or server conditions rather than your render path."),
            ),
            follow_through="Keep the smallest set of changes that made the input feel cleaner and reverse the rest. A shorter settings trail is easier to maintain and much easier to explain if support becomes necessary.",
            mistakes=(
                note("Confusing low FPS with pure input lag", "A game can feel delayed because frames arrive unevenly, not because a secret latency toggle is wrong."),
                note("Turning off security or applying unsupported system hacks", "Unsafe advice can create bigger problems than the latency you were trying to solve."),
                note("Testing only online matches", "You need at least one local-feeling reference point to know whether the problem belongs to the game client or the network."),
            ),
            success_criteria=(
                "Menu and camera response feel more immediate in a repeatable comparison task.",
                "The fix is stable under normal play, not only in a sterile test range.",
                "You understand whether the remaining issue is local, network, or both.",
                "The final setup uses supported settings you can recreate later.",
            ),
            success_note="The best result is clarity as much as speed. Even if you do not eliminate every millisecond, you should know which layer is still limiting the experience and avoid magical thinking about the rest.",
            source_keys=("performance",),
            limitations=(
                "Cloud gaming and long-distance server routing set a hard floor that local tweaks cannot erase.",
                "Console menu names and performance options differ from PC even when the principles are similar.",
                "Persistent crashes, overheating, or electrical issues are support problems, not latency-tuning puzzles.",
            ),
            visual_points=("Refresh first", "Cap sanely", "Avoid risky tweaks"),
        ),
        guide(
            slug="multiplayer-beginner-checklist",
            title="Multiplayer Beginner Checklist: Your First Ten Matches",
            category="Teamwork",
            summary="Use your first ten matches to learn the objective, map flow, and recovery habits before you obsess over stats.",
            description="A practical first-ten-matches guide with checklist, scenario, process, mistakes, success criteria, and source links.",
            quick_answer="Define success as understanding the mode, not proving your talent. Learn one map or mode, use pings early, and leave each session with one concrete next question.",
            introduction=(
                "Beginners often judge themselves before they understand what the match is asking for. That creates bad habits fast: unnecessary settings changes, role swapping after every loss, and frustration rooted in confusion rather than in performance.",
                "A better start treats early matches as orientation. Your job is to understand the win condition, the pace of danger, and the safe default action when you are unsure—not to prove that you belong in the lobby already.",
            ),
            checklist=(
                "Know how the round, race, or objective actually ends before you care about individual score lines.",
                "Play one mode or map repeatedly instead of trying to learn the whole game at once.",
                "Turn on or learn the game's pings, subtitles, and objective markers early.",
                "Set one tiny mechanical goal per session such as movement, recoil control, or timing.",
                "End each play block by writing down one question the game still did not answer clearly.",
            ),
            checklist_note="This checklist keeps the first ten matches narrow enough to learn from. If every match has a different role, map, and goal, nothing sticks.",
            scenario_title="Your first group night in a game everyone else already knows",
            scenario=(
                "Joining friends who know the game can feel efficient, but it also creates pressure to copy their pace before you understand the basics. That often leads to silent following, panic deaths, and no memory of why the strong players moved the way they did.",
                "The fix is to ask for one stable assignment: hold this lane, follow this route, ping this target, revive only when safe. A narrow job lets you see the shape of the game without pretending you can already do every job on the team.",
            ),
            steps=(
                note("Define the win condition first", "If you cannot explain what ends the round or how progress is measured, every personal stat becomes misleading."),
                note("Shadow one dependable pattern", "Follow a reliable route, teammate, or role long enough to understand why it works before improvising."),
                note("Add only one mechanical focus", "Trying to improve recoil, communication, map memory, and abilities all at once hides the real lesson."),
                note("Leave with one next-step question", "A good beginner session ends with a clear curiosity, not with a vague feeling of being overwhelmed."),
            ),
            follow_through="After ten matches, review what became clearer on its own and what still required outside explanation. That split tells you whether the game is onboarding you reasonably or expecting too much self-teaching for your taste.",
            mistakes=(
                note("Jumping into ranked immediately", "Ranked pressure magnifies confusion and tempts you to treat every early loss as proof you picked the wrong game."),
                note("Changing role or class every time you die", "Constant role swapping makes the entire game feel random even when it is not."),
                note("Talking about blame instead of information", "New players learn faster from pings, timing, and position calls than from emotional post-mortems in the middle of the round."),
            ),
            success_criteria=(
                "You can explain the win condition and one safe default action when you are uncertain.",
                "You survive longer because you recognize danger and spacing earlier.",
                "You know which role, mode, or weapon you want to explore next instead of feeling equally lost everywhere.",
                "The game feels less noisy because key information has started to stand out.",
            ),
            success_note="A successful first ten matches do not make you look advanced. They make the game intelligible enough that the eleventh match teaches you something instead of merely overwhelming you again.",
            source_keys=("teamwork",),
            limitations=(
                "Each game has its own vocabulary, timers, and community culture, so this checklist stays intentionally general.",
                "Toxic lobbies may require mute, block, or group-only play before the advice here can work well.",
                "Accessibility needs may change which mode or role is the true beginner-friendly option for you.",
            ),
            visual_points=("Learn the objective", "One mode first", "Review one mistake"),
        ),
        guide(
            slug="clear-team-communication",
            title="Clear Team Communication Without Overcalling",
            category="Teamwork",
            summary="Make comms useful by sharing facts, timing, and intent without narrating every thought.",
            description="A practical communication guide with checklist, scenario, process, mistakes, success criteria, and sources for groups that want calmer multiplayer calls.",
            quick_answer="Say what changed, where it matters, and what action follows. If the call does not help the team act now, save it for downtime.",
            introduction=(
                "Most team communication problems are not about courage. They are about relevance. Players either say too little when action is needed or narrate everything, flooding the channel with details that no one can use in time.",
                "Clear comms are usually short, factual, and tied to the next action. Good teams are not silent because they know everything already. They are concise because they respect how little attention is available during a live fight.",
            ),
            checklist=(
                "Agree on simple place names or use the game's official callout language if it exists.",
                "Decide who should call rotates, ult plans, or resets when several people notice the same thing.",
                "Use pings as backup, not as a replacement for every verbal call.",
                "Cut dead talk after you lose agency in the round unless the game specifically needs your information.",
                "Review communication problems after the fight, not in the middle of it.",
            ),
            checklist_note="The aim is not perfect language. It is a shared minimum structure that stops every fight from turning into five private monologues.",
            scenario_title="When three teammates talk at once the instant the plan breaks",
            scenario=(
                "Chaos often begins when the team is already under pressure. One player calls damage, another calls a flank, a third complains that no one followed, and the only useful detail gets buried under urgency. The result feels like a communication failure even though everyone technically spoke up.",
                "A better response is to cut the call into action-sized pieces: one enemy close left, rotate now, hold ult, back out. Those phrases are small enough to act on and short enough that another useful call can still fit after them.",
            ),
            steps=(
                note("Call the change, not the whole story", "Say what is different: one flank, one cooldown spent, one site open, one revive unsafe."),
                note("Pair information with intent", "A good call often ends with what you want next: push, hold, back, trade, wait, rotate."),
                note("Hand off after death or loss of control", "Once you are spectating, keep only the information the living players still need."),
                note("Debrief in the gap, not in the fire", "Long explanations belong after the fight, when teammates can process them without dying for your timing."),
            ),
            follow_through="The real test is whether your calls make teammates easier to predict. If the group starts moving earlier and second-guessing less, the language is probably becoming useful.",
            mistakes=(
                note("Blaming during the round", "Emotion crowds out the exact information teammates need to recover or convert a fight."),
                note("Calling details with no decision attached", "Damage numbers, ult percentages, or pathing notes matter only if they change the next action."),
                note("Talking after you lost agency", "Dead players often over-narrate because they have more attention available than the people still alive."),
            ),
            success_criteria=(
                "Teammates react faster because the call already contains the next action.",
                "Important pings and short voice calls reinforce each other instead of competing.",
                "The group spends less time arguing about what happened in the middle of live rounds.",
                "You can tell when silence is better than another sentence.",
            ),
            success_note="The best communication often feels boring. That is a compliment. Predictable, compact calls free attention for aim, movement, and decision-making instead of stealing it.",
            source_keys=("teamwork",),
            limitations=(
                "Random teammates may not share language, patience, or interest in structured comms.",
                "Some games lean harder on ping systems than live voice, so the right balance varies.",
                "Accessibility or comfort needs can change whether speaking, pinging, or text is the better default.",
            ),
            visual_points=("Facts not blame", "Action plus timing", "Debrief later"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="eve-online",
            name="EVE Online",
            genre="Space MMO",
            official_url="https://www.eveonline.com/",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free Alpha access with optional Omega subscription and premium services.",
            session_length="20 minutes to several hours, plus out-of-game planning if you go deep.",
            session_bucket="long",
            play_style="player-driven economy and corporation strategy",
            hub_group="progression",
            core_loop="Choose a role in a player-shaped economy, fly ships you can afford to lose, and let knowledge plus social ties become the real progression.",
            best_for="players who want a player-driven economy, corporations, and real risk attached to decisions",
            not_for="players who want fast onboarding, low-loss consequences, or simple menus",
            learning_barrier="EVE is very high-friction up front because economy, navigation, fitting, and social context all matter together.",
            social_shape="You can explore solo, but the strongest stories and progression usually come from corporations and coordinated groups.",
            progression_notes="Ships are tools, not the final goal; the real progression is knowledge, industrial reach, and social position.",
            spending_notes="Alpha access lets you sample, while Omega and optional services deepen the hobby if the wider game sticks.",
            first_session_plan=(
                "Finish the official career-agent path before deciding whether the menus are a deal-breaker.",
                "Join a new-player-friendly corporation before buying into giant ambitions.",
                "Fly ships you can afford to lose so fear does not distort every lesson.",
                "Judge the fit by whether the social strategy sounds exciting, not by how pretty the first mining session looks.",
            ),
            fit_questions=(
                "Do you enjoy social strategy as much as direct combat?",
                "Are meaningful losses exciting to you or simply stressful?",
                "Will out-of-game planning feel like homework or like part of the game?",
            ),
            source_label="EVE Academy",
            source_url="https://www.eveonline.com/eve-academy",
            title="EVE Online Before You Play: A Fit Guide for Corporation-Driven Space Strategy",
            description="Read this sourced EVE Online fit profile before you commit to its corporation focus, economy depth, Alpha/Omega model, and real-loss tension.",
            summary="EVE Online fits niche players who enjoy spreadsheets, politics, logistics, and accepting losses as part of the story.",
            onboarding_notes="The right question is not 'Can I play this tonight?' but 'Do I want to learn a social simulation with ships attached?' That makes EVE a narrow but powerful fit.",
            commitment_notes="Even if daily play is short, successful long-term involvement usually means reading, planning, or coordinating outside the client.",
            what_can_change=(
                "Omega value and pack offers can change the sampling-to-hobby transition.",
                "Warfare balance and alliance politics can reshape what types of corporation play feel accessible.",
                "Tutorial tools may improve or change what the first hours emphasize.",
            ),
            review_hub_summary="Best for players who want economy, corporations, and high-consequence decisions more than accessibility.",
            related_guides=("multiplayer-beginner-checklist", "free-to-play-spending"),
            visual_points=("20+ min", "Corporation-heavy", "Alpha + Omega"),
        ),
        game(
            slug="dauntless",
            name="Dauntless",
            genre="Cooperative action RPG",
            official_url="https://playdauntless.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch"),
            platform_tags=("pc", "playstation", "xbox", "switch"),
            business_model="Free-to-play boss-hunt game with cosmetic and pass-based monetization.",
            session_length="10-25 minute hunts that are easy to schedule with friends.",
            session_bucket="short",
            play_style="repeatable co-op boss hunts",
            hub_group="progression",
            core_loop="Hunt a behemoth, learn its tells, craft upgrades, and repeat with different weapons or targets.",
            best_for="players who want approachable co-op hunts without Monster Hunter's heavier upfront complexity",
            not_for="players who need huge encounter variety or deep long-term worldbuilding",
            learning_barrier="Dauntless is easy to understand at the hunt level, though weapon mastery and progression choices still take time.",
            social_shape="The game is comfortable solo or in drop-in co-op, which lowers the scheduling pressure.",
            progression_notes="Behemoth hunts, weapon paths, and crafted gear form a clean repeatable loop.",
            spending_notes="Core access is free. Cosmetics and seasonal extras are the main monetized layers.",
            first_session_plan=(
                "Test two weapon types before investing emotionally in one style.",
                "Learn one behemoth tell at a time instead of reading every effect in one sitting.",
                "Use early hunts to practice survival and parts, not speedrunning.",
                "Keep social expectations casual until everyone understands revives and upgrade pacing.",
            ),
            fit_questions=(
                "Do you want co-op boss hunts without a giant rulebook up front?",
                "Is repetition a positive because it creates mastery, or a warning sign for your taste?",
                "Would you rather schedule 15-minute hunts than 90-minute raids?",
            ),
            source_label="Official game overview",
            source_url="https://playdauntless.com/game/",
            title="Dauntless Before You Play: A Fit Guide for Co-op Hunt Sessions",
            description="Use this sourced Dauntless fit profile to weigh short co-op hunts, repetitive progression, and cosmetic monetization before you install.",
            summary="Dauntless fits players who want repeatable boss-hunt sessions that are easy to schedule with friends.",
            onboarding_notes="The fit is clear fast because the hunt loop is easy to understand. The real question is whether repeating that loop feels satisfying enough without a more sprawling RPG shell around it.",
            commitment_notes="Sessions are neat and short, but long-term retention depends on whether you enjoy farming the same core activity.",
            what_can_change=(
                "Event cadence and pass rewards can change how much short-term novelty the game offers.",
                "Weapon or gear balance can alter which options feel welcoming to beginners.",
                "Platform-support features such as account linking should be rechecked on live official pages.",
            ),
            review_hub_summary="A clean fit for groups who want straightforward co-op hunts and do not need a giant long-form RPG around them.",
            related_guides=("multiplayer-beginner-checklist", "crossplay-guide"),
            visual_points=("10-25 min", "Drop-in co-op", "Cosmetics + pass"),
        ),
        game(
            slug="world-of-tanks",
            name="World of Tanks",
            genre="Vehicle combat",
            official_url="https://worldoftanks.com/",
            platforms=("PC", "Console editions", "Mobile variants"),
            platform_tags=("pc", "playstation", "xbox", "mobile"),
            business_model="Free-to-play vehicle combat game with premium time, convenience offers, and optional vehicle purchases.",
            session_length="5-15 minute matches that can quietly chain into longer progression sessions.",
            session_bucket="short",
            play_style="slow tactical team combat",
            hub_group="competitive",
            core_loop="Use armor, vision, and map lanes well enough to win a few decisive engagements and keep a tank line progressing.",
            best_for="players who like slow tactical vehicle combat, spotting mind games, and historical machine flavor",
            not_for="players who want fast twitch movement or a very simple free-to-play economy",
            learning_barrier="Armor angles, view range, map lanes, and class roles all matter enough that early matches can feel harsh without context.",
            social_shape="The game is playable solo, though platoons make focus fire and map control easier to coordinate.",
            progression_notes="Grinding new lines, crews, and vehicle mastery is central to the long-term loop.",
            spending_notes="Core access is free, but premium time, convenience, and vehicle offers are part of the live economy pressure.",
            first_session_plan=(
                "Start with one nation and one class so the tech tree stays understandable.",
                "Learn spotting and basic lane discipline before chasing damage numbers.",
                "Watch how armor angles worked after each death instead of writing losses off as matchmaking alone.",
                "Avoid buying premium vehicles until the base pace and economy truly click for you.",
            ),
            fit_questions=(
                "Do you enjoy slow map control and information games more than rapid flanking speed?",
                "Will convenience offers bother you if the base tactics are excellent?",
                "Are vehicle classes and historical flavor more appealing than hero abilities or pure infantry shooters?",
            ),
            source_label="Official game guide",
            source_url="https://worldoftanks.com/en/content/guide/",
            title="World of Tanks Before You Play: Is It a Fit for Slow Tactical Vehicle Battles?",
            description="This sourced World of Tanks fit profile helps you weigh slow tactical pacing, tech-tree grind, and premium-time pressure before you commit.",
            summary="World of Tanks fits deliberate players who enjoy positioning and class roles more than speed.",
            onboarding_notes="The crucial fit question is whether patient setup and information denial sound fun. If you want immediate flanking speed, the pace can feel restrictive no matter how much you like tanks.",
            commitment_notes="Matches are fairly short, but understanding lines, crews, and the economy turns it into a bigger hobby over time.",
            what_can_change=(
                "Vehicle balance and tech-tree routes can change which lines are easiest for newcomers.",
                "Event progression can temporarily increase grind or reward pressure.",
                "Premium offers and time savers move more often than the core tactical pacing.",
            ),
            review_hub_summary="Best for players who enjoy deliberate tactical pacing and can keep premium offers in perspective.",
            related_guides=("free-to-play-spending", "multiplayer-beginner-checklist"),
            visual_points=("5-15 min", "Solo or platoon", "Premium time"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="guild-wars-2",
            name="Guild Wars 2",
            genre="Online role-playing game",
            official_url="https://www.guildwars2.com/",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free base access with paid expansions and optional convenience purchases.",
            session_length="20 minutes to several hours, depending on whether you want open-world events or deeper progression blocks.",
            session_bucket="flex",
            play_style="exploration-forward MMO",
            hub_group="progression",
            core_loop="Roam events, complete story or exploration goals, and gradually open more account-wide systems like mounts, elite specs, and collections.",
            best_for="players who want an MMO with flexible grouping and less subscription pressure",
            not_for="players who need a simple quest flow or a tiny set of systems",
            learning_barrier="Early play is welcoming, but gear tiers, masteries, mounts, and endgame systems create a wide information spread over time.",
            social_shape="Guild Wars 2 is easy to play solo in open-world events, while guilds and friends make structured endgame much easier to approach.",
            progression_notes="Leveling is only the first layer; elite specializations, map metas, mounts, and collections deepen the long-term loop.",
            spending_notes="The base entry is generous, but expansions and convenience items unlock much of the larger progression arc.",
            first_session_plan=(
                "Pick a profession theme you actually like instead of optimizing for endgame before you know the world.",
                "Follow hearts and events together rather than speed-running alone through every marker.",
                "Bank crafting clutter you do not yet understand instead of letting systems overwhelm your first evening.",
                "Ignore endgame optimization until the level-up and exploration loop proves it is interesting to you.",
            ),
            fit_questions=(
                "Do you want MMO social energy without a subscription clock?",
                "Are you happy exploring and joining events rather than racing to fixed dungeons?",
                "Will many side systems feel rich or simply too wide for your available time?",
            ),
            source_label="Official new player guide",
            source_url="https://www.guildwars2.com/en/new-player-guide/",
            title="Guild Wars 2 Before You Play: A Fit Guide for Flexible MMO Explorers",
            description="Use this sourced Guild Wars 2 fit profile to weigh free base access, exploration-first MMO design, and expansion-gated progression before you start.",
            summary="Guild Wars 2 fits players who want a cooperative MMO that usually lets them join the crowd without strict role queues.",
            onboarding_notes="The fit is strongest if open-world exploration and spontaneous event participation sound attractive. It is weaker if you want a heavily directed, linear quest treadmill from the very first zone.",
            commitment_notes="You can make steady progress in short chunks, but the broader account systems still reward a long relationship with the game.",
            what_can_change=(
                "Expansion bundles and seasonal content packaging can alter the value equation.",
                "Class balance may change which professions are easiest for first-time players.",
                "Event cadence can shift how lively certain maps feel at any given time.",
            ),
            review_hub_summary="A strong fit for players who want cooperative MMO energy without mandatory subscription pressure.",
            related_guides=("multiplayer-beginner-checklist", "free-to-play-spending"),
            visual_points=("20+ min", "Solo or guild", "Free base + expansions"),
        ),
        game(
            slug="lost-ark",
            name="Lost Ark",
            genre="Online action RPG",
            official_url="https://www.playlostark.com/",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free-to-play online action RPG with optional convenience spending and account-wide progression layers.",
            session_length="30 minutes to several hours, especially once raids and roster systems matter.",
            session_bucket="long",
            play_style="ARPG combat inside an MMO schedule",
            hub_group="progression",
            core_loop="Push story or raids forward, hone gear, and manage roster-wide systems that reward regular return play.",
            best_for="players who like sharp isometric combat and do not mind layered endgame systems",
            not_for="players who want a simple casual ARPG or zero schedule pressure",
            learning_barrier="Combat is readable, but currencies, engravings, alts, and roster systems make the endgame much denser than the opening hours suggest.",
            social_shape="Story play can be solo, while raids and endgame participation become the bigger long-term draw.",
            progression_notes="Roster growth, gear honing, alts, and scheduled activities are central to the long-term game.",
            spending_notes="Free entry exists, but progression convenience and cosmetics can create pressure if you start chasing efficiency.",
            first_session_plan=(
                "Finish the early story without alt anxiety or endgame spreadsheets open beside you.",
                "Save paid currency until you understand which roster pressures actually matter.",
                "Separate 'fun build' goals from 'efficient raid prep' goals so the game stays readable.",
                "Look for beginner-friendly learning groups before you let raid expectations define the whole game.",
            ),
            fit_questions=(
                "Do you enjoy ARPG combat enough to live with MMO chores around it?",
                "Will alt-based progress feel clever or simply tiring?",
                "Are you comfortable with a live economy constantly talking about efficiency?",
            ),
            source_label="Official classes overview",
            source_url="https://www.playlostark.com/en-us/game/classes",
            title="Lost Ark Before You Play: A Fit Guide for Action Combat and Scheduled Endgame",
            description="Read this sourced Lost Ark fit profile before you commit to its flashy combat, roster systems, and schedule-heavy endgame structure.",
            summary="Lost Ark fits players who want flashy combat inside an MMO-style economy and schedule.",
            onboarding_notes="The central fit question is whether you want the combat enough to tolerate the live-service scaffolding around it. Players who only want the story often stop early. Players who love the combat usually decide whether the endgame structure is a deal-breaker later.",
            commitment_notes="Lost Ark can turn into a calendar hobby faster than the leveling game suggests, especially if you care about raids or keeping pace.",
            what_can_change=(
                "Catch-up events and honing incentives can shift the new-player experience dramatically.",
                "Class releases and balance updates can change what feels approachable.",
                "Regional service policies and monetization framing may evolve over time.",
            ),
            review_hub_summary="Best for players who want great isometric combat and can tolerate layered endgame systems and schedule pressure.",
            related_guides=("free-to-play-spending", "multiplayer-beginner-checklist"),
            visual_points=("30+ min", "Solo then raids", "Convenience pressure"),
        ),
        game(
            slug="runescape",
            name="RuneScape",
            genre="Online role-playing game",
            official_url="https://www.runescape.com/",
            platforms=("PC", "Mobile"),
            platform_tags=("pc", "mobile"),
            business_model="Free entry with membership unlocking much of the fuller experience.",
            session_length="10 minutes to several hours across quests, skills, and long-term account goals.",
            session_bucket="flex",
            play_style="open-ended account progression",
            hub_group="progression",
            core_loop="Quest, train skills, and set personal goals that slowly turn into a persistent account identity.",
            best_for="players who want open-ended goals, account persistence, and lots of low-intensity activities",
            not_for="players who need cutting-edge presentation or a narrow focused loop",
            learning_barrier="RuneScape's interface and decades of accumulated systems can feel wide and old-school before they feel liberating.",
            social_shape="It works solo, socially, or half-passively depending on what you are doing and how intensely you want to engage.",
            progression_notes="Skill levels, quests, gear, and self-set projects make progression durable even when you switch activities often.",
            spending_notes="The free layer is real, but membership is the gateway to much of what long-term players value most.",
            first_session_plan=(
                "Follow the introductory quest path instead of wandering until every menu feels equally important.",
                "Choose two skills you honestly enjoy so early progress feels personal rather than obligatory.",
                "Use pathing aids and tooltips until the interface stops fighting you.",
                "Treat membership as a later decision rather than a day-one purchase.",
            ),
            fit_questions=(
                "Do you value persistent progress more than fast spectacle?",
                "Will a legacy-style interface annoy you before the systems can pay it back?",
                "Do you want a game that can be played in calm, low-intensity windows at times?",
            ),
            source_label="Official game guide",
            source_url="https://www.runescape.com/game-guide",
            title="RuneScape Before You Play: Is It a Fit for Open-Ended Long-Term Progress?",
            description="Use this sourced RuneScape fit profile to judge free entry, membership value, legacy interface friction, and open-ended progression before you begin.",
            summary="RuneScape fits players who like steady account growth and self-directed projects more than sharp match-based competition.",
            onboarding_notes="The game is easiest to judge through quests and a couple of skills, not by graphics alone. If slow, persistent progress sounds relaxing, RuneScape can be remarkably sticky.",
            commitment_notes="RuneScape can fill tiny breaks or huge long-term projects, which is both its strength and its biggest commitment risk.",
            what_can_change=(
                "Membership bundles and bond value can change how generous the free layer feels.",
                "Seasonal events may shift what new players notice first.",
                "Tutorial or interface improvements can reduce some early friction over time.",
            ),
            review_hub_summary="A durable fit for players who want account persistence and self-directed goals more than modern presentation.",
            related_guides=("free-to-play-spending", "healthy-gaming-setup"),
            visual_points=("10 min to hours", "Solo or clan", "Membership matters"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="efootball",
            name="eFootball",
            genre="Football simulation",
            official_url="https://www.konami.com/efootball/",
            platforms=("PC", "PlayStation", "Xbox", "Mobile"),
            platform_tags=("pc", "playstation", "xbox", "mobile"),
            business_model="Free-to-play football game with live squad-building and optional paid progression layers.",
            session_length="10-20 minute matches that are easy to fit in one sitting.",
            session_bucket="short",
            play_style="head-to-head sports live service",
            hub_group="competitive",
            core_loop="Play football matches, build or tune a squad, and decide how much of the live-service wrapper you actually want to engage with.",
            best_for="football fans who want free match access and are comfortable checking current mode support before investing time",
            not_for="players who want a fully static offline package or zero service-model uncertainty",
            learning_barrier="Basic passing and defending are approachable, but team-building systems and event logic add friction over time.",
            social_shape="Most of the social energy is head-to-head or local rivalry rather than voice-heavy team coordination.",
            progression_notes="Club building and event participation drive the long-term loop more than one clean campaign structure.",
            spending_notes="Core match access is free, but live squad-building and special offers can add collection pressure.",
            first_session_plan=(
                "Play plain matches before you invest energy in team-building systems or event ladders.",
                "Learn two safe passing patterns and one defensive recovery habit before chasing highlight goals.",
                "Check current event rules directly on the official live-service pages before you care about the rewards.",
                "Set a spending boundary before opening any paid card or coin offers.",
            ),
            fit_questions=(
                "Are you here for the on-pitch feel or for long-term collection systems?",
                "Do you want a live football hobby or a simple side game?",
                "Will changing events and offers bother you more than they motivate you?",
            ),
            source_label="Official game overview",
            source_url="https://www.konami.com/efootball/en/page/gameoverview",
            title="eFootball Before You Play: A Fit Guide for Free Football Match Sessions",
            description="This sourced eFootball fit profile helps you weigh football match feel, live squad-building systems, and monetization pressure before you install.",
            summary="eFootball fits players who want football matches first and can tolerate a live-service wrapper around them.",
            onboarding_notes="It is worth separating the on-pitch feel from the surrounding live economy. If the passing rhythm clicks, the game may suit you even if you ignore many events. If the live wrapper feels distracting immediately, that feeling usually stays relevant.",
            commitment_notes="Short matches make eFootball easy to sample, but club optimization and event cadence can quietly turn it into a more demanding routine.",
            what_can_change=(
                "Event structures and squad-building incentives can change frequently.",
                "Licensing or featured content can alter how current the presentation feels.",
                "Monetization offers and progression pacing may shift more often than core match feel.",
            ),
            review_hub_summary="Best for football fans who mainly care about free match access and can keep live economy features in proportion.",
            related_guides=("free-to-play-spending", "controller-settings-guide"),
            visual_points=("10-20 min", "Solo or versus", "Live squad economy"),
        ),
        game(
            slug="trackmania",
            name="Trackmania",
            genre="Time-trial racing",
            official_url="https://www.ubisoft.com/en-us/game/trackmania/trackmania",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-entry racing game with official access tiers that should be checked before you commit long-term.",
            session_length="1-10 minute runs with instant restarts and easy stop points.",
            session_bucket="short",
            play_style="asynchronous precision racing",
            hub_group="competitive",
            core_loop="Run a short track, restart instantly, and shave time off through cleaner lines and better surface control.",
            best_for="players who enjoy shaving seconds off a time and learning one track more efficiently each day",
            not_for="players who need door-to-door racing chaos or heavy progression rewards",
            learning_barrier="Driving is simple to start, but advanced surfaces and speed techniques create a higher ceiling than the first track suggests.",
            social_shape="Most of the competition is asynchronous through ghosts and leaderboards, with optional live rooms layered on top.",
            progression_notes="The durable hook is self-improvement and track mastery more than account power.",
            spending_notes="Access tiers and club features can matter, so the current official offering is worth checking before you assume the long-term value.",
            first_session_plan=(
                "Pick one daily or campaign track and stay with it long enough to learn why restarts feel good here.",
                "Run without ghosts first so your own baseline is readable.",
                "Use instant restarts freely instead of finishing messy runs out of habit.",
                "Judge the fit by whether repetition feels satisfying, not by your leaderboard position on night one.",
            ),
            fit_questions=(
                "Do you enjoy repetition with clear measurable improvement?",
                "Is asynchronous leaderboard pressure enough social energy for you?",
                "Will official access tiers feel fair for the time you plan to spend?",
            ),
            source_label="Official game page",
            source_url="https://www.ubisoft.com/en-us/game/trackmania/trackmania",
            title="Trackmania Before You Play: A Fit Guide for Quick Time-Trial Improvement",
            description="Use this sourced Trackmania fit profile to judge instant restarts, short sessions, asynchronous competition, and access-tier questions before you install.",
            summary="Trackmania fits short-session players who like instant restarts and improvement loops more than car collecting or contact racing.",
            onboarding_notes="If repeating the same corner twenty times sounds satisfying, the fit is strong. If that sounds tedious, the game's brilliance may never surface no matter how slick the interface feels.",
            commitment_notes="Trackmania is one of the easiest precision games to fit around real life because you can stop after one clean run or vanish into iteration for an hour.",
            what_can_change=(
                "Campaign tracks and featured events rotate regularly.",
                "Access tiers or club features may change how much long-term value you see.",
                "Community map visibility can alter how social the experience feels beyond the basics.",
            ),
            review_hub_summary="A great fit for players who want measurable improvement in tiny sessions and do not need direct-contact racing.",
            related_guides=("controller-settings-guide", "cloud-gaming-guide"),
            visual_points=("1-10 min", "Async competition", "Check access tier"),
        ),
        game(
            slug="the-sims-4",
            name="The Sims 4",
            genre="Life simulation",
            official_url="https://www.ea.com/games/the-sims/the-sims-4",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free base game with optional paid expansions, kits, and packs.",
            session_length="30 minutes to several hours depending on how deep you go into one household or build.",
            session_bucket="flex",
            play_style="solo sandbox storytelling",
            hub_group="social",
            core_loop="Create a household, build or manage a space, and let self-directed stories become the reason you keep playing.",
            best_for="creative players who want storytelling, building, and self-directed household routines",
            not_for="players who need clear victory conditions or a complete all-in-one package without expansions",
            learning_barrier="Basic play is approachable, but building tools, aspirations, careers, and pack interactions can still snowball in scope.",
            social_shape="The Sims 4 is primarily solo and self-paced.",
            progression_notes="Household stories, builds, collections, and pack systems create personal goals rather than competitive progression.",
            spending_notes="The base game is free, but expansions and kits can turn the total cost into a long-tail decision.",
            first_session_plan=(
                "Play one small household before building a giant save or buying extra content.",
                "Learn pause, build, and needs-management controls early so the pacing feels calm instead of messy.",
                "Decide whether you care more about storytelling or architecture before browsing packs.",
                "Judge the base game on its own terms before assuming expansion marketing reflects what you need.",
            ),
            fit_questions=(
                "Do you enjoy inventing your own goals instead of following a fixed challenge path?",
                "Will paid packs feel like optional flavor or missing pieces to you?",
                "Are you looking for a solo decompress game rather than a competitive one?",
            ),
            source_label="Official free-to-play overview",
            source_url="https://www.ea.com/games/the-sims/the-sims-4/free-to-play",
            title="The Sims 4 Before You Play: Is It a Fit for Creative Sandbox Storytellers?",
            description="This sourced The Sims 4 fit profile helps you weigh free-base access, expansion cost creep, and self-directed sandbox play before you download.",
            summary="The Sims 4 fits players who want a creative sandbox more than a game that tells them exactly what to do next.",
            onboarding_notes="The first fit check is whether creating routines and stories feels relaxing or directionless. If you like setting your own goals, the base game already reveals a lot about whether the series works for you.",
            commitment_notes="Sessions can stretch unexpectedly because there is rarely a hard stop point, but there is also no multiplayer schedule pressure pulling you back in.",
            what_can_change=(
                "Pack bundles and sales can change the value conversation quickly.",
                "Base-game updates may shift what new players can do without extra spending.",
                "PC mod compatibility or platform parity can change with updates outside the base fit question.",
            ),
            review_hub_summary="Best for creative solo players who want self-directed stories and can keep pack marketing in perspective.",
            related_guides=("free-to-play-spending", "healthy-gaming-setup"),
            visual_points=("30+ min", "Solo sandbox", "Free base + packs"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="hearthstone",
            name="Hearthstone",
            genre="Digital card game",
            official_url="https://hearthstone.blizzard.com/",
            platforms=("PC", "Mobile"),
            platform_tags=("pc", "mobile"),
            business_model="Free-to-play card game with expansion bundles, packs, and seasonal reward tracks.",
            session_length="5-15 minute matches that fit well on PC or mobile.",
            session_bucket="short",
            play_style="turn-based ladder strategy",
            hub_group="strategy",
            core_loop="Build or borrow a deck, navigate short matches, and refine how you trade tempo, value, and risk.",
            best_for="players who want turn-based strategy in short windows on PC or mobile",
            not_for="players who hate meta churn, card acquisition systems, or randomness in outcomes",
            learning_barrier="The interface is welcoming, but collection efficiency and format knowledge matter as soon as you want several decks.",
            social_shape="Hearthstone is mostly a solo queue game; the social layer is more about discussing decks than live teamwork.",
            progression_notes="Daily quests, collection growth, and ranked ladders drive regular engagement.",
            spending_notes="You can play for free, but building many competitive decks quickly usually means money or careful long-term dust management.",
            first_session_plan=(
                "Finish the tutorial path and let the game teach board flow before crafting anything.",
                "Pick one mode and one starter deck instead of sampling every queue in one night.",
                "Avoid crafting niche cards until you know what style of deck you actually enjoy.",
                "Decide whether collection building feels motivating before treating every set release as an obligation.",
            ),
            fit_questions=(
                "Do you want strategy in ten-minute windows more than long live matches?",
                "Are card rotations a plus because they refresh the game, or a hassle because they age your collection?",
                "Can you commit to one or two decks instead of wanting every archetype immediately?",
            ),
            source_label="Official how-to-play guide",
            source_url="https://hearthstone.blizzard.com/en-us/how-to-play",
            title="Hearthstone Before You Play: A Fit Guide for Short Strategic Mobile Sessions",
            description="Use this sourced Hearthstone fit profile to judge match length, collection pressure, mobile convenience, and pack-driven monetization before you install.",
            summary="Hearthstone fits players who want short strategic sessions and do not mind card-set rotation.",
            onboarding_notes="The key fit question is whether you enjoy deck identity and matchup knowledge enough to revisit the game after each expansion. If yes, the short match length becomes a strength. If no, the collection treadmill can feel louder than the strategy.",
            commitment_notes="It is easy to sample in tiny sessions, but maintaining a broad card pool is the real long-term friction.",
            what_can_change=(
                "Standard format rotations can redefine what a beginner-friendly deck looks like.",
                "Balance patches and mini-sets move the meta more often than the interface suggests.",
                "Bundle pricing and reward-track structures change independently of the core card-game fit.",
            ),
            review_hub_summary="A strong fit for short strategic play, especially if you can stay focused on a small collection at first.",
            related_guides=("free-to-play-spending", "cloud-gaming-guide"),
            visual_points=("5-15 min", "Mostly solo", "Packs + passes"),
        ),
        game(
            slug="teamfight-tactics",
            name="Teamfight Tactics",
            genre="Auto battler",
            official_url="https://teamfighttactics.leagueoflegends.com/",
            platforms=("PC", "Mobile"),
            platform_tags=("pc", "mobile"),
            business_model="Free-to-play strategy game with cosmetic monetization and seasonal passes.",
            session_length="30-40 minute matches that reward planning and adaptation more than speed.",
            session_bucket="medium",
            play_style="economy-and-positioning strategy",
            hub_group="strategy",
            core_loop="Manage economy, scout the lobby, and adapt your board as item drops and contested units change the plan.",
            best_for="strategy players who want planning, economy decisions, and flexible adaptation instead of twitch aim",
            not_for="players who need short matches or dislike relearning sets",
            learning_barrier="TFT is approachable once the shop makes sense, but each new set brings a fresh web of traits, units, and item priorities.",
            social_shape="The game works solo or socially, yet live voice coordination matters less than in shooters or MOBAs.",
            progression_notes="The long-term hook is learning each set's trait web and transition patterns rather than building account power.",
            spending_notes="Core play is free. Spending is mainly cosmetic and pass-based.",
            first_session_plan=(
                "Learn interest breakpoints and leveling basics before chasing advanced compositions.",
                "Force one simple comp for a few games so the economy rhythm becomes familiar.",
                "Scout the lobby every player-damage phase even if you only understand half of what you see.",
                "Judge the game after one full match where adaptation mattered, not after a lucky opening shop.",
            ),
            fit_questions=(
                "Do you like adaptation more than real-time execution?",
                "Can you spend 30-plus minutes on one strategic match without feeling trapped?",
                "Will set resets feel fresh or annoying to you as the game evolves?",
            ),
            source_label="Official how-to-play guide",
            source_url="https://teamfighttactics.leagueoflegends.com/en-us/how-to-play/",
            title="Teamfight Tactics Before You Play: A Fit Guide for Planning-Heavy Auto Battler Fans",
            description="Read this sourced Teamfight Tactics fit profile before you commit to its long matches, set relearning, and cosmetic-first monetization.",
            summary="Teamfight Tactics fits players who like thinking ahead, scouting opponents, and iterating on a meta over weeks.",
            onboarding_notes="The game becomes much easier to like once you stop trying to memorize everything on day one and instead learn one flexible opening and one late-game plan. If that kind of strategic patience sounds good, TFT is rewarding.",
            commitment_notes="One match is a real block of time, and each new set asks returning players to refresh their knowledge before they feel sharp again.",
            what_can_change=(
                "Set themes and unit pools redefine the entire strategic vocabulary several times a year.",
                "Balance patches can quickly change which comps are easiest for beginners to trust.",
                "Pass rewards and cosmetic systems change more often than the base adaptation loop.",
            ),
            review_hub_summary="Best for players who want long strategic matches and do not mind relearning the game each set.",
            related_guides=("multiplayer-beginner-checklist", "free-to-play-spending"),
            visual_points=("30-40 min", "Low-comm strategy", "Cosmetics + pass"),
        ),
        game(
            slug="brawlhalla",
            name="Brawlhalla",
            genre="Platform fighter",
            official_url="https://www.brawlhalla.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch", "Mobile"),
            platform_tags=("pc", "playstation", "xbox", "switch", "mobile"),
            business_model="Free-to-play platform fighter with character unlocks and cosmetic crossovers.",
            session_length="3-10 minute matches that work online, locally, or in quick bursts.",
            session_bucket="short",
            play_style="cross-platform fighting game",
            hub_group="competitive",
            core_loop="Learn a legend's weapons, recover to the stage cleanly, and win short exchanges through movement and reads.",
            best_for="players who want a free cross-platform fighter that supports short casual or local sessions",
            not_for="players who need a small fixed roster or deep single-player content",
            learning_barrier="Brawlhalla is easy to pick up, but movement, dodging, and edge guarding become demanding once ranked interests you.",
            social_shape="It works solo, couch-side, or online with friends, and communication is optional outside serious team play.",
            progression_notes="Legend familiarity and movement skill matter more than account progression.",
            spending_notes="Entry is free, with optional unlocks, cosmetics, and crossover skins.",
            first_session_plan=(
                "Pick one weapon pair you like instead of constantly chasing the whole roster.",
                "Play free-for-all or casual modes before ranked formats start shaping your mood.",
                "Practice recovering back to the stage until losing stocks feels understandable.",
                "Judge the fit by whether short rematches feel inviting, not by immediate ranked success.",
            ),
            fit_questions=(
                "Do you want fighting-game energy without a huge barrier to first play?",
                "Is cross-play more important to you than roster prestige or brand legacy?",
                "Are very short rounds a plus because they lower the commitment to play again?",
            ),
            source_label="Official legends overview",
            source_url="https://www.brawlhalla.com/legends/",
            title="Brawlhalla Before You Play: Is It a Fit for Cross-Platform Fighting Nights?",
            description="Use this sourced Brawlhalla fit profile to judge cross-play, short rounds, unlock pressure, and casual-versus-ranked appeal before you install.",
            summary="Brawlhalla fits players who want a low-friction fighting game that travels well across devices and group setups.",
            onboarding_notes="The cleanest first test is local or casual online play. If the knockback, dodges, and weapon cycling click immediately, the game does not need much explanation. If they do not, the short rounds can still keep experimentation painless.",
            commitment_notes="Very short matches make Brawlhalla easy to keep around as a side game even if you never climb seriously.",
            what_can_change=(
                "The free legend rotation alters what a no-spend player can test immediately.",
                "Crossover events and seasonal cosmetics can change the surrounding appeal without changing the fundamentals.",
                "Balance patches can make certain weapons friendlier or rougher for beginners.",
            ),
            review_hub_summary="A clean fit when you want a free fighter that works across platforms and does not demand long sessions.",
            related_guides=("controller-settings-guide", "crossplay-guide"),
            visual_points=("3-10 min", "Local or online", "Unlocks + skins"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="the-finals",
            name="THE FINALS",
            genre="Team objective shooter",
            official_url="https://www.reachthefinals.com/",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-to-play objective shooter with cosmetic bundles and seasonal passes.",
            session_length="10-20 minute matches that still benefit from a regular squad.",
            session_bucket="short",
            play_style="destruction-driven squad shooter",
            hub_group="competitive",
            core_loop="Chase cashout objectives while using gadgets, movement, and destruction to create better fights than the other team expects.",
            best_for="squads who want destructible arenas, objective chaos, and creative gadget planning",
            not_for="players who need very clean visual information or low-chaos fights",
            learning_barrier="The rules are easy to describe, but destruction, class roles, and cashout timing create many moving parts quickly.",
            social_shape="Playable solo, but much better with a duo or trio who can coordinate pushes, revives, and retreats.",
            progression_notes="Unlocks and ranked goals help, yet the durable appeal is learning how destruction changes each objective.",
            spending_notes="Core access is free. Monetization is mostly cosmetic and seasonal.",
            first_session_plan=(
                "Start on a medium or balanced build unless you already know you want a specialist role.",
                "Follow the cashout objective instead of treating the game like team deathmatch.",
                "Pay attention to how floor and roof destruction changes safe routes.",
                "Judge the fit after a few matches where revives and resets actually matter, not after one highlight reel round.",
            ),
            fit_questions=(
                "Do you like improvisation more than tight competitive control?",
                "Will visual chaos feel fun or tiring after several sessions?",
                "Are you willing to queue with at least one reliable partner if solo matchmaking feels noisy?",
            ),
            source_label="Official patch notes",
            source_url="https://www.reachthefinals.com/patch-notes",
            title="THE FINALS Before You Play: A Fit Guide for Destruction-Driven Squads",
            description="Read this sourced THE FINALS fit profile before you commit to its destructible arenas, squad reliance, and seasonal cosmetic economy.",
            summary="THE FINALS fits players who want an objective shooter that feels improvisational instead of fixed.",
            onboarding_notes="If map destruction sounds exciting rather than messy, the game has a clear niche. If you prefer predictable sightlines and tidy readouts, the same chaos can be its biggest weakness.",
            commitment_notes="Individual matches are short, but understanding cashout pacing and class roles takes more deliberate reps than the bright presentation suggests.",
            what_can_change=(
                "Class balance and gadget strength can swing with seasonal patches.",
                "Event modes and ranked structures may change what the beginner path looks like.",
                "Cosmetic pass cadence is separate from whether the core objective loop suits you.",
            ),
            review_hub_summary="Great for squads who like creative objective play and destruction; weaker if you want quiet visual clarity.",
            related_guides=("clear-team-communication", "optimize-fps-settings"),
            visual_points=("10-20 min", "Best in squad", "Cosmetics + pass"),
        ),
        game(
            slug="marvel-rivals",
            name="Marvel Rivals",
            genre="Third-person hero shooter",
            official_url="https://www.marvelrivals.com/",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-to-play hero shooter with cosmetic monetization and seasonal progression.",
            session_length="10-20 minute matches with fast hero experimentation up front.",
            session_bucket="short",
            play_style="hero fantasy team combat",
            hub_group="competitive",
            core_loop="Choose a hero fantasy you enjoy, layer team-up synergies on top, and use objective pressure instead of only duel skill.",
            best_for="players who want accessible hero-shooter action and already enjoy Marvel character fantasy",
            not_for="players who dislike crowded visuals or want a minimal-ability shooter",
            learning_barrier="The hero fantasy is easy to understand, but large rosters and overlapping effects raise the knowledge load over time.",
            social_shape="Easy to sample solo, yet team-up interactions and focus fire feel much better with friends or steady pings.",
            progression_notes="Hero familiarity and matchup knowledge matter more than account power.",
            spending_notes="Core play is free. Spending is centered on cosmetics and seasonal extras.",
            first_session_plan=(
                "Try three heroes from different roles before deciding what the roster feels like.",
                "Use one easy combo repeatedly so your first wins come from execution, not chaos.",
                "Follow the objective UI instead of letting the hero fantasy pull you into every duel.",
                "Turn on accessibility and subtitle options before ranked-style play starts to matter.",
            ),
            fit_questions=(
                "Do you want broad hero fantasy more than realistic shooting discipline?",
                "Will a large roster energize you or overwhelm you?",
                "Are you mostly looking for casual team action rather than a tight tactical ladder?",
            ),
            source_label="Official news hub",
            source_url="https://www.marvelrivals.com/news/",
            title="Marvel Rivals Before You Play: A Fit Guide for Accessible Hero-Shooter Groups",
            description="Use this sourced Marvel Rivals fit profile to weigh roster size, team-up synergy, quick sessions, and cosmetic monetization before you jump in.",
            summary="Marvel Rivals fits players who want a broad hero roster and readable power fantasy more than tight tactical austerity.",
            onboarding_notes="The early hook is character experimentation. If swapping between recognizable heroes feels exciting, the fit is straightforward. If you want minimal overlap and cleaner visuals, the game can feel crowded fast.",
            commitment_notes="Quick sessions work well, though the roster is large enough that serious improvement still means narrowing to a few mains.",
            what_can_change=(
                "Hero balance and team-up interactions can move rapidly in a live roster game.",
                "New hero releases may reshape what counts as beginner-friendly.",
                "Seasonal cosmetic plans will change more often than the core question of whether the hero sandbox suits you.",
            ),
            review_hub_summary="A good fit when you want accessible hero fantasy and quick group matches, not clean minimalist gunplay.",
            related_guides=("multiplayer-beginner-checklist", "controller-settings-guide"),
            visual_points=("10-20 min", "Team-up focus", "Cosmetic pass"),
        ),
        game(
            slug="pubg-battlegrounds",
            name="PUBG: Battlegrounds",
            genre="Battle royale shooter",
            official_url="https://pubg.com/en",
            platforms=("PC", "PlayStation", "Xbox", "Mobile variants"),
            platform_tags=("pc", "playstation", "xbox", "mobile"),
            business_model="Free-to-play battle royale with cosmetic and pass-based monetization.",
            session_length="20-35 minute matches where surviving deeper can consume a full play block.",
            session_bucket="medium",
            play_style="slow-burn survival shooter",
            hub_group="competitive",
            core_loop="Loot efficiently, position for circles, and win a few high-pressure firefights rather than constant skirmishes.",
            best_for="players who want slower battle royale tension, longer sightlines, and punishing positioning",
            not_for="players who need constant fights or forgiving recoil",
            learning_barrier="PUBG is readable, but the gun handling and pace are harsher than more arcade-style battle royales.",
            social_shape="Solo, duo, and squad play all work; teamwork matters more than flashy mechanics.",
            progression_notes="Account progression exists, but the durable loop is map knowledge, circle decisions, and recoil control.",
            spending_notes="Entry is free. Spending is mostly cosmetic and battle-pass driven.",
            first_session_plan=(
                "Pick one smaller drop route with vehicles nearby so the early game stops feeling random.",
                "Loot only the basics first and learn to move when the circle asks you to move.",
                "Practice recoil in training mode instead of letting your first firefights teach it from scratch.",
                "Judge the pace after a full match where survival decisions matter, not after one hot drop wipe.",
            ),
            fit_questions=(
                "Do you enjoy survival pacing enough to accept quiet minutes between fights?",
                "Are realistic-feeling guns more appealing to you than ability kits?",
                "Can you enjoy a tense long match even if you fire only a few decisive bursts?",
            ),
            source_label="PUBG support hub",
            source_url="https://support.pubg.com/",
            title="PUBG: Battlegrounds Before You Play: Is It a Fit for Slower Battle Royale Tension?",
            description="This sourced PUBG: Battlegrounds fit profile helps you judge survival pacing, recoil harshness, and pass-based monetization before you commit.",
            summary="PUBG fits players who want survival tension and deliberate gunfights more than constant ability-driven action.",
            onboarding_notes="The game is easiest to judge once you accept that downtime is part of the design. If traveling, scouting, and one hard fight sound good, it still owns that niche clearly.",
            commitment_notes="A single match can consume a real block of time, especially if you survive deep into the round.",
            what_can_change=(
                "Map rotation and event playlists can alter how quickly matches get to the tension you want.",
                "Balance tuning may change recoil or loot assumptions for newcomers.",
                "Pass cadence and crossover cosmetics do not change the core slower battle-royale fit.",
            ),
            review_hub_summary="Best for players who want survival tension and realistic gun rhythm, not nonstop action.",
            related_guides=("optimize-fps-settings", "clear-team-communication"),
            visual_points=("20-35 min", "Solo or squad", "Cosmetics + pass"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="roblox",
            name="Roblox",
            genre="User-created game platform",
            official_url="https://www.roblox.com/",
            platforms=("PC", "PlayStation", "Xbox", "Mobile", "VR"),
            platform_tags=("pc", "playstation", "xbox", "mobile", "vr"),
            business_model="Free platform access with Robux purchases and experience-specific monetization.",
            session_length="5-60 minutes depending on the specific experience and group plan.",
            session_bucket="flex",
            play_style="social variety platform",
            hub_group="social",
            core_loop="Browse or revisit user-created experiences, play a few short sessions, and decide which spaces deserve repeat visits.",
            best_for="families, friend groups, or variety seekers who want many low-friction experiences on familiar devices",
            not_for="players who want one curated game, strong discovery filtering, or zero interest in user-generated spaces",
            learning_barrier="The controls can be easy, but account safety, social settings, and smart experience selection matter more than with a single curated game.",
            social_shape="Roblox is highly social by default, which makes privacy and communication settings part of the fit rather than a side issue.",
            progression_notes="Progress depends on the specific experience you choose rather than one unified Roblox-wide progression loop.",
            spending_notes="Entry is free, but Robux spending and experience-specific monetization vary widely enough that boundaries matter early.",
            first_session_plan=(
                "Configure privacy, chat, and purchase settings before you browse widely.",
                "Save two or three trusted experiences instead of drifting through the whole discovery feed.",
                "Play with known friends or a family member first so the social tools are easier to read.",
                "Treat every in-experience store as optional until you understand what it actually changes.",
            ),
            fit_questions=(
                "Do you want variety more than consistency?",
                "Are you comfortable curating what gets played instead of trusting discovery systems completely?",
                "Do in-experience purchases need hard boundaries in your household?",
            ),
            source_label="Roblox help center",
            source_url="https://en.help.roblox.com/hc/en-us",
            title="Roblox Before You Play: A Fit Guide for Families and Group Variety",
            description="This sourced Roblox fit profile helps you judge variety, social exposure, household controls, and Robux monetization before you jump in.",
            summary="Roblox fits players who value range and easy group access more than curation and consistent design standards.",
            onboarding_notes="The core question is not whether Roblox is a good single game. It is whether you want a platform full of uneven but accessible experiments. That makes safety setup and curation part of the decision, not a footnote.",
            commitment_notes="You can dip in for minutes at a time, but account controls and spending boundaries should be handled before browsing freely.",
            what_can_change=(
                "Popular experiences and discovery surfaces shift constantly.",
                "Platform-level safety tools and communication defaults can change by device.",
                "Individual experiences can alter their own monetization and moderation rules at any time.",
            ),
            review_hub_summary="Best when easy social variety matters more than curation, consistency, or a single polished game loop.",
            related_guides=("family-gaming-safety", "free-to-play-spending"),
            visual_points=("5-60 min", "Very social", "Robux varies"),
        ),
        game(
            slug="fall-guys",
            name="Fall Guys",
            genre="Party platformer",
            official_url="https://www.fallguys.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch"),
            platform_tags=("pc", "playstation", "xbox", "switch"),
            business_model="Free-to-play party game with cosmetic and event-driven monetization.",
            session_length="10-20 minute show runs that work well for mixed-skill groups.",
            session_bucket="short",
            play_style="light party competition",
            hub_group="social",
            core_loop="Run short obstacle rounds, survive a few playful elimination games, and accept a little chaos as part of the joke.",
            best_for="players who want low-pressure party sessions and easy laugh-at-the-chaos rounds",
            not_for="players who hate random collisions or want serious competitive control over every outcome",
            learning_barrier="Fall Guys is immediately understandable, and the main question is tolerance for slapstick unpredictability rather than complexity.",
            social_shape="It is great with friends, but still easy to parse solo because the rounds are short and the stakes stay light.",
            progression_notes="Cosmetics and event rewards add direction, but most of the value comes from the social moment-to-moment loop.",
            spending_notes="The game is free to enter. Spending is mostly cosmetic and event-driven.",
            first_session_plan=(
                "Link the platform accounts you need before a group night instead of during it.",
                "Play one solo show first so camera feel and jump timing are not new when friends arrive.",
                "Use early rounds to learn how dive and grab actually feel rather than only racing for qualification.",
                "Judge the game by the mood it creates, not by how many crowns you win right away.",
            ),
            fit_questions=(
                "Are you looking for a party game more than a ladder-focused competitive game?",
                "Will light randomness feel funny or frustrating after several rounds?",
                "Do you need something nonthreatening for mixed-skill friends or family?",
            ),
            source_label="Official news hub",
            source_url="https://www.fallguys.com/en-US/news",
            title="Fall Guys Before You Play: A Fit Guide for Casual Party Sessions",
            description="Use this sourced Fall Guys fit profile to weigh short party rounds, mixed-skill group appeal, and event-driven cosmetics before you install.",
            summary="Fall Guys fits casual groups who want short multiplayer rounds without heavy study or serious pressure.",
            onboarding_notes="It is one of the fastest fit checks on the site: if slapstick physics and elimination-show pacing sound fun, you will know quickly. If you need competitive precision every second, it may never fully click.",
            commitment_notes="The game respects short sessions, and long-term stickiness depends more on your friend group than on deep progression.",
            what_can_change=(
                "Limited-time events and playlists rotate regularly.",
                "Licensed cosmetics and crossover seasons can change the game's surrounding appeal.",
                "Platform or account-linking steps can change after backend updates.",
            ),
            review_hub_summary="A clean fit for low-pressure party nights and short casual rounds, especially with mixed-skill groups.",
            related_guides=("crossplay-guide", "family-gaming-safety"),
            visual_points=("10-20 min", "Party-friendly", "Cosmetics + events"),
        ),
        game(
            slug="halo-infinite",
            name="Halo Infinite Multiplayer",
            genre="Arena shooter",
            official_url="https://www.halowaypoint.com/games/halo-infinite",
            platforms=("PC", "Xbox"),
            platform_tags=("pc", "xbox"),
            business_model="Free-to-play arena shooter with cosmetic monetization.",
            session_length="10-20 minute matches that are easy to fit around other games.",
            session_bucket="short",
            play_style="arena objective shooter",
            hub_group="competitive",
            core_loop="Use equal starts, map pickups, and clean positioning to win fights and objective trades.",
            best_for="players who want classic arena pacing, strong controller feel, and readable map control",
            not_for="players who want heavy hero abilities or a giant reward treadmill",
            learning_barrier="The combat is approachable, but weapon spawns, sightlines, and movement discipline still matter once the novelty wears off.",
            social_shape="Halo Infinite works solo or with friends; objective modes simply get better when even light communication exists.",
            progression_notes="Battle passes and ranks exist, but the deeper hook is learning maps, starts, and pickup timing.",
            spending_notes="Core multiplayer access is free. Spending is mostly cosmetic.",
            first_session_plan=(
                "Play Slayer or Quick Play before ranked so the arena rhythm is clear.",
                "Learn two weapons you like and where they tend to appear on a favorite map.",
                "Treat equipment as a survival or repositioning tool before trying fancy outplays.",
                "Notice whether equal starts feel freeing to you or strangely restrictive.",
            ),
            fit_questions=(
                "Do equal starts and map pickups sound appealing instead of outdated?",
                "Are you willing to learn maps instead of relying on hero kits?",
                "Do you want arena pacing more than battle-royale sprawl?",
            ),
            source_label="Halo support hub",
            source_url="https://support.halowaypoint.com/hc/en-us",
            title="Halo Infinite Multiplayer Before You Play: Is It a Fit for Arena Shooter Fans?",
            description="This sourced Halo Infinite Multiplayer fit profile helps you judge arena pacing, equal starts, map knowledge, and cosmetic-only monetization before you queue.",
            summary="Halo Infinite Multiplayer fits players who want arena-shooter fundamentals without the density of older hardcore PC-only titles.",
            onboarding_notes="The key fit question is whether you enjoy equal starts and map pickups more than loadout building. If you do, Halo remains extremely readable. If not, it can feel old-fashioned rather than elegant.",
            commitment_notes="Matches are manageable enough that Halo works well as a secondary competitive title, not only as a main hobby.",
            what_can_change=(
                "Playlist rotation and event structure can change what beginners see first.",
                "Sandbox tuning alters which weapons feel easiest to learn.",
                "Cosmetic events and passes change more often than the core arena fit.",
            ),
            review_hub_summary="A strong fit when you want equal-start arena combat and matches that do not monopolize the night.",
            related_guides=("controller-settings-guide", "multiplayer-beginner-checklist"),
            visual_points=("10-20 min", "Solo or fireteam", "Cosmetics only"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="overwatch-2",
            name="Overwatch 2",
            genre="Hero shooter",
            official_url="https://overwatch.blizzard.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch"),
            platform_tags=("pc", "playstation", "xbox", "switch"),
            business_model="Free-to-play hero shooter with battle passes and cosmetic monetization.",
            session_length="10-20 minute matches that are easy to sample casually.",
            session_bucket="short",
            play_style="objective-based hero combat",
            hub_group="competitive",
            core_loop="Take or defend objectives, swap heroes when a matchup asks for it, and coordinate ultimates well enough to win team fights.",
            best_for="players who like fast objective fights, hero swapping, and readable team roles",
            not_for="players who want one loadout to master without mid-match adaptation",
            learning_barrier="The basics are accessible, but hero counters, ult economy, and role pressure matter more as soon as you care about consistency.",
            social_shape="Overwatch 2 is easy to queue casually, though the match quality improves when teammates ping or talk around plans instead of reacting alone.",
            progression_notes="The real improvement loop is understanding matchups and timing rather than grinding account power.",
            spending_notes="Access is free. Battle passes and cosmetic shop items are the core monetization pressure.",
            first_session_plan=(
                "Play Quick Play before you let ranked expectations distort the first impression.",
                "Choose one comfortable tank, support, and damage hero instead of trying the whole roster at once.",
                "Learn the objective UI and when your team actually has numbers before spending ultimates.",
                "Try hero swapping only after you know what problem the swap is supposed to solve.",
            ),
            fit_questions=(
                "Do you like changing plans mid-match instead of one static build?",
                "Will role queue make the game more readable or more restrictive for you?",
                "Do you prefer team-fight rhythm over one-life round tension?",
            ),
            source_label="Official heroes overview",
            source_url="https://overwatch.blizzard.com/en-us/heroes/",
            title="Overwatch 2 Before You Play: A Fit Guide for Hero-Swap Team Players",
            description="Use this sourced Overwatch 2 fit profile to judge quick session length, role readability, hero swapping, and battle-pass pressure before you queue.",
            summary="Overwatch 2 fits players who want colorful team fights and a lower mechanical barrier than tactical shooters.",
            onboarding_notes="The fit comes down to whether you enjoy adapting on the fly. If hero swapping sounds interesting rather than annoying, the game opens up quickly. If you want one unchanging role script, it can feel slippery.",
            commitment_notes="Quick Play is easy to sample, but meaningful role confidence still asks for repeated map and matchup learning.",
            what_can_change=(
                "Hero balance and role expectations can move aggressively between seasons.",
                "New heroes or modes can reshape the beginner path.",
                "Battle-pass structures and seasonal cosmetics are separate from the core objective loop.",
            ),
            review_hub_summary="A good fit when you want fast, readable team fights and do not mind changing heroes to solve problems.",
            related_guides=("multiplayer-beginner-checklist", "clear-team-communication"),
            visual_points=("10-20 min", "Easy casual queue", "Battle pass"),
        ),
        game(
            slug="destiny-2",
            name="Destiny 2",
            genre="Online action shooter",
            official_url="https://www.bungie.net/7/en/Destiny",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-entry online shooter with paid expansions, dungeons, and seasonal content layers.",
            session_length="20-120 minutes depending on whether you are doing quick activities or organized endgame.",
            session_bucket="flex",
            play_style="loot shooter with co-op endgame",
            hub_group="progression",
            core_loop="Shoot through activities that feel excellent moment to moment, then use loot and build options to open harder co-op goals.",
            best_for="players who want polished shooting plus long-form co-op goals like dungeons and raids",
            not_for="players who want simple storefront clarity or a fully self-contained free campaign",
            learning_barrier="Destiny 2 is easy to enjoy at the trigger-pull level, but ownership structure and endgame systems can confuse new players.",
            social_shape="Patrols and some playlists work solo, yet the most memorable content is built around a regular group.",
            progression_notes="Power, exotics, subclasses, and rotating activities create a strong weekly rhythm once you understand what you actually own.",
            spending_notes="The free entry layer is real, but major campaigns, dungeon keys, and seasons often sit behind paid additions.",
            first_session_plan=(
                "Play the introductory path and confirm what campaigns or expansions your account really includes.",
                "Keep one favorite weapon type equipped long enough to learn how the sandbox feels.",
                "Treat the early menus as a map of content ownership, not a sign that you must buy everything at once.",
                "Decide whether group endgame sounds exciting before spending on deeper add-ons.",
            ),
            fit_questions=(
                "Do you want raids and dungeons, or do you mainly want satisfying shooting for a few hours?",
                "Will changing seasonal packaging confuse you or feel manageable once you know the structure?",
                "Are you willing to buy expansions only after the free layer proves itself?",
            ),
            source_label="Official New Light overview",
            source_url="https://www.bungie.net/7/en/Destiny/NewLight",
            title="Destiny 2 Before You Play: Is It a Fit for Co-op Groups Wanting Endgame Raids?",
            description="Read this sourced Destiny 2 fit profile before you commit to its excellent gunplay, group endgame, and paid expansion structure.",
            summary="Destiny 2 fits players who want great-feeling shooting and group endgame more than clean product packaging.",
            onboarding_notes="The biggest fit question is whether you enjoy chasing gear across a changing seasonal structure. If you do, the shooting and raids can carry a lot of complexity. If not, the storefront and content layers can feel messy quickly.",
            commitment_notes="You can enjoy strikes or short story sessions casually, but meaningful long-term participation often means scheduling around resets or friends' availability.",
            what_can_change=(
                "Active expansions, seasons, and bundles change over time.",
                "Activity rotation and power targets can move what counts as the best beginner path.",
                "Cross-save or account-link expectations should always be rechecked on Bungie's live pages.",
            ),
            review_hub_summary="A good fit for groups that want premium-feeling shooting and are comfortable with add-on-driven live-service packaging.",
            related_guides=("free-to-play-spending", "crossplay-guide"),
            visual_points=("20-120 min", "Best with group", "Free entry + add-ons"),
        ),
        game(
            slug="path-of-exile",
            name="Path of Exile",
            genre="Action RPG",
            official_url="https://www.pathofexile.com/",
            platforms=("PC", "PlayStation", "Xbox"),
            platform_tags=("pc", "playstation", "xbox"),
            business_model="Free-to-play action RPG with cosmetic monetization and practical stash-tab convenience purchases.",
            session_length="20 minutes to several hours, depending on where you are in a league or build plan.",
            session_bucket="flex",
            play_style="build-first loot RPG",
            hub_group="progression",
            core_loop="Follow a build through the campaign, then chase stronger gear, maps, and seasonal systems with ever more specific goals.",
            best_for="players who enjoy theorycrafting, loot filters, and learning a build over a season",
            not_for="players who want a gentle first campaign or a self-explanatory passive tree",
            learning_barrier="Path of Exile is famous for its build freedom, and that same freedom makes the first serious character much harder without guidance.",
            social_shape="The game works fine solo, while trading and community guides become useful if you care about efficiency.",
            progression_notes="The campaign is only the first layer; mapping, league systems, and build optimization are the real long-term loop.",
            spending_notes="Power is not directly sold, but stash tabs become a practical quality-of-life purchase for many committed players.",
            first_session_plan=(
                "Choose one beginner build you are willing to follow instead of improvising everything blind.",
                "Finish the campaign before worrying about perfect loot or advanced crafting systems.",
                "Learn one currency item at a time rather than treating the whole economy as day-one homework.",
                "Decide whether the game's planning-heavy style is enjoyable before buying stash upgrades.",
            ),
            fit_questions=(
                "Do you enjoy reading build guides instead of discovering every system alone?",
                "Can you live with a rough first character if the long-term depth is excellent?",
                "Do you want power depth more than elegant menus and onboarding?",
            ),
            source_label="Official game overview",
            source_url="https://www.pathofexile.com/game",
            title="Path of Exile Before You Play: A Fit Guide for Build-First ARPG Players",
            description="Use this sourced Path of Exile fit profile to judge build complexity, league structure, stash-tab pressure, and solo-friendly progression before you start.",
            summary="Path of Exile fits players who like build research and long seasonal optimization more than smooth onboarding.",
            onboarding_notes="The cleanest first test is whether following a beginner build sounds helpful or restrictive. Players who accept outside guidance usually settle in faster; players who insist on complete self-discovery often hit a wall sooner.",
            commitment_notes="A first season can consume a lot of reading time, even if your actual play sessions are short and modular.",
            what_can_change=(
                "League mechanics and economies reset regularly.",
                "Build recommendations shift hard when balance patches hit the passive tree or core skills.",
                "Stash sales and cosmetic promotions change independently of gameplay fit.",
            ),
            review_hub_summary="Best for theorycrafters who want depth first and are happy to treat outside guides as part of the game.",
            related_guides=("free-to-play-spending", "multiplayer-beginner-checklist"),
            visual_points=("20+ min", "Solo friendly", "QoL stash tabs"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="rocket-league",
            name="Rocket League",
            genre="Sports action",
            official_url="https://www.rocketleague.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch"),
            platform_tags=("pc", "playstation", "xbox", "switch"),
            business_model="Free-to-play competitive sports game with cosmetic bundles and season passes.",
            session_length="5-10 minute matches that are easy to stack into a short session.",
            session_bucket="short",
            play_style="physics-based competitive sports",
            hub_group="competitive",
            core_loop="Control the car cleanly enough to challenge the ball, rotate intelligently, and slowly add more mechanical range.",
            best_for="players who want five-minute matches and almost endless room to refine mechanics",
            not_for="players who need RPG progression, heavy onboarding, or forgiving ranked ladders",
            learning_barrier="The objective is obvious immediately, yet advanced movement and recovery take real practice.",
            social_shape="Rocket League works solo, in duos, or in full teams; voice helps, but even casual pings or chat can be enough.",
            progression_notes="Progression is mostly skill, rank, and cosmetics rather than account power.",
            spending_notes="Gameplay is free. Monetization is centered on the pass and optional cosmetic bundles.",
            first_session_plan=(
                "Stay in casual 2v2 or 3v3 before trying to judge ranked stress.",
                "Learn boost management and camera toggle before worrying about aerial highlights.",
                "Use free play for a few calm minutes between matches instead of one long grind block.",
                "Judge your enjoyment by whether basic movement practice feels satisfying, not by your first win rate.",
            ),
            fit_questions=(
                "Do you enjoy repeating the same simple ruleset until your control becomes expressive?",
                "Can you handle being bad at a game that looks easy to understand?",
                "Do you value short matches more than heavy progression systems?",
            ),
            source_label="Official game information hub",
            source_url="https://www.rocketleague.com/en",
            title="Rocket League Before You Play: A Fit Guide for Quick Competitive Sessions",
            description="Use this sourced Rocket League fit profile to weigh its short matches, high mechanical ceiling, and cosmetic-only monetization before you install.",
            summary="Rocket League fits short-session competitors who enjoy practicing the same simple ruleset until movement becomes expression.",
            onboarding_notes="Because the objective is instantly readable, the real fit question is whether you enjoy failing at a skill for a while before it feels elegant. Players who love self-improvement usually stick. Players who need constant new systems often bounce.",
            commitment_notes="Rocket League respects tight schedules, but the skill ceiling is high enough that it can quietly become your main competitive hobby.",
            what_can_change=(
                "Season challenges and pass structures rotate regularly.",
                "Limited modes and licensed cosmetic bundles can change the surrounding appeal.",
                "Competitive playlist rules or ranking presentation can shift over time.",
            ),
            review_hub_summary="Excellent when you want a deep competitive game that still fits into ten-minute windows.",
            related_guides=("controller-settings-guide", "crossplay-guide"),
            visual_points=("5-10 min", "Solo or duos", "Cosmetics only"),
        ),
        game(
            slug="league-of-legends",
            name="League of Legends",
            genre="MOBA",
            official_url="https://www.leagueoflegends.com/",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free-to-play competitive MOBA with cosmetic monetization and time-based champion unlocking.",
            session_length="25-45 minute matches, with extra time required for learning outside the match itself.",
            session_bucket="long",
            play_style="team strategy arena",
            hub_group="strategy",
            core_loop="Manage your lane, contest objectives, and build team-fight advantage through champion knowledge and map timing.",
            best_for="competitive players who enjoy team strategy, lane responsibilities, and learning a big champion roster over months",
            not_for="players who want short matches, a low knowledge load, or a calm solo experience",
            learning_barrier="League's core objective is readable, but the game becomes demanding once matchups, role expectations, and objective timings start compounding.",
            social_shape="Solo queue works, yet the experience is emotionally easier when you have friends to queue with or strong mute discipline.",
            progression_notes="Account levels and champion ownership matter early, but long-term retention comes from knowledge depth and ranked improvement.",
            spending_notes="Core competition is free. Cosmetics dominate monetization, while expanding a big champion pool takes time rather than direct power purchases.",
            first_session_plan=(
                "Pick one lane and two beginner-friendly champions instead of touching every role.",
                "Treat minion timing and recall rhythm as the first lessons, not kill chasing.",
                "Use pings heavily and mute chat early if the social tone starts distracting you.",
                "End the night by naming one map objective you still do not understand and look up only that.",
            ),
            fit_questions=(
                "Do you like studying outside the match as much as competing inside it?",
                "Are you comfortable with 30-minute losses that still teach something useful?",
                "Will team friction ruin the fun faster than the strategy can repay it?",
            ),
            source_label="Official how-to-play guide",
            source_url="https://www.leagueoflegends.com/en-us/how-to-play/",
            title="League of Legends Before You Play: A Fit Guide for Long-Term Competitive Teammates",
            description="This sourced League of Legends fit profile helps you judge match length, team friction, champion learning, and cosmetic-led monetization before you commit.",
            summary="League of Legends fits players who want a long-term competitive game and are willing to study rather than dabble.",
            onboarding_notes="The first hours feel chaotic because the game assumes vocabulary you do not yet have. The fit becomes clearer once you narrow yourself to one role and a tiny champion pool.",
            commitment_notes="For many players, League becomes a hobby game rather than a casual detour, because even moderate competence depends on repeated map, role, and matchup study.",
            what_can_change=(
                "Patch balance and item systems can alter role priorities quickly.",
                "New champions and seasonal structure changes affect the learning load.",
                "Onboarding tools and queue formats can improve or complicate the beginner path.",
            ),
            review_hub_summary="Best for players who want strategy depth and do not mind the long ramp into competence.",
            related_guides=("multiplayer-beginner-checklist", "clear-team-communication"),
            visual_points=("25-45 min", "Team strategy", "Cosmetics + time unlocks"),
        ),
        game(
            slug="dota-2",
            name="Dota 2",
            genre="MOBA",
            official_url="https://www.dota2.com/",
            platforms=("PC",),
            platform_tags=("pc",),
            business_model="Free-to-play strategy game with cosmetic monetization and no power sales.",
            session_length="35-60 minute matches that demand sustained attention.",
            session_bucket="long",
            play_style="systems-heavy team strategy",
            hub_group="strategy",
            core_loop="Draft and pilot heroes, manage item timings, and make enough macro decisions to convert one opening into map control.",
            best_for="players who want maximum strategic freedom, long matches, and a ruleset that rewards deep systems knowledge",
            not_for="players who need quick onboarding, short queue commitments, or a gentle social environment",
            learning_barrier="Dota 2 is deliberately dense, and nearly every system offers meaningful complexity very early.",
            social_shape="Solo queue is possible, but a patient group or thick skin helps because the game is system-dense and communication-heavy.",
            progression_notes="The real progression is understanding heroes, timings, and win conditions; account power is minimal.",
            spending_notes="Core play is free, and spending is mostly cosmetic rather than competitive.",
            first_session_plan=(
                "Use the official tutorial and bot matches before letting live chaos define the game for you.",
                "Pick one support hero so the map and item layers stay readable.",
                "Read item descriptions during downtime instead of trying to memorize everything pre-match.",
                "Judge the game after you understand why an objective mattered, not after your first scoreboard line.",
            ),
            fit_questions=(
                "Do you enjoy complex rules for their own sake?",
                "Can you commit to long matches even when the result feels obvious early?",
                "Are you looking for strategic freedom more than smooth accessibility?",
            ),
            source_label="Official heroes overview",
            source_url="https://www.dota2.com/heroes",
            title="Dota 2 Before You Play: Is It a Fit for Strategy-Heavy Teams?",
            description="Read this sourced Dota 2 fit profile before you commit to its long matches, very high learning curve, and strategy-first social demands.",
            summary="Dota 2 fits strategy-first players who want decisions and counterplay more than accessibility.",
            onboarding_notes="Dota asks whether you enjoy feeling lost for a while in exchange for a much wider strategic sandbox later. If you do, few games match its depth. If you do not, the friction is immediate.",
            commitment_notes="Matches are long and mentally heavy enough that many players treat one or two strong games as a full session.",
            what_can_change=(
                "Hero balance and draft trends can transform what beginners are told to prioritize.",
                "Tutorial tooling and new-player surfaces can improve or degrade over time.",
                "Event cosmetics and storefront changes do not alter the core complexity described here.",
            ),
            review_hub_summary="A niche but powerful fit for players who want the deepest strategy sandbox in the library.",
            related_guides=("multiplayer-beginner-checklist", "clear-team-communication"),
            visual_points=("35-60 min", "Group helps", "Cosmetics only"),
        ),
    ]
)

GAMES.extend(
    [
        game(
            slug="apex-legends",
            name="Apex Legends",
            genre="Hero battle royale",
            official_url="https://www.ea.com/games/apex-legends/apex-legends",
            platforms=("PC", "PlayStation", "Xbox", "Switch"),
            platform_tags=("pc", "playstation", "xbox", "switch"),
            business_model="Free-to-play battle royale with cosmetic events and battle-pass monetization.",
            session_length="15-25 minute matches, with some extra setup time while learning maps and legends.",
            session_bucket="short",
            play_style="movement-heavy squad battle royale",
            hub_group="competitive",
            core_loop="Loot quickly, rotate with purpose, and combine squad abilities well enough to survive into the last circles.",
            best_for="duos or trios who love movement, hero synergy, and endgame decision making",
            not_for="players who hate looting downtime or being reset by one rough early drop",
            learning_barrier="Apex is readable on the surface, but movement, legend synergy, and map pacing all matter sooner than they look.",
            social_shape="Playable solo, but the game feels much better when you have even one partner who pings well or uses voice calmly.",
            progression_notes="Legend unlocks and account levels provide direction, yet mastery comes more from movement and rotation choices than raw grind.",
            spending_notes="Core access is free. Cosmetics, passes, and event items are the main monetized layers.",
            first_session_plan=(
                "Choose one forgiving legend and resist swapping characters every death.",
                "Land at one quieter point of interest for several matches so loot decisions become predictable.",
                "Use the ping wheel constantly, even if you are not on voice chat.",
                "Try to reach late ring at least once before judging whether the overall pace works for you.",
            ),
            fit_questions=(
                "Do you enjoy learning one map and rotation pattern instead of pure aim duels?",
                "Do you want shooter speed plus hero kits rather than one or the other?",
                "Are you willing to lose some early fights while the loot pace starts making sense?",
            ),
            source_label="Official game overview",
            source_url="https://www.ea.com/games/apex-legends/apex-legends/about",
            title="Apex Legends Before You Play: Is It a Fit for Movement-Focused Trio Players?",
            description="Use this sourced Apex Legends fit profile to judge its movement, squad dependence, legend learning curve, and event-driven cosmetic economy.",
            summary="Apex Legends fits players who want expressive movement and squad synergy more than pure pick-up-and-play simplicity.",
            onboarding_notes="Apex feels best when you like the rhythm of looting quickly, rotating with intent, and only taking the fights your squad can finish. If you mainly want nonstop arena action, the battle royale structure may feel slower than the movement suggests.",
            commitment_notes="The match length is manageable, but getting comfortable with maps and legend interactions takes more repetition than one evening reveals.",
            what_can_change=(
                "Map rotation and limited-time modes change season to season.",
                "Legend balance can alter which team styles feel easiest for beginners.",
                "Cosmetic events and collection pricing move independently of the core fit.",
            ),
            review_hub_summary="Best for squads who love movement and coordinated pushes; weaker if you hate looting or battle-royale downtime.",
            related_guides=("clear-team-communication", "crossplay-guide"),
            visual_points=("15-25 min", "Best in trios", "Pass + events"),
        ),
        game(
            slug="warframe",
            name="Warframe",
            genre="Cooperative action RPG",
            official_url="https://www.warframe.com/",
            platforms=("PC", "PlayStation", "Xbox", "Switch", "Mobile"),
            platform_tags=("pc", "playstation", "xbox", "switch", "mobile"),
            business_model="Free-to-play PvE action game with optional premium currency and convenience purchases.",
            session_length="10-40 minute missions, wrapped inside a much larger hobby-game structure.",
            session_bucket="flex",
            play_style="fast co-op loot progression",
            hub_group="progression",
            core_loop="Run missions, craft or rank new gear, and keep expanding the set of frames, weapons, and systems you understand.",
            best_for="players who want an enormous co-op grind with fast movement and lots of build experimentation",
            not_for="players who need a tidy tutorial path or immediate clarity on every system",
            learning_barrier="Warframe starts approachable in motion and becomes increasingly dense as mods, relics, open worlds, and currencies stack up.",
            social_shape="Warframe is comfortable solo or with drop-in co-op; a clan simply makes the larger system map easier to parse.",
            progression_notes="Progression is long-term and account-wide: new frames, weapons, mods, star-chart nodes, and quest unlocks all layer together.",
            spending_notes="Time can replace much spending, but premium currency and inventory convenience can tempt new players before they understand the economy.",
            first_session_plan=(
                "Finish the opening quest path and let the game teach the mission basics before chasing side systems.",
                "Use early platinum only after you understand whether inventory slots are the pressure point.",
                "Clear the next obvious star-chart nodes instead of bouncing between every new menu.",
                "Ask one specific system question at a time when you get confused instead of trying to decode the whole game at once.",
            ),
            fit_questions=(
                "Do you enjoy very long-term PvE progression more than clean onboarding?",
                "Can you tolerate learning a private vocabulary of mods, relics, and crafting over time?",
                "Will outside research feel like part of the hobby or an immediate turn-off?",
            ),
            source_label="Official game overview",
            source_url="https://www.warframe.com/game",
            title="Warframe Before You Play: A Fit Guide for Co-op Loot Hobbyists",
            description="This sourced Warframe fit profile covers its fast missions, dense long-term progression, optional spending pressure, and solo-or-co-op flexibility.",
            summary="Warframe fits players who want depth, speed, and a huge PvE backlog more than perfectly guided onboarding.",
            onboarding_notes="The real fit question is whether you enjoy being handed a very long menu of future goals. Warframe becomes rewarding once you accept that the early game is about learning vocabulary as much as combat feel.",
            commitment_notes="Short missions make Warframe easy to dip into, but understanding what to farm and when can still turn it into a serious hobby.",
            what_can_change=(
                "New quests, frames, and feature layers can alter recommended early priorities.",
                "Cross-save and cross-play support details can evolve by platform.",
                "Market pricing and convenience pressure are separate from the free core loop itself.",
            ),
            review_hub_summary="A great fit for players who love fast co-op PvE and do not mind learning many overlapping systems.",
            related_guides=("free-to-play-spending", "multiplayer-beginner-checklist"),
            visual_points=("10-40 min", "Solo or co-op", "Time-rich economy"),
        ),
        game(
            slug="genshin-impact",
            name="Genshin Impact",
            genre="Open-world action RPG",
            official_url="https://genshin.hoyoverse.com/",
            platforms=("PC", "PlayStation", "Xbox", "Mobile"),
            platform_tags=("pc", "playstation", "xbox", "mobile"),
            business_model="Free-to-play open-world RPG with gacha monetization and regular live updates.",
            session_length="15-90 minutes depending on whether you are exploring, questing, or doing dailies.",
            session_bucket="flex",
            play_style="solo exploration with live-service systems",
            hub_group="progression",
            core_loop="Explore, complete quests, build a small team around elemental reactions, and gradually strengthen characters through resource farming.",
            best_for="players who want a solo-first exploration game with live updates and character-building goals",
            not_for="anyone who dislikes gacha systems or mainly wants competitive multiplayer",
            learning_barrier="Genshin is easy to begin and becomes more layered once elemental reactions, resin, and team composition begin to matter.",
            social_shape="The game is primarily solo-friendly, with optional co-op rather than required scheduling.",
            progression_notes="Story, exploration, resin-spending, and character ascension drive the long-term pace more than a traditional endgame ladder.",
            spending_notes="The adventure is free to start, but wish banners reward strict budget discipline if you are vulnerable to limited-character hype.",
            first_session_plan=(
                "Play through the early regions long enough to judge whether exploration itself is satisfying.",
                "Test a few free or early characters before thinking about banners or optimal teams.",
                "Spend resin only on obvious early progression needs instead of chasing perfect efficiency.",
                "Leave the wish menu alone until you know whether you enjoy the world without paid pulls.",
            ),
            fit_questions=(
                "Do you want exploration and atmosphere more than competitive challenge?",
                "Can you ignore limited banners without feeling constant fear of missing out?",
                "Are you comfortable with story pacing that stretches between major updates?",
            ),
            source_label="Official game overview",
            source_url="https://genshin.hoyoverse.com/en/game",
            title="Genshin Impact Before You Play: Is It a Fit for Solo Explorers Who Pace Spending?",
            description="Read this sourced Genshin Impact fit profile before you commit to its exploration-first structure, resin pacing, and gacha economy.",
            summary="Genshin Impact fits players who want a relaxed exploration-first live game and can treat wishing as optional rather than mandatory.",
            onboarding_notes="The game is easiest to judge after a few regions of exploration, not after the opening cutscenes alone. If wandering, collecting, and building a small roster sounds inviting, it can become a dependable routine game.",
            commitment_notes="You can enjoy Genshin in short daily bursts or longer story blocks, but deeper optimization introduces ongoing calendar friction.",
            what_can_change=(
                "Character banners and limited events rotate continuously.",
                "Cross-save or login rules can differ by platform and account history.",
                "Resin advice and farming priorities change when new regions or systems arrive.",
            ),
            review_hub_summary="A strong fit for solo explorers who can separate the free world from the temptation of banner spending.",
            related_guides=("free-to-play-spending", "cloud-gaming-guide"),
            visual_points=("15-90 min", "Mostly solo", "Gacha caution"),
        ),
    ]
)


if __name__ == "__main__":
    main()
