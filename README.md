
# Búsqueda de Cartas Yu-Gi-Oh!

Este proyecto implementa un sistema de Recuperación Aumentada por Generación (RAG) sobre un corpus imagen-texto de cartas Yu-Gi-Oh!, permitiendo búsqueda por texto o imagen y respuestas generadas por un modelo.

## 📦 Estructura del Proyecto

```
backend/
├── api.py
├── cards_downloader.py          # Descarga y guarda las cartas desde la API
├── generate_clip_index.py       # Construye embeddings CLIP y FAISS para búsqueda por imagen
├── prepare_rag_index.py         # Prepara el índice RAG con descripciones
├── rag_chat.py                  # Llama al modelo generativo Gemini con contexto
├── search_text.py               # Búsqueda textual y similares
├── search_image_clip.py         # Búsqueda por imagen
├── data/                        # Corpus imagen-texto descargado
├── faiss_clip.index             # Índice FAISS para imagen (CLIP)
├── rag_faiss.index              # Índice FAISS para texto (RAG)
└── *.pkl                        # Datos serializados (nombres, textos)
frontend/
├── index.html
├── app.js
└── estilos.css
```

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

Modelos utilizados:
- `sentence-transformers/all-MiniLM-L6-v2`
- `openai/clip-vit-base-patch32` (vía CLIP)
- Google Gemini 2.5 Flash (API KEY en .env)

## 🧠 Comandos clave

### 1. Descargar las cartas Yu-Gi-Oh!
```bash
python cards_downloader.py
```
⏱️ Toma ~1 hora (más de 10k cartas con imágenes)

### 2. Generar índice CLIP (imagen-texto)
```bash
python generate_clip_index.py
```
Salida: `faiss_clip.index`, `faiss_nombres.pkl`

### 3. Generar índice RAG (texto-descripción)
```bash
python prepare_rag_index.py
```
Salida: `rag_faiss.index`, `rag_nombres.pkl`, `rag_textos.pkl`

### 4. Ejecutar backend Flask
```bash
python api.py
```

## 🌐 Interfaz Web

Permite:
- Búsqueda por texto o imagen
- Mostrar carta y similares
- Preguntas tipo RAG como:
  - ¿Qué mazo va con [carta]?
  - ¿Qué carta destruye/gana a [carta]?

