# Laborator: functii, metode si importuri pe web
# Student: Pavalchi Veronica

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import argparse
import csv
from datetime import datetime
from pathlib import Path
import requests
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS

# Exercitiul 45: o definitie ulterioara def get_title in acest fisier
# ar inlocui numele importat. webtools.get_title ar ramane accesibil.


# Exercitiul 49
def save_csv(url):
    """Salveaza codurile cailor in report.csv, langa script."""
    results = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    path = Path(__file__).with_name("report.csv")
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for page, status in results.items():
            writer.writerow([page, status if status is not None else "eroare_conexiune",
                             datetime.now().isoformat()])
    print("Salvat in", path.name)


def main():
    """Citeste adresa si ruleaza demonstratiile modulului si raportul final."""
    # Exercitiul 48
    parser = argparse.ArgumentParser(description="Laborator web - raport CYBERCOR")
    parser.add_argument("url", nargs="?", default=BASE_URL, help="https://cybercor.org")
    args = parser.parse_args()
    if args.url.rstrip("/") != BASE_URL:
        parser.error("Pentru acest laborator foloseste doar https://cybercor.org")
    url = args.url.rstrip("/")

    try:
        # Exercitiul 44 - importul intregului modul
        print("44:", webtools.get_title(webtools.fetch(url).text))
        # Exercitiul 45 - importarea anumitor nume
        print("45:", get_title(webtools.fetch(url).text))
        print(security_headers(url))
    except requests.RequestException as error:
        print("Demonstratia nu a putut accesa pagina:", error)

    # Exercitiul 47
    print("47 - DEFAULT_HEADERS:", DEFAULT_HEADERS)
    # Regula generala cere antete personalizate doar pe httpbin.org.
    # De aceea fetch foloseste DEFAULT_HEADERS numai pentru httpbin.
    try:
        echo = webtools.fetch(ECHO_URL + "/headers")
        echo.raise_for_status()
        received = echo.json()["headers"].get("User-Agent")
        print("User-Agent confirmat:", received == DEFAULT_HEADERS["User-Agent"])
    except (requests.RequestException, ValueError, KeyError) as error:
        print("Nu am putut confirma antetul:", error)
    save_csv(url)
    webtools.site_report(url)


if __name__ == "__main__":
    main()
