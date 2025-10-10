from __future__ import annotations
import feedparser
from typing import Iterable


def fetch_headlines(feeds: Iterable[dict], limit: int = 5) -> list[dict]:
    items: list[dict] = []
    for f in feeds:
        parsed = feedparser.parse(f["url"]) # lenient e gratuito
        for e in parsed.entries[:limit]:
            items.append({
                "source": f["name"],
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "published": e.get("published", ""),
            })
    return items