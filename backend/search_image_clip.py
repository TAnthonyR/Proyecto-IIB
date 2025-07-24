import os
import pickle
import numpy as np
import faiss
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from search_text import buscar_por_nombre, buscar_similares_por_nombre

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def vectorizar_imagen_clip(path):
    image = Image.open(path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt", padding=True)
    outputs = model.get_image_features(**inputs)
    return outputs.detach().numpy()[0]

def buscar_similares_por_imagen_clip(path, top_k=1):
    vector = vectorizar_imagen_clip(path).astype("float32")
    index = faiss.read_index("faiss_clip.index")
    with open("faiss_nombres.pkl", "rb") as f:
        nombres = pickle.load(f)

    D, I = index.search(np.array([vector]), top_k)
    idx = I[0][0]
    nombre = nombres[idx].replace("_", " ")
    carta = buscar_por_nombre(nombre)
    similares = buscar_similares_por_nombre(nombre)
    return {"carta": carta, "similares": similares}