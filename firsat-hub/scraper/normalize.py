"""Ham veriyi tek tip hale getirir: kategori, seviye, tarih, hash."""
import hashlib
import re
from datetime import datetime, timezone

import dateparser
from slugify import slugify

CATEGORY_KEYWORDS = {
    "hackathon": ["hackathon", "hackaton", "kodlama maratonu"],
    "bootcamp": ["bootcamp", "boot-camp", "boot camp", "kamp"],
    "staj": ["staj", "intern"],
    "yarisma": ["yarışma", "yarisma", "competition", "challenge", "ödül"],
    "konferans": ["konferans", "webinar", "zirve", "summit", "panel", "etkinlik"],
}
LEVEL_KEYWORDS = {
    "yuksek-lisans": ["yüksek lisans", "yuksek lisans", "master", "msc", "lisansüstü"],
    "lisans": ["lisans", "üniversite", "universite", "undergraduate", "bachelor"],
    "lise": ["lise", "high school", "ortaöğretim"],
}


def guess_category(text: str) -> str:
    t = text.lower()
    for cat, words in CATEGORY_KEYWORDS.items():
        if any(w in t for w in words):
            return cat
    return "konferans"


def guess_levels(text: str) -> list[str]:
    t = text.lower()
    found = [lvl for lvl, words in LEVEL_KEYWORDS.items() if any(w in t for w in words)]
    # "yüksek lisans" metni "lisans" kelimesini de içerir; açıkça yazılmadıysa lisansı ele
    if "yuksek-lisans" in found and "lisans" in found and not re.search(r"(?<!yüksek )(?<!yuksek )lisans(?!üstü)", t):
        found.remove("lisans")
    return found or ["lisans"]


def parse_deadline(text: str | None) -> str | None:
    """'15 Kasım 2026', '20 Ekim', '15.11.26' gibi metinleri UTC ISO'ya çevirir. Geçmiş yılları ve süresi dolmuşları eler."""
    if not text:
        return None

    # "Son Başvuru", "Etkinlik", "Bilet satışı" gibi Türkçe ön ekleri ayıkla
    clean = re.sub(r"(?i)\b(son\s*ba[sş]vuru|etkinlik|tarih|bilet\s*sat[ıi][sş][ıi])\s*:?\s*", "", text).strip()
    if not clean or clean.lower() in ("sürekli", "başvurular açık", "açık"):
        return None

    # Açıkça geçmiş bir yıl geçiyorsa (2025 ve öncesi) doğrudan atla
    if re.search(r"\b(201\d|202[0-5])\b", clean):
        return None

    d = dateparser.parse(
        clean,
        languages=["tr", "en"],
        settings={
            "TIMEZONE": "Europe/Istanbul",
            "RETURN_AS_TIMEZONE_AWARE": True,
            "PREFER_DATES_FROM": "future",
            "DATE_ORDER": "DMY",
        },
    )
    if not d:
        return None

    if d.hour == 0 and d.minute == 0:  # sadece gün verildiyse günün sonu
        d = d.replace(hour=23, minute=59)

    d_utc = d.astimezone(timezone.utc)
    # Eğer hesaplanan tarih şu andan eskiyse süresi dolmuştur
    if d_utc < datetime.now(timezone.utc):
        return None

    return d_utc.isoformat()


def content_hash(title: str, organization: str) -> str:
    key = re.sub(r"\W+", " ", f"{title} {organization}".lower()).strip()
    return hashlib.sha1(key.encode()).hexdigest()


def make_slug(title: str, organization: str) -> str:
    base = slugify(f"{title} {organization}")[:80]
    return f"{base}-{content_hash(title, organization)[:6]}"


def normalize(raw: dict, source: str) -> dict | None:
    """raw: title, organization, application_url, description?, deadline_text?, image_url?, category_text?, level_text?"""
    title = (raw.get("title") or "").strip()
    url = (raw.get("application_url") or "").strip()
    org = (raw.get("organization") or "").strip() or source
    if not title or not url:
        return None

    # Geçmiş yıl tespiti (2025 ve öncesi bir yıl belirtilmişse eski etkinliktir)
    deadline_raw = (raw.get("deadline_text") or "").strip()
    if re.search(r"\b(201\d|202[0-5])\b", deadline_raw):
        return None

    deadline = parse_deadline(deadline_raw)

    blob = f"{title} {raw.get('category_text', '')} {raw.get('description', '')}"
    return {
        "slug": make_slug(title, org),
        "title": title,
        "organization": org,
        "description": (raw.get("description") or "").strip() or None,
        "category": guess_category(blob),
        "education_levels": guess_levels(f"{raw.get('level_text', '')} {blob}"),
        "application_url": url,
        "image_url": raw.get("image_url") or None,
        "deadline": deadline,
        "is_online": bool(re.search(r"online|çevrimiçi|cevrimici|uzaktan", blob.lower())),
        "source": source,
        "source_url": raw.get("source_url") or url,
        "content_hash": content_hash(title, org),
    }
