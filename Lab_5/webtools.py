# Laborator: functii, metode si importuri pe web
# Student: Pavalchi Veronica

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import requests
import time


# Exercitiul 21 - Prima versiune
def fetch(url):
    """Returneaza raspunsul primit de la adresa indicata."""
    time.sleep(1)
    return requests.get(url, timeout=TIMEOUT)


fetch_initial = fetch  # pastram prima versiune pentru demonstratie


# Exercitiul 23 - Versiunea extinsa a lui fetch din exercitiul 21
def fetch(url, timeout=TIMEOUT):
    """Returneaza raspunsul; timeout poate fi schimbat la apel."""
    time.sleep(1)  # pauza inaintea fiecarei cereri
    headers = DEFAULT_HEADERS if urlparse(url).hostname == "httpbin.org" else {}
    return requests.get(url, timeout=timeout, headers=headers)


# Exercitiile 22 si 26
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP al adresei."""
    return fetch(url).status_code


# Exercitiile 24, 25 si 26
def get_title(html: str) -> str:
    """Extrage titlul din HTML fara sa faca o cerere de retea."""
    start = html.lower().find("<title>")
    if start == -1:
        return "Titlu negasit"
    start += len("<title>")
    end = html.lower().find("</title>", start)
    if end == -1:
        return "Titlu negasit"
    return html[start:end].strip()


# Exercitiul 27
def page_exists(url):
    """Returneaza True pentru un raspuns 2xx, altfel False."""
    try:
        response = fetch(url)
        return 200 <= response.status_code < 300
    except requests.RequestException:
        return False


# Exercitiul 28
def check_paths(base, paths):
    """Returneaza codurile cailor; None inseamna eroare de conexiune."""
    results = {}
    for path in paths:
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None
    return results


# Exercitiul 29
def get_header(url, name, default="lipseste"):
    """Returneaza un antet sau valoarea implicita daca acesta lipseste."""
    return fetch(url).headers.get(name, default)


# Exercitiul 30
def security_headers(url):
    """Verifica prezenta celor cinci antete cerute in laborator."""
    response = fetch(url)
    names = ["Strict-Transport-Security", "Content-Security-Policy",
             "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"]
    results = {}
    for name in names:
        results[name] = name in response.headers
    return results


# Exercitiul 31
def score_headers(results):
    """Returneaza numarul antetelor prezente raportat la total."""
    return str(sum(results.values())) + "/" + str(len(results))
    # Prezenta antetelor nu reprezinta un audit complet de securitate.


# Exercitiul 32
def fetch_robots(base):
    """Returneaza robots.txt sau None la lipsa ori eroare de acces."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return None


def disallowed_paths(robots_text):
    """Extrage valorile Disallow nevida; accepta si None."""
    paths = []
    if robots_text is None:
        return paths
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()
        name, separator, value = line.partition(":")
        if separator and name.strip().lower() == "disallow" and value.strip():
            paths.append(value.strip())
    return paths
    # Extragem toate valorile, fara interpretarea grupurilor User-agent.
    # robots.txt da instructiuni robotilor; nu este o protectie prin parola.


# Exercitiul 33
def response_times(*urls):
    """Returneaza duratele cererilor, fara pauza; None la eroare."""
    results = {}
    for url in urls:
        time.sleep(1)
        start = time.perf_counter()
        try:
            requests.get(url, timeout=TIMEOUT)
            results[url] = time.perf_counter() - start
        except requests.RequestException:
            results[url] = None
    return results


# Exercitiul 34
def log(message, **details):
    """Afiseaza mesajul si detaliile primite prin argumente cu nume."""
    parts = [message]
    for name, value in details.items():
        parts.append(name + "=" + str(value))
    print(" | ".join(parts))


# Exercitiile 44-47: modul reutilizabil
DEFAULT_HEADERS = {"User-Agent": "WebLab-Pavalchi-Veronica"}

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


# Exercitiul 50
def site_report(url):
    """Colecteaza informatiile, afiseaza raportul si salveaza report.json."""
    hostname = urlparse(url).hostname
    report = {"url": url, "status_code": None, "final_url": None,
              "title": None, "ip": None, "redirects": [],
              "http_final_url": None, "security_headers": None,
              "security_score": None, "certificate_days_left": None,
              "internal_links": None, "external_links": None,
              "disallowed_paths": None, "errors": []}
    try:
        response = fetch(url)
        report["status_code"] = response.status_code
        report["final_url"] = response.url
        report["title"] = get_title(response.text)
        internal, external = split_links(extract_links(response.text), response.url)
        report["internal_links"] = len(internal)
        report["external_links"] = len(external)
    except requests.RequestException as error:
        report["errors"].append("Pagina: " + str(error))
    try:
        report["ip"] = resolve(hostname)
    except OSError as error:
        report["errors"].append("DNS: " + str(error))
    try:
        response = fetch("http://" + urlparse(url).netloc)
        report["redirects"] = [
            {"status": step.status_code, "url": step.url,
             "location": step.headers.get("Location")}
            for step in response.history
        ]
        report["http_final_url"] = response.url
    except requests.RequestException as error:
        report["errors"].append("Redirectionari: " + str(error))
    try:
        headers = security_headers(url)
        report["security_headers"] = headers
        report["security_score"] = score_headers(headers)
    except requests.RequestException as error:
        report["errors"].append("Antete: " + str(error))
    try:
        report["certificate_days_left"] = cert_days_left(hostname)
    except (OSError, ValueError, KeyError) as error:
        report["errors"].append("Certificat: " + str(error))
    robots = fetch_robots(url)
    if robots is None:
        report["errors"].append("robots.txt lipseste sau nu a putut fi citit.")
    else:
        report["disallowed_paths"] = disallowed_paths(robots)
    print("=== Raport site:", url, "===")
    labels = {"status_code": "Cod de stare", "final_url": "URL final",
              "title": "Titlu", "ip": "Adresa IP", "redirects": "Redirectionari",
              "http_final_url": "Destinatie HTTP", "security_score": "Scor antete",
              "certificate_days_left": "Zile certificat", "internal_links": "Legaturi interne",
              "external_links": "Legaturi externe", "disallowed_paths": "Valori Disallow"}
    for key, label in labels.items():
        print(label + ":", report[key] if report[key] is not None else "indisponibil")
    for error in report["errors"]:
        print("Observatie:", error)
    path = Path(__file__).with_name("report.json")
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
    print("Salvat in", path.name)
    return report


# Exercitiul 46 - ruleaza doar cand pornim direct webtools.py
if __name__ == "__main__":
    try:
        print("Autotest:", get_status(BASE_URL))
    except requests.RequestException as error:
        print("Autotestul nu a putut contacta site-ul:", error)

