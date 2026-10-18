# Fırsat Hub

Next.js 15 + Tailwind CSS + Supabase web uygulaması ve Python fırsat/etkinlik scraper'ı.

Öğrenciler ve yeni mezunlar için staj, hackathon, bootcamp, yarışma ve konferansları tek merkezden toplayıp listeler.

---

## Desteklenen Kaynaklar (Scraper Sources)

1. **Youthall** (`youthall.com`): Zirveler, hackathonlar, yarışmalar, staj programları.
2. **Coderspace** (`coderspace.io`): Bootcamp, datathon, hiring challenge ve teknoloji etkinlikleri.
3. **Techcareer.net** (`techcareer.net`): Bootcamp, yapay zeka kulüpleri ve atölyeler.
4. **Patika.dev** (`patika.dev`): IBM, Akbank ve kurumsal bootcamp'ler, hackathonlar, stajlar.
5. **Kommunity** (`kommunity.com`): Topluluk etkinlikleri ve buluşmalar.

---

## Yerel Kurulum (Local Development)

### 1. Web Uygulaması (Next.js)

```bash
# Bağımlılıkları yükle
npm install

# .env.local dosyasını kontrol et (mevcut değilse .env.example'dan kopyala)
# NEXT_PUBLIC_SUPABASE_URL ve NEXT_PUBLIC_SUPABASE_ANON_KEY tanımlı olmalı

# Geliştirme sunucusunu başlat
npm run dev
```

Tarayıcıda [http://localhost:3000](http://localhost:3000) adresine gidin.

### 2. Scraper'ı Çalıştırma (Python)

```bash
# Sanal ortamı aktifleştir (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r scraper/requirements.txt

# Scraper'ı çalıştır
python scraper/main.py
```

> **Not:** VS Code kullanıyorsanız doğrudan `F5` tuşuna basarak veya `scraper/main.py` dosyasını açıp sağ üstteki "Run Python File" butonuna basarak da scraper'ı çalıştırabilirsiniz. `.vscode` ayarları otomatik olarak tanımlanmıştır.

### 3. Supabase Veritabanı ve Yetkiler

- Tablo şeması için `supabase/schema.sql` dosyasını Supabase SQL Editor'de çalıştırın.
- Scraper'ın veritabanına doğrudan kayıt ekleyebilmesi için `.env.local` dosyasına Supabase Dashboard > Settings > API altındaki `service_role` gizli anahtarını `SUPABASE_SERVICE_KEY` olarak ekleyin.

---

## İletişim

Sorularınız ve geri bildirimleriniz için:
- **E-posta:** [musabakten070@gmail.com](mailto:musabakten070@gmail.com)
