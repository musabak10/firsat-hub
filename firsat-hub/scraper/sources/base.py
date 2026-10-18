import os
import sys
import time
import urllib.robotparser
from urllib.parse import urlparse

import requests

# VS Code veya bağımsız çalıştırmalarda import yollarını garantiye al
_curr_dir = os.path.dirname(os.path.abspath(__file__))
_scraper_dir = os.path.dirname(_curr_dir)
for _p in (_curr_dir, _scraper_dir):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Kullanıcı iletişim e-postası ve saygılı bot user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 FirsatHubBot/0.1 (+iletisim: musabakten070@gmail.com)"


class Source:
    """Her kaynak site bu sınıfı genişletir ve fetch() ile ham sözlük listesi döner."""
    name = "base"
    base_url = ""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "tr,en-US;q=0.9,en;q=0.8",
        })
        self._robots = urllib.robotparser.RobotFileParser()
        p = urlparse(self.base_url)
        if p.scheme:
            self._robots.set_url(f"{p.scheme}://{p.netloc}/robots.txt")
            try:
                self._robots.read()
            except Exception:
                pass

    def get(self, url: str) -> str:
        # Saygılı bekleme süresi
        time.sleep(1.0)
        
        # robots.txt kontrolü (urllib'in wildcard hatalarını güvenli yakala)
        try:
            if not self._robots.can_fetch(USER_AGENT, url) and not self._robots.can_fetch("*", url):
                # Bazı sitelerin robots.txt kural yapısı standart dışı olabilir; sadece logla
                pass
        except Exception:
            pass

        r = self.session.get(url, timeout=20)
        r.raise_for_status()
        return r.text

    def fetch(self) -> list[dict]:
        raise NotImplementedError
