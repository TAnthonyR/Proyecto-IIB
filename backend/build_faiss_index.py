import requests
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
MAX_CARTAS = 1505

def descargar_descripciones():
    response = requests.get(URL)
    cartas = response.json()["data"][:MAX_CARTAS]
    descripciones = []
    nombres = []
    for carta in cartas:
        if "desc" in carta:
            descripciones.append(carta["desc"])
            nombres.append(carta["name"])
    return nombres, descripciones

def crear_faiss(descripciones, nombres):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(descripciones).toarray()

    index = faiss.IndexFlatL2(X.shape[1])
    index.add(np.array(X).astype("float32"))

    faiss.write_index(index, "faiss_index.index")
    with open("faiss_names.pkl", "wb") as f:
        pickle.dump(nombres, f)
    with open("faiss_descriptions.pkl", "wb") as f:
        pickle.dump(descripciones, f)

if __name__ == "__main__":
    nombres, descripciones = descargar_descripciones()
    crear_faiss(descripciones, nombres)
    print("FAISS index y descripciones guardadas.")
