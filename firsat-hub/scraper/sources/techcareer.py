"""Techcareer.net Etkinlik Scraper Modülü

Techcareer Next.js SSR kullanıyor. Sayfa HTML'indeki __NEXT_DATA__ JSON bloğu
tüm etkinlik verisini yapılandırılmış şekilde içeriyor — HTML parse'a gerek yok.
"""
import json
import os
import re
import sys

# VS Code veya doğrudan çalıştırma durumunda import güvenliği
_curr = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_curr)
for _p in (_curr, _parent):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from .base import Source
except (ImportError, ValueError):
    from base import Source


class TechcareerSource(Source):
    name = "techcareer"
    base_url = "https://www.techcareer.net"
    list_url = "https://www.techcareer.net/events"

    def fetch(self) -> list[dict]:
        content = self.get(self.list_url)
        if not content:
            return []

        # __NEXT_DATA__ script bloğundan JSON'u çıkar
        match = re.search(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', content)
        if not match:
            return []

        try:
            next_data = json.loads(match.group(1))
        except json.JSONDecodeError:
            return []

        events_data = (
            next_data
            .get("props", {})
            .get("pageProps", {})
            .get("openEvents", {})
            .get("data", [])
        )

        items = []
        for event in events_data:
            attrs = event.get("attributes", {})
            title = (attrs.get("title") or "").strip()
            if not title:
                continue

            slug = attrs.get("slug", "")
            external_link = attrs.get("externalLink", "")
            event_url = external_link or f"{self.base_url}/events/{slug}"

            items.append({
                "title": title,
                "organization": "Techcareer.net",
                "description": (attrs.get("subTitle") or "").strip(),
                "deadline_text": attrs.get("deadlineText") or attrs.get("deadline") or "",
                "category_text": attrs.get("eventType") or "Bootcamp",
                "application_url": event_url,
                "source_url": f"{self.base_url}/events/{slug}",
                "image_url": attrs.get("image"),
            })

        return items


if __name__ == "__main__":
    src = TechcareerSource()
    res = src.fetch()
    print(f"Techcareer: {len(res)} etkinlik bulundu.")
    for item in res[:3]:
        print(item)
