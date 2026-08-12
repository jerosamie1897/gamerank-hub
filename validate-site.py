from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML_FILES = list(ROOT.rglob("*.html"))
errors: list[str] = []
titles: defaultdict[str, list[Path]] = defaultdict(list)
descriptions: defaultdict[str, list[Path]] = defaultdict(list)
canonical_to_page: dict[str, Path] = {}
long_paragraphs: Counter[str] = Counter()


def local_target(source: Path, href: str) -> Path | None:
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return None
    clean = href.strip().split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None
    return (source.parent / clean).resolve()


for page in HTML_FILES:
    text = page.read_text(encoding="utf-8")
    relative = page.relative_to(ROOT)
    for required in ('<meta name="description"', '<link rel="canonical"', 'application/ld+json'):
        if required not in text:
            errors.append(f"{relative}: missing {required}")
    for href in re.findall(r'(?:href|src)="([^"]+)"', text):
        target = local_target(page, href)
        if target is not None and not target.exists():
            errors.append(f"{relative}: broken local reference {href}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON-LD: {exc}")
    title_match = re.search(r"<title>(.*?)</title>", text, re.S)
    description_match = re.search(r'<meta name="description" content="([^"]+)"', text)
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', text)
    if title_match:
        titles[re.sub(r"\s+", " ", title_match.group(1)).strip()].append(relative)
    if description_match:
        descriptions[description_match.group(1).strip()].append(relative)
    if canonical_match:
        canonical = canonical_match.group(1).strip()
        if canonical in canonical_to_page:
            errors.append(f"{relative}: duplicate canonical also used by {canonical_to_page[canonical]}")
        canonical_to_page[canonical] = relative
    if relative.parts and relative.parts[0] in {"reviews", "guides", "blog"}:
        for paragraph in re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", text, re.S):
            plain = re.sub(r"<[^>]+>", " ", paragraph)
            plain = re.sub(r"\s+", " ", plain).strip()
            if len(plain) >= 220:
                long_paragraphs[plain] += 1

for title, pages in titles.items():
    if len(pages) > 1:
        errors.append(f"Duplicate title on {', '.join(map(str, pages))}: {title}")

for description, pages in descriptions.items():
    if len(pages) > 1:
        errors.append(f"Duplicate meta description on {', '.join(map(str, pages))}")

for paragraph, count in long_paragraphs.items():
    if count >= 8:
        errors.append(f"Long paragraph repeated across {count} generated pages: {paragraph[:100]}...")

for review_page in (ROOT / "reviews").glob("*.html"):
    if review_page.name == "index.html":
        continue
    text = review_page.read_text(encoding="utf-8")
    relative = review_page.relative_to(ROOT)
    if '"@type":"Review"' in text or '"@type": "Review"' in text:
        errors.append(f"{relative}: unsupported Review schema; use Article/WebPage for sourced profiles")
    if not re.search(r"official (?:source|site)|source links?", text, re.I):
        errors.append(f"{relative}: missing visible official source section")
    if not re.search(r"hands-on|hands on|not a scored review", text, re.I):
        errors.append(f"{relative}: missing testing limitation disclosure")

for xml_name in ("sitemap.xml", "feed.xml"):
    try:
        ET.parse(ROOT / xml_name)
    except ET.ParseError as exc:
        errors.append(f"{xml_name}: invalid XML: {exc}")

report = json.loads((ROOT / "content-report.json").read_text(encoding="utf-8"))
if report["html_pages"] != len(HTML_FILES):
    errors.append(f"Content report lists {report['html_pages']} HTML pages, found {len(HTML_FILES)}")

try:
    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = [node.text.strip() for node in sitemap.findall(".//sm:loc", namespace) if node.text]
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("sitemap.xml contains duplicate URLs")
    for url in sitemap_urls:
        if url not in canonical_to_page:
            errors.append(f"sitemap.xml URL has no matching canonical page: {url}")
except ET.ParseError:
    pass

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(json.dumps(report, indent=2))
print(f"Validated {len(HTML_FILES)} HTML pages for links, metadata, schema, duplication, and sitemap consistency.")
