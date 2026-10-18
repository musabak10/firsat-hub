"""Coderspace Bootcamp, Hackathon ve Etkinlik Scraper Modülü"""
import os
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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


class CoderspaceSource(Source):
    name = "coderspace"
    base_url = "https://coderspace.io"
    list_url = "https://coderspace.io/etkinlikler"

    def fetch(self) -> list[dict]:
        content = self.get(self.list_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        items = []

        # Coderspace kart kapsayıcıları
        cards = soup.select("div.group")
        seen_urls = set()

        for card in cards:
            link = card.select_one("a[href*='/etkinlikler/']")
            if not link:
                continue

            href = link.get("href", "")
            if not href or href in (
                "/etkinlikler/bootcamp/",
                "/etkinlikler/hackathon/",
                "/etkinlikler/hiring-challenge/",
                "/etkinlikler/meet-up/",
                "/etkinlikler/yetenek-programi/",
                "/etkinlikler/web3/",
            ):
                continue

            event_url = urljoin(self.base_url, href)
            if event_url in seen_urls:
                continue
            seen_urls.add(event_url)

            full_text = card.get_text(" ", strip=True).lower()
            if "tamamlandı" in full_text or "kapandı" in full_text or "sona erdi" in full_text:
                continue

            title_el = card.select_one("a.line-clamp-2, h3, h4, a[class*='font-heading']") or link
            title = title_el.get_text(strip=True) if title_el else ""
            if not title:
                continue

            desc_el = card.select_one("p.line-clamp-3, p")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            badge_el = card.select_one("span.inline-flex, span[class*='rounded'], [class*='badge']")
            badge = badge_el.get_text(strip=True) if badge_el else ""

            img = card.select_one("img")
            img_url = urljoin(self.base_url, img["src"]) if img and img.get("src") else None

            # Son Başvuru tarihi
            deadline = ""
            for s in card.select("span"):
                if "son başvuru" in s.get_text(strip=True).lower():
                    parent = s.parent
                    if parent:
                        deadline = parent.get_text(" ", strip=True)
                    break

            items.append({
                "title": title,
                "organization": "Coderspace",
                "description": desc,
                "deadline_text": deadline,
                "category_text": badge,
                "application_url": event_url,
                "source_url": event_url,
                "image_url": img_url,
            })

        return items


if __name__ == "__main__":
    src = CoderspaceSource()
    res = src.fetch()
    print(f"Coderspace: {len(res)} etkinlik bulundu.")
    for item in res[:3]:
        print(item)