"""Youthall Etkinlik ve Yarışma Scraper Modülü"""
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


class YouthallSource(Source):
    name = "youthall"
    base_url = "https://www.youthall.com"
    list_url = "https://www.youthall.com/tr/etkinlikler/"

    def fetch(self) -> list[dict]:
        content = self.get(self.list_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        items = []

        # Güncel Youthall etkinlik kartları: a.events-card__link veya genel kart yapısı
        cards = soup.select("a.events-card__link, a[class*='events-card']")
        seen_urls = set()

        for card in cards:
            href = card.get("href")
            if not href or not href.startswith("/tr/etkinlikler/"):
                continue

            # Alt kategori/filtre linklerini atla (/tr/etkinlikler/akademi/ vb.)
            parts = [p for p in href.strip("/").split("/") if p]
            if len(parts) <= 2:
                continue

            event_url = urljoin(self.base_url, href)
            if event_url in seen_urls:
                continue
            seen_urls.add(event_url)

            title_el = card.select_one(".events-card__title, h3, h2, [class*='title']")
            title = title_el.get_text(strip=True) if title_el else ""
            if not title:
                continue

            org_el = card.select_one(".events-card__org-name")
            org = org_el.get_text(strip=True) if org_el else "Youthall"

            full_text = card.get_text(" ", strip=True).lower()
            if "bitti" in full_text or "tamamlandı" in full_text or "kapandı" in full_text:
                continue

            # Tarih / Son Başvuru bilgisi
            deadline_el = card.select_one(".events-card__deadline-val, .events-card__deadline, [class*='deadline']")
            deadline_text = deadline_el.get_text(" ", strip=True) if deadline_el else ""
            if not deadline_text:
                when_el = card.select_one(".events-card__val, .events-card__when")
                deadline_text = when_el.get_text(" ", strip=True) if when_el else ""

            # Etkinlik türü ve etiketler
            tags = [t.get_text(strip=True) for t in card.select(".events-card__tag, [class*='tag']")]
            category_text = " ".join(tags)

            # Görsel
            img = card.select_one("img.events-card__img, img")
            image_url = urljoin(self.base_url, img["src"]) if img and img.get("src") else None

            items.append({
                "title": title,
                "organization": org,
                "description": f"{title} - {category_text}".strip(),
                "deadline_text": deadline_text,
                "category_text": category_text,
                "application_url": event_url,
                "source_url": event_url,
                "image_url": image_url,
            })

        return items


if __name__ == "__main__":
    src = YouthallSource()
    res = src.fetch()
    print(f"Youthall: {len(res)} etkinlik bulundu.")
    for item in res[:3]:
        print(item)