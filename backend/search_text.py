import re
import faiss
import pickle
import numpy as np
from urllib.parse import quote
from sentence_transformers import SentenceTransformer
from cards_downloader import limpiar_nombre

# --- Preprocesamiento de texto ---
def preprocesar_texto(texto):
    texto = texto.lower()                         # Convertir a minúsculas
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)  # Eliminar signos de puntuación
    texto = re.sub(r'\s+', ' ', texto).strip()    # Eliminar espacios múltiples
    return texto

# --- Cargar nombres y descripciones ---
with open("faiss_names.pkl", "rb") as f:
    NOMBRES = pickle.load(f)
with open("faiss_descriptions.pkl", "rb") as f:
    DESCRIPCIONES = pickle.load(f)

# --- Preprocesar descripciones ---
DESCRIPCIONES_LIMPIAS = [preprocesar_texto(desc) for desc in DESCRIPCIONES]

# --- Cargar modelo y vectorizar descripciones ---
modelo = SentenceTransformer("all-MiniLM-L6-v2")
X = modelo.encode(DESCRIPCIONES_LIMPIAS, convert_to_numpy=True).astype("float32")

# --- Crear índice FAISS ---
index_faiss = faiss.IndexFlatL2(X.shape[1])
index_faiss.add(X)

def buscar_por_descripcion(query, top_k=5):
    query_limpio = preprocesar_texto(query)

    # Buscar por nombre exacto
    resultado_nombre = buscar_por_nombre(query_limpio)
    if resultado_nombre:
        similares = buscar_similares_por_nombre(query_limpio, top_k=top_k - 1)
        return [resultado_nombre] + similares

    # Buscar por descripción semántica
    vector_query = modelo.encode([query_limpio], convert_to_numpy=True).astype("float32")
    _, indices = index_faiss.search(vector_query, top_k)

    resultados = []
    for i in indices[0]:
        if i < 0:
            continue
        nombre = NOMBRES[i]
        nombre_archivo = limpiar_nombre(nombre) + ".jpg"
        resultados.append({
            "name": nombre,
            "desc": DESCRIPCIONES[i],
            "image_url": f"/data/cartas/{quote(nombre_archivo)}"
        })
    return resultados

def buscar_por_nombre(nombre):
    nombre_limpio = preprocesar_texto(nombre)
    for i, n in enumerate(NOMBRES):
        if preprocesar_texto(n) == nombre_limpio:
            nombre_archivo = limpiar_nombre(NOMBRES[i]) + ".jpg"
            return {
                "name": NOMBRES[i],
                "desc": DESCRIPCIONES[i],
                "image_url": f"/data/cartas/{quote(nombre_archivo)}"
            }
    return None

def buscar_similares_por_nombre(nombre, top_k=4):
    for i, n in enumerate(NOMBRES):
        if preprocesar_texto(n) == preprocesar_texto(nombre):
            idx = i
            break
    else:
        return []

    vector_query = modelo.encode([preprocesar_texto(DESCRIPCIONES[idx])], convert_to_numpy=True).astype("float32")
    _, indices = index_faiss.search(vector_query, top_k + 1)

    similares = []
    for i in indices[0]:
        if i >= 0 and i != idx:
            nombre_similar = NOMBRES[i]
            nombre_archivo = limpiar_nombre(nombre_similar) + ".jpg"
            similares.append({
                "name": nombre_similar,
                "desc": DESCRIPCIONES[i],
                "image_url": f"/data/cartas/{quote(nombre_archivo)}"
            })
    return similares
