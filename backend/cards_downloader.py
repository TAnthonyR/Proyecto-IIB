"""Descarga una muestra y conserva las descripciones reales de YGOPRODeck."""
import argparse
import json
from pathlib import Path
import re
import time
import requests

URL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
DATA_DIR = Path(__file__).resolve().parent / 'data'

def limpiar_nombre(nombre):
    return re.sub(r'[\\/*?:"<>|]', '', nombre)

def descargar_cartas(limit=100):
    if limit < 1:
        raise ValueError('El límite debe ser positivo')
    DATA_DIR.mkdir(exist_ok=True)
    images = DATA_DIR / 'cartas'
    images.mkdir(exist_ok=True)
    cache = DATA_DIR / 'catalogo.json'
    with requests.Session() as session:
        if cache.exists():
            cards = json.loads(cache.read_text(encoding='utf-8'))
        else:
            response = session.get(URL, timeout=60)
            response.raise_for_status()
            cards = response.json()['data']
            cache.write_text(json.dumps(cards, ensure_ascii=False), encoding='utf-8')
        selected = []
        for card in sorted(cards, key=lambda item: item['id'])[:limit]:
            if not card.get('card_images'):
                continue
            filename = limpiar_nombre(card['name']) + '.jpg'
            path = images / filename
            try:
                if not path.exists():
                    response = session.get(card['card_images'][0]['image_url'], timeout=30)
                    response.raise_for_status()
                    path.write_bytes(response.content)
                    time.sleep(0.2)
                selected.append({'name': card['name'], 'desc': card.get('desc', ''), 'filename': filename})
                print(f"Preparada: {card['name']}")
            except requests.RequestException:
                print(f"No se pudo descargar: {card['name']}; se excluye de la muestra.")
        if not selected:
            raise SystemExit('No se descargó ninguna carta. Comprueba Internet y vuelve a intentar.')
        (DATA_DIR / 'cards.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{len(selected)} cartas listas. Ejecuta backend/build_all_faiss_indexes.py.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=100)
    descargar_cartas(parser.parse_args().limit)
