# A1: Încălzirea - Diferența dintre Text (str) și Octeți (bytes)
s = "salut"
b = s.encode()  # Convertim șirul în octeți (bytes)

print(b)                    # Afișează b"salut"
print(b[0])                 # Afișează valoarea numerică a primului octet (115 pentru 's')
print(b.hex())              # Afișează reprezentarea hexazecimală a octeților
print(bytes.fromhex(b.hex())) # Reface octeții înapoi din hexazecimal

import re

# A2: Recunoașterea stratului după formă (Ghicirea codării)
def ghici_strat(s):
    # Verificăm întâi formatul URL (%xx) - cel mai specific
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    # Verificăm dacă este Hex pur (caractere 0-9, a-f și lungime pară)
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"

    # Verificăm dacă este Base64 (alfabet standard, lungime multiplu de 4 cu padding '=')
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s) and len(s) % 4 == 0:
        return "base64"

    return "necunoscut"

# Teste pentru funcția de ghicire
print(ghici_strat("%2Fetc"))          # -> url
print(ghici_strat("48656c6c6f"))     # -> hex
print(ghici_strat("U2FsdXQ="))       # -> base64

import base64
from urllib.parse import unquote

# A3: Desfacerea stratului recunoscut
# aplicăm funcția inversă corespunzătoare pentru a decoda șirul în octeți.
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode()
    else:
        rezultat = s.encode()

    return strat, rezultat

print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%2Fetc"))

# A4: Straturi multiple într-o buclă (Citirea din 'mesaj.txt')
# (de ex. Base64 peste Hex). Facem o buclă de până la 8 pași care decodifică iterativ până la textul clar.
with open("mesaj.txt") as fisier:
    mesaj = fisier.read().strip()

for i in range(8):
    strat, rezultat = desfa(mesaj)

    if strat == "necunoscut":
        break  # Oprim bucla dacă nu mai recunoaște nicio codare

    mesaj = rezultat.decode()
    print(strat, mesaj)

print("Mesaj final:", mesaj)

# A5: Spargerea unui XOR cu cheie de un octet ('xor.bin')
# Testăm toate cheile prin operatorul XOR (^), căutând markerul standard 'FLAG{' în textul rezultat.
with open("xor.bin", "rb") as fisier:
    date = fisier.read()

for cheie in range(256):
    clar = bytes(b ^ cheie for b in date)

    if b"FLAG{" in clar:
        print("Cheie gasita:", cheie)
        print("Mesaj decriptat:", clar.decode())
        break

import hashlib

# A6: Spargerea unui hash prin dicționar ('hashuri.txt' + 'wordlist.txt')
# sau dicționar: hashuim fiecare cuvânt din wordlist și comparăm rezultatul cu hashul țintă.
with open("hashuri.txt") as fisier:
    tinta = fisier.readline().strip()

print("Lungimea hashului:", len(tinta)) # 32 caractere indică algoritmul MD5

with open("wordlist.txt") as fisier:
    for parola in fisier:
        parola = parola.strip()
        calculat = hashlib.md5(parola.encode()).hexdigest()

        if calculat == tinta:
            print("Parola gasita:", parola)
            break

import argparse
import json

# A7: Argumente în linie de comandă (CLI), salvare în JSON și Test Unitar
# primind un șir sau un fișier, salvăm rezultatul într-o fișă JSON structurată și testăm validitatea cu assert.
p = argparse.ArgumentParser()
p.add_argument("intrare")
p.add_argument("--fisier", action="store_true")
a = p.parse_args()

if a.fisier:
    with open(a.intrare, "rb") as fisier:
        mesaj = fisier.read().decode().strip()
else:
    mesaj = a.intrare

strat, rezultat = desfa(mesaj)

# Salvăm rezultatul într-o fișă JSON oficială
fisa = {
    "strat": strat,
    "rezultat": rezultat.decode()
}

with open("fisa.json", "w", encoding="utf-8") as fisier:
    json.dump(fisa, fisier, indent=4, ensure_ascii=False)

print("Rezultatul a fost salvat in fisa.json")

# Test unitar pentru verificarea corectitudinii funcției de Base64
def test_base64():
    strat, rezultat = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert rezultat == b"Salut"

test_base64()
print("Testul Base64 a trecut!")
