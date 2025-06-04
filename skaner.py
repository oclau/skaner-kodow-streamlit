import cv2
from pyzbar.pyzbar import decode
import datetime
import csv
import requests
from bs4 import BeautifulSoup

# Przykładowe zdjęcia
# Nazwa pliku ze zdjęciem kodu
# nazwa_pliku = "mus_owocowy.jpg"
# nazwa_pliku = "lek.jpg"
# nazwa_pliku = "pigwoniada.jpg"
nazwa_pliku = "woda_jablkowa.jpg"



# Funkcja do wyszukiwania produktu przez DuckDuckGo
def wyszukaj_nazwe_produktu(kod):
    url = f"https://duckduckgo.com/html/?q={kod}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        wynik = soup.find("a", {"class": "result__a"})
        return wynik.text.strip() if wynik else "Nie znaleziono produktu"
    except Exception as e:
        return f"Problem z wyszukiwaniem ({e})"



# Wczytaj obrazek
frame = cv2.imread(nazwa_pliku)
if frame is None:
    print(f"Nie udało się wczytać pliku '{nazwa_pliku}'")
    exit(1)


# Zmniejsz obraz do szerokości 800 pikseli (z zachowaniem proporcji)
szerokosc_docelowa = 800
wysokosc_docelowa = int(frame.shape[0] * (szerokosc_docelowa / frame.shape[1]))
frame = cv2.resize(frame, (szerokosc_docelowa, wysokosc_docelowa))

# Wykryj kody 
znalezione_kody = decode(frame)

# Utwórz / dopisz do pliku log.csv
with open("log_z_pliku.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["czas", "kod", "nazwa_produktu"])

    if znalezione_kody:
        for barcode in znalezione_kody:
            data = barcode.data.decode("utf-8")
            rect = barcode.rect

            # Wyszukaj nazwę produktu
            nazwa = wyszukaj_nazwe_produktu(data)

            # Wypisz i zapisz
            teraz = datetime.datetime.now()
            print(f"[{teraz}] Odczytano: {data} → {nazwa}")
            writer.writerow([teraz, data, nazwa])

            # Rysuj ramkę
            cv2.rectangle(
                frame,
                (rect.left, rect.top),
                (rect.left + rect.width, rect.top + rect.height),
                (0, 255, 0),
                2
            )

            # Tekst nad kodem
            cv2.putText(
                frame,
                data,
                (rect.left, rect.top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    else:
        print("Nie wykryto żadnego kodu na tym obrazie.")

# Pokaż obrazek z ramkami
cv2.imshow("Wynik odczytu z pliku", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
