import os
import requests
import re

URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
DATA_DIR = "backend/data/cartas"
os.makedirs(DATA_DIR, exist_ok=True)

def limpiar_nombre(nombre):
    return re.sub(r'[\\/*?:"<>|]', "", nombre)

def descargar_cartas():
    response = requests.get(URL)
    cartas = response.json()["data"]

    for carta in cartas:
        nombre = limpiar_nombre(carta["name"])
        if "card_images" in carta:
            url_imagen = carta["card_images"][0]["image_url"]
            ruta = os.path.join(DATA_DIR, f"{nombre}.jpg")

            try:
                img_data = requests.get(url_imagen).content
                with open(ruta, 'wb') as handler:
                    handler.write(img_data)
                print(f"[✓] {nombre}")
            except Exception as e:
                print(f"[!] Error con {nombre}: {e}")

if __name__ == "__main__":
    descargar_cartas()
