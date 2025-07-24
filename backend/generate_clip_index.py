import os
import numpy as np
import pickle
import faiss
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def vectorizar_imagen_clip(path):
    image = Image.open(path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt", padding=True)
    outputs = model.get_image_features(**inputs)
    return outputs.detach().numpy()[0]

carpeta = "data/cartas"
vectores = []
nombres = []

for archivo in os.listdir(carpeta):
    if archivo.endswith(".jpg"):
        ruta = os.path.join(carpeta, archivo)
        try:
            v = vectorizar_imagen_clip(ruta)
            vectores.append(v)
            nombres.append(archivo.replace(".jpg", ""))
        except:
            continue

vectores = np.array(vectores).astype("float32")
index = faiss.IndexFlatL2(vectores.shape[1])
index.add(vectores)

faiss.write_index(index, "faiss_clip.index")
with open("faiss_nombres.pkl", "wb") as f:
    pickle.dump(nombres, f)