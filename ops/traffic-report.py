from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)
BOT_PATTERN = re.compile(
    r"bot|crawler|spider|slurp|scanner|curl|wget|python|lighthouse|pagespeed|headless",
    re.IGNORECASE,
)
ASSET_SUFFIXES = {
    ".css",
    ".js",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".json",
    ".xml",
    ".webmanifest",
}
SEARCH_HOSTS = {
    "google": ("google.",),
    "bing": ("bing.com",),
    "duckduckgo": ("duckduckgo.com",),
    "yahoo": ("search.yahoo.",),
    "yandex": ("yandex.",),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize GameRank Hub Nginx traffic without storing visitor IPs.")
    parser.add_argument("--log", type=Path, default=Path("/var/log/nginx/gamerankhub.access.log"))
    parser.add_argument("--output", type=Path, default=Path("/var/lib/gamerankhub/traffic/latest.json"))
    parser.add_argument("--hours", type=int, default=24)
    return parser.parse_args()


def parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z")


def is_pageview(method: str, path: str, status: int) -> bool:
    if method != "GET" or status >= 400 or path.startswith("/api/"):
        return False
    suffix = Path(urlsplit(path).path).suffix.lower()
    return suffix not in ASSET_SUFFIXES


def search_source(referrer: str) -> str | None:
    if not referrer or referrer == "-":
        return None
    host = urlsplit(referrer).hostname or ""
    for source, fragments in SEARCH_HOSTS.items():
        if any(fragment in host for fragment in fragments):
            return source
    return None


def build_report(log_path: Path, hours: int) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=hours)
    pageviews = 0
    bot_requests = 0
    total_requests = 0
    search_visits: Counter[str] = Counter()
    top_pages: Counter[str] = Counter()
    errors: Counter[str] = Counter()
    unique_visitors: set[str] = set()

    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = LOG_PATTERN.match(line)
            if not match:
                continue
            timestamp = parse_time(match["time"])
            if timestamp < cutoff:
                continue
            total_requests += 1
            status = int(match["status"])
            path = urlsplit(match["path"]).path
            agent = match["agent"]
            if BOT_PATTERN.search(agent):
                bot_requests += 1
                continue
            if status >= 400:
                errors[f"{status} {path}"] += 1
            if is_pageview(match["method"], path, status):
                pageviews += 1
                unique_visitors.add(match["ip"])
                top_pages[path] += 1
                source = search_source(match["referrer"])
                if source:
                    search_visits[source] += 1

    return {
        "generated_at": now.isoformat(),
        "window_hours": hours,
        "total_requests": total_requests,
        "human_pageviews": pageviews,
        "estimated_unique_visitors": len(unique_visitors),
        "bot_requests": bot_requests,
        "search_referrals": dict(search_visits.most_common()),
        "top_pages": dict(top_pages.most_common(20)),
        "top_errors": dict(errors.most_common(20)),
        "privacy_note": "Visitor IP addresses are counted in memory and are not written to this report.",
    }


def main() -> None:
    args = parse_args()
    report = build_report(args.log, args.hours)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
