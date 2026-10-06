"""API local con búsqueda independiente de una clave de Gemini."""
import os
import pickle
from pathlib import Path
import tempfile
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError

BASE = Path(__file__).resolve().parent
os.chdir(BASE)
required = ['faiss_names.pkl', 'faiss_descriptions.pkl', 'faiss_clip.index', 'faiss_nombres.pkl']
if any(not (BASE / name).exists() for name in required):
    raise SystemExit('Faltan índices. Ejecuta cards_downloader.py y build_all_faiss_indexes.py según README.md.')
from search_text import buscar_por_descripcion
from search_image_clip import buscar_similares_por_imagen_clip

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500'])
with (BASE / 'faiss_names.pkl').open('rb') as handle:
    NOMBRES = pickle.load(handle)
with (BASE / 'faiss_descriptions.pkl').open('rb') as handle:
    DESCRIPCIONES = pickle.load(handle)

@app.get('/data/cartas/<path:filename>')
def serve_image(filename):
    return send_from_directory(BASE / 'data/cartas', filename)

@app.post('/api/buscar')
def buscar_texto():
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or not isinstance(body.get('nombre'), str):
        return jsonify(error='Envía un nombre o descripción de texto.'), 400
    text = body['nombre'].strip()
    if not text:
        return jsonify(error='Escribe una consulta.'), 400
    results = buscar_por_descripcion(text)
    if not results:
        return jsonify(error='No se encontraron coincidencias.'), 404
    return jsonify(carta=results[0], similares=results[1:])

@app.get('/api/descripcion/<nombre>')
def obtener_descripcion(nombre):
    for name, description in zip(NOMBRES, DESCRIPCIONES):
        if name.lower() != nombre.lower():
            continue
        key, model = os.getenv('GOOGLE_API_KEY'), os.getenv('GEMINI_MODEL')
        if key and model:
            try:
                response = requests.post(
                    f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                    headers={'x-goog-api-key': key},
                    json={'contents': [{'parts': [{'text': 'Resume esta descripción de una carta de Yu-Gi-Oh! en español:\n' + description}]}]},
                    timeout=30)
                response.raise_for_status()
                parts = response.json()['candidates'][0]['content']['parts']
                summary = ''.join(part.get('text', '') for part in parts).strip()
                if summary:
                    return jsonify(descripcion=summary)
            except (requests.RequestException, KeyError, IndexError, ValueError):
                pass
        return jsonify(descripcion=description)
    return jsonify(descripcion='Descripción no encontrada.'), 404

@app.post('/api/similar')
def buscar_imagen():
    image = request.files.get('image')
    if image is None or not image.filename:
        return jsonify(error='Selecciona una imagen.'), 400
    fd, name = tempfile.mkstemp(suffix='.jpg')
    os.close(fd)
    try:
        image.save(name)
        with Image.open(name) as uploaded:
            uploaded.verify()
        return jsonify(buscar_similares_por_imagen_clip(name))
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        return jsonify(error='El archivo no es una imagen válida.'), 400
    finally:
        Path(name).unlink(missing_ok=True)

if __name__ == '__main__':
    print('Servidor local: http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=False)
