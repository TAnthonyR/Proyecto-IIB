"""Prepara índices alineando imágenes, nombres y descripciones."""
import json
import pickle
from pathlib import Path
import numpy as np
import faiss
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

BASE = Path(__file__).resolve().parent

def main():
    metadata = BASE / 'data/cards.json'
    if not metadata.exists():
        raise SystemExit('Primero ejecuta python backend/cards_downloader.py --limit 100')
    cards = json.loads(metadata.read_text(encoding='utf-8'))
    model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32').eval()
    processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
    names, descriptions, vectors = [], [], []
    for card in cards:
        try:
            with Image.open(BASE / 'data/cartas' / card['filename']) as image:
                inputs = processor(images=image.convert('RGB'), return_tensors='pt')
                with torch.no_grad():
                    vector = model.get_image_features(**inputs).cpu().numpy()[0]
            vectors.append(vector)
            names.append(card['name'])
            descriptions.append(card['desc'])
        except (OSError, ValueError) as error:
            print(f"Imagen excluida: {card['name']} ({type(error).__name__})")
    if not vectors:
        raise SystemExit('No hay imágenes válidas para crear el índice.')
    matrix = np.asarray(vectors, dtype='float32')
    index = faiss.IndexFlatL2(matrix.shape[1])
    index.add(matrix)
    faiss.write_index(index, str(BASE / 'faiss_clip.index'))
    for name, values in [('faiss_names.pkl', names), ('faiss_nombres.pkl', names), ('faiss_descriptions.pkl', descriptions)]:
        with (BASE / name).open('wb') as handle:
            pickle.dump(values, handle)
    print(f'Índice visual y metadatos de {len(names)} cartas preparados. El índice semántico se crea al iniciar la API.')

if __name__ == '__main__':
    main()
