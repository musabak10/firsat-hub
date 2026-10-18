import os
import sys

# VS Code veya farklı dizinlerden çalıştırıldığında import'ların sorunsuz çalışmasını sağla
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
for path in (CURRENT_DIR, PROJECT_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

# Eğer ortam değişkenleri terminalde set edilmemişse .env.local dosyasından yükle
def load_env_file(filepath: str):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip("'\"")
            if k not in os.environ:
                os.environ[k] = v

load_env_file(os.path.join(PROJECT_ROOT, ".env.local"))
load_env_file(os.path.join(PROJECT_ROOT, ".env"))

# Supabase URL / Key eşlemeleri (NEXT_PUBLIC_ veya standart)
if "SUPABASE_URL" not in os.environ and "NEXT_PUBLIC_SUPABASE_URL" in os.environ:
    os.environ["SUPABASE_URL"] = os.environ["NEXT_PUBLIC_SUPABASE_URL"]
if "SUPABASE_SERVICE_KEY" not in os.environ and "SUPABASE_SERVICE_ROLE_KEY" in os.environ:
    os.environ["SUPABASE_SERVICE_KEY"] = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

try:
    from supabase import create_client
except ImportError:
    print("[HATA] 'supabase' kütüphanesi bulunamadı. Lütfen 'pip install -r requirements.txt' çalıştırın.")
    create_client = None

# Kaynak modülleri içe aktar
try:
    from normalize import normalize
    from sources.youthall import YouthallSource
    from sources.coderspace import CoderspaceSource
    from sources.techcareer import TechcareerSource
    from sources.patika import PatikaSource
    from sources.kommunity import KommunitySource
except ImportError:
    from scraper.normalize import normalize
    from scraper.sources.youthall import YouthallSource
    from scraper.sources.coderspace import CoderspaceSource
    from scraper.sources.techcareer import TechcareerSource
    from scraper.sources.patika import PatikaSource
    from scraper.sources.kommunity import KommunitySource

SOURCES = [
    YouthallSource(),
    CoderspaceSource(),
    TechcareerSource(),
    PatikaSource(),
]


def main() -> int:
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = (os.getenv("SUPABASE_SERVICE_KEY") or "").strip()

    if not supabase_url or not service_key:
        print("=" * 65)
        print("[TEST / ÖNİZLEME MODU]")
        print("SUPABASE_SERVICE_KEY tanımlı olmadığı için veritabanına yazılmayacak.")
        print("Tüm kaynaklar taranıp bulunan etkinlikler konsola listelenecek.")
        print("Kalıcı kayıt için .env.local dosyasına:")
        print("SUPABASE_SERVICE_KEY=<Supabase Settings > API > service_role key>")
        print("eklemeniz yeterlidir.")
        print("=" * 65 + "\n")
        db = None
    else:
        db = create_client(supabase_url, service_key)

    status = "approved" if os.getenv("AUTO_APPROVE") == "1" else "pending"

    seen_urls = set()
    seen_hashes = set()

    if db:
        try:
            existing = db.table("events").select("source_url,content_hash").execute().data
            seen_urls = {r["source_url"] for r in existing if r.get("source_url")}
            seen_hashes = {r["content_hash"] for r in existing if r.get("content_hash")}
        except Exception as e:
            print(f"[UYARI] Mevcut kayıtlar okunamadı: {e}")

    failed = False
    total_found = 0
    total_new = 0

    for src in SOURCES:
        print(f"--> [{src.name}] taranıyor...")
        try:
            raw_items = src.fetch()
        except Exception as e:
            print(f"  [HATA] {src.name}: {e}")
            failed = True
            continue

        if not raw_items:
            print(f"  [UYARI] {src.name}: 0 sonuç.")
            continue

        new_rows = []
        for raw in raw_items:
            row = normalize(raw, src.name)
            if not row or row["source_url"] in seen_urls or row["content_hash"] in seen_hashes:
                continue
            row["status"] = status
            seen_urls.add(row["source_url"])
            seen_hashes.add(row["content_hash"])
            new_rows.append(row)

        total_found += len(raw_items)
        total_new += len(new_rows)

        if db and new_rows:
            try:
                db.table("events").insert(new_rows).execute()
                print(f"  [OK] {src.name}: {len(raw_items)} bulundu, {len(new_rows)} veritabanına eklendi.")
            except Exception as e:
                err_str = str(e)
                if "row-level security" in err_str.lower():
                    print(f"  [UYARI] {src.name}: Supabase RLS yazma izni vermedi (anon key ile yazma yetkisi yok).")
                    print("         --> Çözüm: .env.local dosyasına Supabase service_role anahtarınızı SUPABASE_SERVICE_KEY olarak ekleyin.")
                else:
                    print(f"  [HATA] {src.name} veritabanına eklenirken hata: {e}")
                failed = True
        else:
            print(f"  [OK] {src.name}: {len(raw_items)} bulundu ({len(new_rows)} yeni/benzersiz).")

    print(f"\n[TAMAMLANDI] Toplam {total_found} fırsat tarandı, {total_new} yeni kayıt tespit edildi.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
