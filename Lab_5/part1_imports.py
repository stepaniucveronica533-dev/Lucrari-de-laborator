# Laborator: functii, metode si importuri pe web
# Student: Pavalchi Veronica

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import urllib.request
import time


def main():
    """Demonstreaza exercitiile 1-8."""
    # Exercitiul 1 - Primul import
    print("Exercitiul 1:", requests.__version__)
    # requests este externa: o instalam cu pip install requests.
    # urllib este inclusa in Python si nu necesita instalare separata.

    # Exercitiul 2 - Doua stiluri de import
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Exercitiul 2:", response.status_code)
    from requests import get
    time.sleep(1)
    response = get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
    # import requests arata clar biblioteca din care vine get.
    # from requests import get permite apeluri mai scurte.

    # Exercitiul 3 - Alias-uri
    import requests as rq
    time.sleep(1)
    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print("Exercitiul 3:", response.status_code)
    # Alias-ul scurteaza un nume lung; o prescurtare neclara ingreuneaza citirea.

    # Exercitiul 4 - Biblioteca standard
    time.sleep(1)
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
        print("Exercitiul 4:", response.status)
        html = response.read().decode("utf-8", errors="replace")
        print(html[:200])

    # Exercitiul 5 - Continutul unui modul
    print("Exercitiul 5:", dir(requests))
    # get este functie; Session este clasa; exceptions este modul.

    # Exercitiul 6 - Documentatie
    help(requests.get)
    # timeout se transmite prin **kwargs; documentatia get poate sa nu-l enumere.
    # help(requests.request) ofera detaliile parametrilor acceptati.
    help(requests.request)
    time.sleep(1)
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Exercitiul 6:", response.status_code)

    # Exercitiul 7 - Cronometrare
    time.sleep(1)
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    duration = time.perf_counter() - start
    print("Exercitiul 7 - Durata totala:", duration)
    print("Pana la antetele raspunsului final:", response.elapsed.total_seconds())
    # perf_counter include si citirea corpului si eventualele redirectionari.
    # elapsed masoara raspunsul respectiv pana la primirea antetelor.

    # Exercitiul 8 - Import care poate lipsi
    try:
        import bs4
        print("Exercitiul 8: bs4 este instalat.")
    except ImportError:
        print("Instalati modulul cu: pip install beautifulsoup4")
    # Modul: unitate de cod importabila, adesea un fisier .py.
    # Pachet: grupeaza module. Biblioteca: colectie de instrumente reutilizabile.


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, OSError) as error:
        print("Nu am putut termina cererile. Verifica internetul:", error)
