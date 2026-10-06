import requests
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Modelo 
model = SentenceTransformer('all-MiniLM-L6-v2')

URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

def descargar_descripciones():
    response = requests.get(URL)
    cartas = response.json()["data"]
    descripciones = []
    nombres = []
    for carta in cartas:
        if "desc" in carta and carta["desc"].strip():  # solo si tiene descripción válida
            descripciones.append(carta["desc"])
            nombres.append(carta["name"])
    return nombres, descripciones

def crear_faiss(descripciones, nombres):
    # Convertimos descripciones en embeddings
    embeddings = model.encode(descripciones, convert_to_numpy=True)
    embeddings = np.array(embeddings).astype("float32")

    # Crear índice FAISS
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Guardar índice y datos
    faiss.write_index(index, "faiss_index.index")
    with open("faiss_names.pkl", "wb") as f:
        pickle.dump(nombres, f)
    with open("faiss_descriptions.pkl", "wb") as f:
        pickle.dump(descripciones, f)

if __name__ == "__main__":
    nombres, descripciones = descargar_descripciones()
    crear_faiss(descripciones, nombres)
    print("FAISS index y descripciones guardadas con SBERT.")
