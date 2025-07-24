import requests
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
resp = requests.get(url).json()
data = resp["data"]

vectores = []
nombres = []
textos = {}

for carta in data:
    nombre = carta["name"]
    texto = f"{carta['name']}. {carta.get('type','')}. {carta.get('race','')}. {carta.get('desc','')}"
    vec = model.encode([texto])[0]
    vectores.append(vec)
    nombres.append(nombre)
    textos[nombre] = texto

vectores = np.array(vectores).astype("float32")
index = faiss.IndexFlatL2(vectores.shape[1])
index.add(vectores)

faiss.write_index(index, "rag_faiss.index")
with open("rag_nombres.pkl", "wb") as f:
    pickle.dump(nombres, f)
with open("rag_textos.pkl", "wb") as f:
    pickle.dump(textos, f)