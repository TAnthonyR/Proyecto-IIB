import faiss
import numpy as np
import pickle
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# --- Cargar modelo CLIP y procesador ---
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# --- Cargar índice FAISS y nombres ---
index = faiss.read_index("faiss_clip.index")
with open("faiss_nombres.pkl", "rb") as f:
    NOMBRES = pickle.load(f)

# --- Función para vectorizar imagen nueva ---
def vectorizar_imagen_clip(path):
    image = Image.open(path).convert("RGB")
    inputs = clip_processor(images=image, return_tensors="pt", padding=True)
    outputs = clip_model.get_image_features(**inputs)
    return outputs.detach().numpy()[0]

# --- Búsqueda por imagen ---
def buscar_similares_por_imagen_clip(path, top_k=5):
    vector = vectorizar_imagen_clip(path).reshape(1, -1).astype("float32")
    _, indices = index.search(vector, top_k)

    resultados = []
    for i in indices[0]:
        nombre = NOMBRES[i]
        nombre_archivo = nombre + ".jpg"
        resultados.append({
            "name": nombre,
            "image_url": f"/data/cartas/{nombre_archivo}"
        })
    return resultados
