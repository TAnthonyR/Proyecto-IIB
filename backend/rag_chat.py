import os
import faiss
import numpy as np
import pickle
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Inicializa el modelo local de embeddings y el generador de Gemini
embedder = SentenceTransformer("all-MiniLM-L6-v2")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Carga FAISS index y nombres
index = faiss.read_index("rag_faiss.index")
with open("rag_nombres.pkl", "rb") as f:
    nombres = pickle.load(f)
with open("rag_textos.pkl", "rb") as f:
    textos = pickle.load(f)

def responder_pregunta(pregunta, top_k=3):
    # Vectoriza la pregunta
    vec = embedder.encode([pregunta]).astype("float32")
    D, I = index.search(vec, top_k)

    # Construir contexto desde los nombres y descripciones
    contexto = ""
    for idx in I[0]:
        try:
            nombre_carta = nombres[idx]
            descripcion = textos[nombre_carta]
            contexto += f"Nombre: {nombre_carta}\nDescripción: {descripcion}\n\n"
        except (IndexError, KeyError):
            continue  # ignora si hay algún índice fuera de rango o nombre inexistente

    # Construir prompt
    prompt = (
        "Actúa como experto en cartas Yu-Gi-Oh. Usa el siguiente contexto para responder "
        "de forma clara y específica la pregunta del usuario. Si no sabes la respuesta, di que no sabes.\n\n"
        f"Contexto:\n{contexto}\n"
        f"Pregunta: {pregunta}\n"
        "Respuesta:"
    )

    # Genera respuesta con Gemini
    respuesta = model.generate_content(prompt)
    return respuesta.text