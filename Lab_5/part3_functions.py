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
    return requests.get(url, timeout=timeout)


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


def main():
    """Apeleaza functiile din exercitiile 21-34."""
    # Apelam versiunea initiala a functiei fetch, pastrata sub alt nume.
    print("21:", fetch_initial(BASE_URL).status_code)
    for path in ["/", "/robots.txt", "/sitemap.xml"]:
        print("22:", path, get_status(BASE_URL + path))
    print("23, implicit:", fetch(BASE_URL).status_code)
    print("23, trei secunde:", fetch(BASE_URL, timeout=3).status_code)
    print("24:", get_title(fetch(BASE_URL).text))
    print("25:")
    help(get_title)
    try:
        get_status(123)
    except requests.RequestException as error:
        print("26: Adnotarea nu opreste apelul; requests respinge URL-ul:", error)
    # Adnotarile sunt indicatii de tip, nu verificari automate la executie.
    print("27:", page_exists(BASE_URL))
    print("27, domeniu invalid:", page_exists("https://this-domain-does-not-exist.invalid"))
    print("28:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))
    print("29:", get_header(url=BASE_URL, name="Server"))
    print("30:", security_headers(BASE_URL))
    print("31:", score_headers(security_headers(BASE_URL)))
    print("32:", disallowed_paths(fetch_robots(BASE_URL)))
    print("32, None:", disallowed_paths(None))
    print("33:", response_times(BASE_URL, BASE_URL + "/robots.txt"))
    log("verificat", url=BASE_URL, status=get_status(BASE_URL))
    # print afiseaza; return trimite valoarea inapoi pentru a fi reutilizata.


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print("O cerere nu a reusit. Verifica internetul si reincearca:", error)
