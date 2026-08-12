from __future__ import annotations

import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HOST = "gamerankhub.com"
KEY = "75eb4cdb1fc2b16251c9bc3e4adbf74a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

sitemap = ET.parse(ROOT / "sitemap.xml")
urls = [
    node.text
    for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    if node.text
]
payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": urls,
}).encode()
request = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "GameRankHub/1.0"},
    method="POST",
)
with urllib.request.urlopen(request, timeout=30) as response:
    print(f"IndexNow accepted {len(urls)} URLs with HTTP {response.status}.")
