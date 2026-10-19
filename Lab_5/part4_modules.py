# Laborator: functii, metode si importuri pe web
# Student: Pavalchi Veronica

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import requests
import time
import re
import hashlib
import json
import socket
import ssl
from pathlib import Path
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser


# Exercitiul 35
def describe_url(url):
    """Afiseaza componentele unui URL, fara a accesa adresa."""
    parts = urlparse(url)
    print(parts.scheme, parts.netloc, parts.path, parts.query, parts.fragment)


# Exercitiul 36
def complete_urls(base, links):
    """Transforma legaturile relative in adrese complete."""
    return [urljoin(base, link) for link in links]


# Exercitiul 37
def extract_links(html):
    """Extrage href cu ghilimele duble, fara duplicate, in ordinea aparitiei."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))
    # Expresia ceruta are limite: nu recunoaste toate formele HTML posibile.


# Exercitiul 38
def split_links(links, domain):
    """Separa adresele HTTP(S) interne de externe; ignora mailto si javascript."""
    base = domain if "://" in domain else "https://" + domain
    internal, external = [], []
    for link in links:
        full = urljoin(base, link)
        parsed = urlparse(full)
        if parsed.scheme not in ("http", "https"):
            continue
        target = internal if parsed.netloc.lower() == urlparse(base).netloc.lower() else external
        if full not in target:
            target.append(full)
    return internal, external


# Exercitiul 39
class ImageFinder(HTMLParser):
    """Colecteaza atributele src ale tag-urilor img."""

    def __init__(self):
        """Pregateste parserul si lista de imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Este apelata automat de HTMLParser cand gaseste un tag de inceput."""
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def test_images():
    """Verifica parserul cu HTML al carui rezultat este cunoscut."""
    test_html = '''<html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fara src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>'''
    finder = ImageFinder()
    finder.feed(test_html)
    print(finder.images)
    assert finder.images == ["/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"], "Lista incorecta"
    print("Testul a trecut!")


# Exercitiul 40
def page_fingerprint(url):
    """Calculeaza amprenta SHA-256 a continutului primit."""
    time.sleep(1)
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


# Exercitiul 41
def save_and_read_headers(response):
    """Salveaza antetele langa script, le reciteste si afiseaza Content-Type."""
    path = Path(__file__).with_name("headers.json")
    with path.open("w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)
    with path.open(encoding="utf-8") as file:
        headers = json.load(file)
    print(requests.structures.CaseInsensitiveDict(headers).get("Content-Type", "lipseste"))


# Exercitiul 42
def resolve(hostname):
    """Returneaza o adresa IPv4 a domeniului prin DNS."""
    return socket.gethostbyname(hostname)


# Exercitiul 43
def cert_days_left(hostname):
    """Returneaza numarul de zile intregi pana la expirarea certificatului TLS."""
    time.sleep(1)
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure:
            expires = secure.getpeercert()["notAfter"]
    return int((ssl.cert_time_to_seconds(expires) - time.time()) // 86400)


def main():
    """Ruleaza exercitiile 35-43; testul local preceda cererile web."""
    print("35:")
    describe_url("https://cybercor.org/path?x=1#top")
    print("36:", complete_urls(BASE_URL, ["/about", "contact.html", "../index.html"]))
    test_images()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    links = extract_links(response.text)
    print("37:", links)
    internal, external = split_links(links, response.url)
    print("38 - Interne:", internal, "Externe:", external)
    finder = ImageFinder()
    finder.feed(response.text)
    print("39:", len(finder.images), "imagini gasite")
    for src in finder.images:
        print(src)
    print("Numar aproximativ prin count:", response.text.lower().count("<img"))
    # Comparam si cu sursa paginii din browser. Nu descarcam imaginile.
    first = page_fingerprint(BASE_URL)
    second = page_fingerprint(BASE_URL)
    print("40:", first, second, "Egale:", first == second)
    # Amprente diferite inseamna continut diferit, inclusiv continut dinamic.
    print("41:")
    save_and_read_headers(response)
    print("42:", resolve("cybercor.org"))
    print("43:", cert_days_left("cybercor.org"), "zile")


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, OSError, ValueError) as error:
        print("Nu am putut termina verificarile:", error)
