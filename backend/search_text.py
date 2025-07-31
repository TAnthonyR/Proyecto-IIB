import faiss
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import quote

# --- Cargar nombres y descripciones ---
with open("faiss_names.pkl", "rb") as f:
    NOMBRES = pickle.load(f)
with open("faiss_descriptions.pkl", "rb") as f:
    DESCRIPCIONES = pickle.load(f)

# --- Vectorizador y FAISS index ---
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(DESCRIPCIONES).toarray().astype("float32")
index_faiss = faiss.IndexFlatL2(X.shape[1])
index_faiss.add(X)

def buscar_por_descripcion(query, top_k=5):
    vector_query = vectorizer.transform([query]).toarray().astype("float32")
    _, indices = index_faiss.search(vector_query, top_k)
    resultados = []
    for i in indices[0]:
        nombre = NOMBRES[i]
        nombre_archivo = nombre + ".jpg"
        resultados.append({
            "name": nombre,
            "desc": DESCRIPCIONES[i],
            "image_url": f"/data/cartas/{nombre_archivo.replace(' ', '%20')}"
        })
    return resultados

from urllib.parse import quote

def buscar_por_nombre(nombre):
    for i, n in enumerate(NOMBRES):
        if n.lower() == nombre.lower():
            nombre_archivo = f"{nombre}.jpg"
            ruta_imagen = f"/data/cartas/{quote(nombre_archivo)}"
            return {
                "name": NOMBRES[i],
                "desc": DESCRIPCIONES[i],
                "image_url": ruta_imagen
            }
    return None



def buscar_similares_por_nombre(nombre, top_k=4):
    if nombre not in NOMBRES:
        return []

    idx = NOMBRES.index(nombre)
    vector_query = vectorizer.transform([DESCRIPCIONES[idx]]).toarray().astype("float32")
    _, indices = index_faiss.search(vector_query, top_k + 1)

    similares = []
    for i in indices[0]:
        if i != idx:
            nombre_similar = NOMBRES[i]
            nombre_archivo = f"{nombre_similar}.jpg"
            ruta_imagen = f"/data/cartas/{quote(nombre_archivo)}"
            similares.append({
                "name": nombre_similar,
                "desc": DESCRIPCIONES[i],
                "image_url": ruta_imagen
            })
    return similares
