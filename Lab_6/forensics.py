import re
from PIL import Image
from PIL.ExifTags import TAGS
import zipfile
import io


# B1: Magic bytes (Detectarea tipului real al fișierului)
# Verificăm primii octeți din antetul fișierului deschis în binar pentru a afla tipul lui real, indiferent de extensie.
def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


print("Tip real foto.jpg:", tip_real("foto.jpg"))


# B2: Strings (Extragerea textului citibil dintr-un binar)
# Folosim o expresie regulată pe octeți pentru a extrage toate secvențele de text vizibile ascunse în interiorul unui fișier binar.
with open("ascuns.png", "rb") as f:
    date_binare = f.read()

print("--- Text extras din ascuns.png (Strings) ---")
for m in re.findall(rb"[ -~]{4,}", date_binare):
    print(m.decode(errors="ignore"))

# ---------------------------------------------------------
# B3: Metadate EXIF și GPS din poză
# ---------------------------------------------------------
# Deschidem imaginea cu biblioteca PIL și extragem dicționarul EXIF pentru a afla date despre cameră, data fotografierii și coordonatele GPS.
img = Image.open("foto.jpg")
exif_data = img._getexif()

if exif_data:
    print("--- Metadate EXIF & GPS ---")
    for tag_id, val in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo":
            print(f"Coordonate GPS (Tag 34853): {val}")
        else:
            print(f"{tag}: {val}")

# ---------------------------------------------------------
# B4: File carving (Extragerea arhivei ZIP ascunse)
# ---------------------------------------------------------
# Căutăm semnătura unei arhive ZIP (PK\x03\x04) care a fost lipită ascuns la coada imaginii, o decupăm de acolo și o salvăm separat.
with open("ascuns.png", "rb") as f:
    continut = f.read()

i = continut.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", "wb") as f_out:
        f_out.write(continut[i:])
    print(f"Arhivă ZIP extrasă cu succes de la octetul {i} în 'gasit.zip'!")

# B5: Ascunderea unui mesaj prin LSB (Least Significant Bit)
# Transformăm mesajul în biți și îi ascundem în ultimul bit al culorilor pixelilor, salvând poza în format PNG.
img_stego = Image.open("foto.jpg").convert("RGB")
px = list(img_stego.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}\x00"  # Mesajul de ascuns
biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
bit_idx = 0
for p in px:
    r, g, b = p
    if bit_idx < len(biti):
        r = (r & ~1) | int(biti[bit_idx]);
        bit_idx += 1
    if bit_idx < len(biti):
        g = (g & ~1) | int(biti[bit_idx]);
        bit_idx += 1
    if bit_idx < len(biti):
        b = (b & ~1) | int(biti[bit_idx]);
        bit_idx += 1
    px_nou.append((r, g, b))
else:
    px_nou.extend(px[len(px_nou):])

img_stego.putdata(px_nou)
img_stego.save("stego.png")
print("Mesaj ascuns și salvat în 'stego.png'!")

# B6: Dezvăluirea mesajului LSB din stego.png
# Citim ultimul bit din fiecare pixel al imaginii modificate, îi grupăm câte 8 înapoi în octeți și reconstituim textul ascuns.
img_citire = Image.open("stego.png").convert("RGB")
px_cititi = list(img_citire.getdata())

biti_extras = ""
for (r, g, b) in px_cititi:
    biti_extras += str(r & 1)
    biti_extras += str(g & 1)
    biti_extras += str(b & 1)

octeti = bytearray()
for b_index in range(0, len(biti_extras), 8):
    octet_str = biti_extras[b_index:b_index + 8]
    if len(octet_str) < 8:
        break
    valoare = int(octet_str, 2)
    if valoare == 0:  # Sfârșitul mesajului
        break
    octeti.append(valoare)

print("Mesaj dezvăluit din LSB:", octeti.decode(errors="ignore"))