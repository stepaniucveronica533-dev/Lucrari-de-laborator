# Laborator: functii, metode si importuri pe web
# Student: Pavalchi Veronica

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import requests
import time


def main():
    """Demonstreaza exercitiile 9-20."""
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    # Exercitiul 9 - Atribute
    print("Exercitiul 9")
    print(response.status_code)  # atribut: codul de stare
    print(response.ok)           # atribut: True pentru coduri sub 400
    print(response.url)          # atribut: adresa finala
    print(response.encoding)     # atribut: codificarea textului

    # Exercitiul 10 - Tratarea erorilor HTTP
    try:
        response.raise_for_status()
        print("Pagina principala nu are eroare HTTP.")
    except requests.HTTPError:
        print("Pagina principala a raspuns cu o eroare HTTP.")
    time.sleep(1)
    missing = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    try:
        missing.raise_for_status()
        print("Serverul a returnat", missing.status_code, "pentru calea de test.")
    except requests.HTTPError:
        print("Pagina de test nu poate fi accesata. Cod:", missing.status_code)
    # Unele site-uri returneaza 200 chiar si pentru o pagina inexistenta.

    # Exercitiul 11 - Toate antetele
    print("Exercitiul 11")
    for name, value in response.headers.items():
        print(name + ": " + value)

    # Exercitiul 12 - Metode de dictionar
    print("Exercitiul 12")
    print(response.headers.get("Server", "lipseste"))
    print(response.headers.get("Content-Type", "lipseste"))
    print(response.headers.get("content-type", "lipseste"))
    # Numele antetelor HTTP nu tin cont de majuscule/minuscule.

    # Exercitiul 13 - Metode de sir
    print("Exercitiul 13:", response.text.lower().count("cyber"))
    # lower() returneaza tot un sir; pe acest sir putem apela count().

    # Exercitiul 14 - Titlul
    html = response.text
    start = html.lower().find("<title>")
    end = html.lower().find("</title>", start + len("<title>"))
    if start != -1 and end != -1:
        title = html[start + len("<title>"):end].strip()
    else:
        title = "Titlu negasit"
    print("Exercitiul 14:", title)

    # Exercitiul 15 - Linii
    lines = html.splitlines()
    longest = max(lines, key=len, default="")
    print("Exercitiul 15:", len(lines), "linii; cea mai lunga:", len(longest))

    # Exercitiul 16 - HTTPS
    if response.url.startswith("https://"):
        print("Conexiune securizata")
    else:
        print("Conexiune nesecurizata")
    # HTTPS protejeaza transportul; nu garanteaza ca site-ul este de incredere.

    # Exercitiul 17 - Redirectionari
    time.sleep(1)
    redirected = requests.get("http://cybercor.org", timeout=TIMEOUT)
    print("Exercitiul 17")
    for step in redirected.history:
        print(step.status_code, step.url)
    print("URL final:", redirected.url)

    # Exercitiul 18 - HEAD si GET
    time.sleep(1)
    head = requests.head(BASE_URL, timeout=TIMEOUT, allow_redirects=True)
    time.sleep(1)
    page = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Exercitiul 18 - HEAD:", len(head.content), "GET:", len(page.content))
    # HEAD cere antetele fara corp; GET primeste si corpul paginii.

    # Exercitiul 19 - Cookie-uri
    print("Exercitiul 19")
    if not response.cookies:
        print("Niciun cookie setat.")
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)

    # Exercitiul 20 - Sesiuni si antete personalizate pe httpbin
    time.sleep(1)
    with requests.Session() as session:
        session.headers.update({"User-Agent": "WebLab-Pavalchi-Veronica"})
        echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
        echo.raise_for_status()
        sent = echo.json()["headers"].get("User-Agent", "lipseste")
        print("Exercitiul 20 - Antet primit de server:", sent)
        print("Antet confirmat:", sent == "WebLab-Pavalchi-Veronica")
    # text este atribut; json() este metoda care interpreteaza corpul ca JSON.


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ValueError, KeyError) as error:
        print("Nu am putut termina exercitiile. Verifica raspunsul site-ului:", error)
