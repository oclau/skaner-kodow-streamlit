import cv2
from pyzbar.pyzbar import decode
import datetime
import csv
import requests
from bs4 import BeautifulSoup


# Nazwa pliku ze zdjęciem kodu
# nazwa_pliku = "mus_owocowy.jpg"
# nazwa_pliku = "lek.jpg"
# nazwa_pliku = "pigwoniada.jpg"
# nazwa_pliku = "woda_jablkowa.jpg"


import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime

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

st.set_page_config(page_title="Skaner kodów", layout="centered")
st.title("Skaner kodów kreskowych z rozpoznawaniem produktu")

uploaded_file = st.file_uploader("Wgraj zdjęcie z kodem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    st.image(image_rgb, caption="Oryginalne zdjęcie", use_container_width=True, channels="RGB")

    znalezione_kody = decode(image_bgr)  # <- ważne: uzyc BGR do rozpoznania

    if znalezione_kody:
        for barcode in znalezione_kody:
            data = barcode.data.decode("utf-8")
            nazwa = wyszukaj_nazwe_produktu(data)
            st.success(f"Odczytano: {data}")
            st.info(f"Nazwa produktu: {nazwa}")
            st.write(f" [Szukaj więcej](https://www.google.com/search?q={data})")

    else:
        st.warning("Nie wykryto żadnego kodu.")
