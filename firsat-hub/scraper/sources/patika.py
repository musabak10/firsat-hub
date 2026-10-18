"""Patika.dev Bootcamp, Hackathon ve Kariyer Fırsatları Scraper Modülü"""
import os
import re
import sys
from urllib.parse import unquote, urljoin
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


class PatikaSource(Source):
    name = "patika"
    base_url = "https://www.patika.dev"
    list_url = "https://www.patika.dev/bootcamp"

    def fetch(self) -> list[dict]:
        content = self.get(self.list_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        items = []

        cards = soup.select("a[href^='/bootcamp/']")
        seen_urls = set()

        for card in cards:
            href = card.get("href", "")
            if not href or href == "/bootcamp":
                continue

            full_text = card.get_text(" ", strip=True)
            lower_text = full_text.lower()

            # Başvurusu kapanmış veya süresi bitmiş eski arşiv programlarını atla
            if "başvurular kapandı" in lower_text or "tamamlandı" in lower_text or "kapandı" in lower_text:
                continue

            # Geçmiş yıllara ait arşiv etkinliklerini atla (2025 ve öncesi)
            if re.search(r"\b(201\d|202[0-5])\b", full_text):
                continue

            event_url = urljoin(self.base_url, href)
            if event_url in seen_urls:
                continue
            seen_urls.add(event_url)

            title_el = card.select_one("h2, h3, [class*='font-bold'], [class*='font-semibold']")
            title = title_el.get_text(strip=True) if title_el else ""
            if not title:
                continue

            desc_el = card.select_one("p")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            # Görsel URL'sini çıkar
            img = card.select_one("img")
            img_url = None
            if img:
                src = img.get("src", "")
                if "url=" in src:
                    m = re.search(r"url=([^&]+)", src)
                    if m:
                        src = unquote(m.group(1))
                img_url = urljoin(self.base_url, src)

            # Son başvuru tarihi ayrıştırma
            deadline_match = re.search(r"Son\s+ba[sş]vuru:\s*([^\n\r]+)", full_text, re.IGNORECASE)
            deadline_text = deadline_match.group(1).strip() if deadline_match else ""
            if not deadline_text and "başvurular açık" in lower_text:
                deadline_text = "Başvurular Açık"

            # Kategori tahmini
            cat_text = "Bootcamp"
            lower_title = title.lower()
            if "hackathon" in lower_title or "datathon" in lower_title:
                cat_text = "Hackathon"
            elif "staj" in lower_title or "internship" in lower_title:
                cat_text = "Staj"
            elif "yarışma" in lower_title or "yarisma" in lower_title or "challenge" in lower_title:
                cat_text = "Yarışma"

            items.append({
                "title": title,
                "organization": "Patika.dev",
                "description": desc,
                "deadline_text": deadline_text,
                "category_text": cat_text,
                "application_url": event_url,
                "source_url": event_url,
                "image_url": img_url,
            })

        return items


if __name__ == "__main__":
    src = PatikaSource()
    res = src.fetch()
    print(f"Patika: {len(res)} aktif fırsat bulundu.")
    for item in res:
        print(f"- {item['title']} | Son Başvuru: {item['deadline_text']}")
