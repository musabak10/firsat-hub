"""Kommunity Etkinlik Scraper Modülü

Kommunity topluluk etkinliklerini listeler.
"""
import os
import sys
from urllib.parse import urljoin

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


class KommunitySource(Source):
    name = "kommunity"
    base_url = "https://kommunity.com"
    api_url = "https://api.kommunity.com/api/v1/events"

    def fetch(self) -> list[dict]:
        try:
            r = self.session.get(f"{self.api_url}?type=upcoming&country=TR", timeout=15)
            if r.status_code != 200:
                return []
            data = r.json().get("data", [])
        except Exception:
            return []

        items = []
        for event in data:
            title = (event.get("name") or "").strip()
            if not title:
                continue

            community = event.get("community", {}).get("name") or "Kommunity"
            slug = event.get("slug", "")
            comm_slug = event.get("community", {}).get("slug", "")
            event_url = f"{self.base_url}/{comm_slug}/events/{slug}" if comm_slug and slug else f"{self.base_url}/events/{slug}"
            start_date = event.get("start_date", {}).get("date", "")

            items.append({
                "title": title,
                "organization": community,
                "description": f"{community} topluluk etkinliği",
                "deadline_text": start_date,
                "category_text": "Konferans",
                "application_url": event_url,
                "source_url": event_url,
                "image_url": event.get("highlight_photo"),
            })

        return items


if __name__ == "__main__":
    src = KommunitySource()
    res = src.fetch()
    print(f"Kommunity: {len(res)} etkinlik bulundu.")
