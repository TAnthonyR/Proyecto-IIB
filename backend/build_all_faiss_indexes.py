import os
import re
import pickle
import numpy as np
import faiss
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import CLIPProcessor, CLIPModel

# --- Paths base ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARTAS_DIR = os.path.join(BASE_DIR, "data", "cartas")

# --- Cargar modelo CLIP ---
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# --- Función: vectorizar imagen con CLIP ---
def vectorizar_imagen_clip(path):
    image = Image.open(path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt", padding=True)
    outputs = clip_model.get_image_features(**inputs)
    return outputs.detach().numpy()[0]

# --- Inicializar variables ---
nombres = []
descripciones = []
vectores_clip = []

# --- Leer cartas (simulando archivo JSON de API local) ---
for archivo in os.listdir(CARTAS_DIR):
    if archivo.endswith(".jpg"):
        nombre = archivo.replace(".jpg", "")
        descripcion_simulada = f"Descripción ficticia de {nombre} para pruebas."

        nombres.append(nombre)
        descripciones.append(descripcion_simulada)

        try:
            ruta = os.path.join(CARTAS_DIR, archivo)
            vector_clip = vectorizar_imagen_clip(ruta)
            vectores_clip.append(vector_clip)
            print(f"[✓] Procesada imagen: {nombre}")
        except Exception as e:
            print(f"[✗] Error con {archivo}: {e}")

# --- Guardar nombres y descripciones ---
with open(os.path.join(BASE_DIR, "faiss_names.pkl"), "wb") as f:
    pickle.dump(nombres, f)
with open(os.path.join(BASE_DIR, "faiss_descriptions.pkl"), "wb") as f:
    pickle.dump(descripciones, f)

# --- Índice TF-IDF (texto) ---
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(descripciones).toarray().astype("float32")
index_texto = faiss.IndexFlatL2(X.shape[1])
index_texto.add(X)
faiss.write_index(index_texto, os.path.join(BASE_DIR, "faiss_index.index"))
print("[✓] Índice TF-IDF guardado")

# --- Índice CLIP (imagen) ---
vectores_clip = np.array(vectores_clip).astype("float32")
index_clip = faiss.IndexFlatL2(vectores_clip.shape[1])
index_clip.add(vectores_clip)
faiss.write_index(index_clip, os.path.join(BASE_DIR, "faiss_clip.index"))
with open(os.path.join(BASE_DIR, "faiss_nombres.pkl"), "wb") as f:
    pickle.dump(nombres, f)
print("[✓] Índice CLIP guardado")

print("✔ Todos los índices fueron generados correctamente.")
