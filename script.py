import pyautogui
import pytesseract
import time
import cv2
import winsound
import re
from PIL import Image
import keyboard
import numpy as np
import requests

# === CONFIGURAZIONE TELEGRAM ===
TELEGRAM_BOT_TOKEN = "7694482372:AAHlt3rqhZ_3DAqTQGvQpm3d37dlLGbcR00"
CHAT_ID = "1407605362"

def invia_notifica_telegram(messaggio):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": messaggio}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Errore nell'invio della notifica:", e)

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

print("Bot avviato. Premi ESC per interrompere.")

pyautogui.click(105, 963)
time.sleep(8)
pyautogui.click(1382, 665)
time.sleep(8)

colori_target = [
    (224, 220, 179),
    (224, 204, 222)
]
tolleranza = 25

def correggi_ocr(testo):
    testo = testo.replace("O", "0").replace("o", "0")
    testo = testo.replace("I", "1").replace("l", "1")
    return testo

def filtra_per_colore(img, colori, tolleranza=10):
    mask_totale = np.zeros(img.shape[:2], dtype=np.uint8)
    for colore in colori:
        min_col = np.array([max(c - tolleranza, 0) for c in colore], dtype=np.uint8)
        max_col = np.array([min(c + tolleranza, 255) for c in colore], dtype=np.uint8)
        mask = cv2.inRange(img, min_col, max_col)
        mask_totale = cv2.bitwise_or(mask_totale, mask)

    debug_vis = cv2.cvtColor(mask_totale, cv2.COLOR_GRAY2BGR)
    debug_vis[mask_totale > 0] = (0, 0, 255)

    risultato = np.full_like(img, 255)
    risultato[mask_totale > 0] = (0, 0, 0)

    kernel = np.ones((2, 2), np.uint8)
    risultato = cv2.dilate(risultato, kernel, iterations=1)

    cv2.imwrite("debug_maschera.png", mask_totale)
    cv2.imwrite("debug_output.png", risultato)
    cv2.imwrite("debug_colore_rosso.png", debug_vis)

    return risultato

while True:
    if keyboard.is_pressed("esc"):
        print("❌ Uscita manuale.")
        break

    screenshot = pyautogui.screenshot(region=(77, 120, 200, 100))
    screenshot.save("alto_sinistra.png")

    img_check = cv2.imread("alto_sinistra.png")
    b, g, r = img_check[25, 60]
    print(f"Colore pixel (60,25): RGB = ({r}, {g}, {b})")

    img_orig = cv2.imread("alto_sinistra.png")
    img = filtra_per_colore(img_orig, colori_target, tolleranza)
    testo = pytesseract.image_to_string(img, config='--psm 6')
    testo = correggi_ocr(testo)
    print("Testo OCR corretto:", testo)

    with open("ocr_log.txt", "a", encoding="utf-8") as f:
        f.write(f"OCR: {testo}\n")

    righe = testo.splitlines()
    buono = False
    numeri_valutati = 0

    for riga in righe:
        matches = re.findall(r"\d[\d\s.]*", riga)
        for match in matches:
            numero_str = match.replace(" ", "").replace(".", "").replace(",", "")
            if numero_str and len(numero_str) >= 5:
                try:
                    numero = int(numero_str)
                    print(f"Numero trovato: {numero}")
                    numeri_valutati += 1
                    if 1600000 < numero < 2500000:
                        buono = True
                        break
                    if numeri_valutati >= 2:
                        break
                except ValueError:
                    continue
        if buono or numeri_valutati >= 2:
            break

    if buono:
        print("🎉 Numero valido trovato! ciao!!!")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        invia_notifica_telegram(f"🎯 Numero valido trovato: {numero}")
        break
    else:
        print("🔁 Nessun numero valido. Click su (1800, 800) e riprovo...")
        pyautogui.click(1800, 800)
        time.sleep(8)
