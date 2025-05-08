import pyautogui
import pytesseract
import time
import cv2
import re
from PIL import Image
import keyboard
import numpy as np
import requests
import winsound

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

def invia_screenshot_telegram(percorso_file):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(percorso_file, "rb") as photo:
        data = {"chat_id": CHAT_ID}
        files = {"photo": photo}
        try:
            requests.post(url, data=data, files=files)
        except Exception as e:
            print("Errore nell'invio dello screenshot:", e)


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

print("Bot avviato. Premi ESC per interrompere.")

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

    return risultato

ultimo_numero_str = None
riparti_da_zero = True
stesso_numero_count = 0  # contatore attese su numero identico

while True:
    if keyboard.is_pressed("esc"):
        print("❌ Uscita manuale.")
        break

    if riparti_da_zero:
        print("▶️ Inizio nuovo ciclo. Avvio click iniziali...")

        screenshot_path = "screenshot_ciclo.png"
        pyautogui.screenshot(screenshot_path)
        invia_screenshot_telegram(screenshot_path)

        pyautogui.click(105, 963)
        time.sleep(8)
        pyautogui.click(1382, 665)
        time.sleep(8)
        riparti_da_zero = False


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
    nuovo_numero_str = None

    for riga in righe:
        matches = re.findall(r"\d[\d\s.]*", riga)
        for match in matches:
            numero_str = match.replace(" ", "").replace(".", "").replace(",", "")
            if numero_str and len(numero_str) >= 5:
                try:
                    numero = int(numero_str)
                    print(f"Numero trovato: {numero}")
                    numeri_valutati += 1
                    nuovo_numero_str = numero_str
                    if 1300000 < numero < 2500000:
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
        #invia_notifica_telegram(f"🎯 Numero valido trovato: {numero}")
        pyautogui.moveTo(306, 420)

        keyboard.press('1')
        time.sleep(0.1)
        keyboard.release('1')
        for _ in range(10):
            pyautogui.click()
            time.sleep(0.1)

        keyboard.press('3')
        time.sleep(0.1)
        keyboard.release('3')
        for _ in range(9):
            pyautogui.click()
            time.sleep(0.1)

        for tasto in ['q', 'w', 'e', 'r']:
            keyboard.press(tasto)
            time.sleep(0.1)
            keyboard.release(tasto)
            pyautogui.click()
            time.sleep(0.1)

        keyboard.press('r')
        time.sleep(0.1)
        keyboard.release('r')
        keyboard.press('5')
        time.sleep(0.1)
        keyboard.release('5')
        pyautogui.click()
        pyautogui.click()
        keyboard.press('z')
        time.sleep(0.1)
        keyboard.release('z')
        pyautogui.click()
        keyboard.press('2')
        time.sleep(0.1)
        keyboard.release('2')
        pyautogui.click()
        keyboard.press('4')
        time.sleep(0.1)
        keyboard.release('4')
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(700, 476)
        keyboard.press('S')
        time.sleep(0.1)
        keyboard.press('e')
        time.sleep(0.1)
        keyboard.release('e')
        keyboard.release('S')
        pyautogui.click()
        time.sleep(4)
        pyautogui.moveTo(948, 486)
        keyboard.press('S')
        time.sleep(0.1)
        keyboard.release('S')
        pyautogui.click()

        print("⏳ In attesa che lo schermo si scurisca...")

        def is_schermo_scuro():
            screenshot = pyautogui.screenshot()
            larghezza, altezza = screenshot.size
            fascia_altezza = 10  # numero di righe dal basso da controllare
            pixel_neri = 0
            pixel_totali = 0

            for y in range(altezza - fascia_altezza, altezza):
                for x in range(0, larghezza, 10):  # ogni 10 pixel in orizzontale per velocità
                    r, g, b = screenshot.getpixel((x, y))
                    pixel_totali += 1
                    if (r, g, b) == (0, 0, 0):
                        pixel_neri += 1

            percentuale_nera = (pixel_neri / pixel_totali) * 100
            print(f"🧪 Fascia nera: {pixel_neri}/{pixel_totali} pixel neri ({percentuale_nera:.0f}%)")

            return percentuale_nera >= 75  # soglia regolabile




        while True:
            if is_schermo_scuro():
                print("🌑 Schermo scuro rilevato!")
                break
            else:
                pixel = pyautogui.screenshot().getpixel((60, 700))
                print(f"🟢 Schermo chiaro, colore pixel: {pixel}")
            time.sleep(0.5)


        # Click su "Torna al villaggio"
        pyautogui.click(959, 919)
        print("✅ Torna al villaggio cliccato.")
        riparti_da_zero = True
        time.sleep(7)

        # Ricomincia ciclo senza uscire
        continue    
    else:
        if nuovo_numero_str != ultimo_numero_str:
            print("🔁 Numero cambiato. Click su (1800, 800) e riprovo...")
            pyautogui.click(1800, 800)
            ultimo_numero_str = nuovo_numero_str
            stesso_numero_count = 0  # reset contatore
        else:
            stesso_numero_count += 1
            print(f"⏳ Numero uguale al precedente. Attendo... ({stesso_numero_count})")

            if stesso_numero_count >= 10:
                print("⚠️ Forzatura: stesso numero rilevato troppe volte. Click forzato.")
                pyautogui.click(1800, 800)
                stesso_numero_count = 0  # reset

        time.sleep(1)


#1463 64