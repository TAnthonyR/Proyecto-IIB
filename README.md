
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
pip install flask flask-cors requests numpy faiss-cpu pillow sentence-transformers google-generativeai
```

Modelos utilizados:
- `sentence-transformers/all-MiniLM-L6-v2`
- `openai/clip-vit-base-patch32` (vía CLIP)
- Google Gemini 2.5 Flash (API KEY en .env)

## 🧠 Comandos clave

### 1. Descargar las cartas Yu-Gi-Oh! (genera la carpeta data/cartas)
```bash
python cards_downloader.py 
```
⏱️ Toma ~1 hora aprox. (más de 10k cartas con imágenes)

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

## 🟥 Posible error al ejecutar el backend

- Error: 
PS C:..\backend> python api.py
Using a slow image processor as `use_fast` is unset and a slow processor was saved with this model. `use_fast=True` will be the default behavior in v4.52, even if the model was saved with a slow processor. This will result in minor differences in outputs. You'll still be able to use a slow processor with `use_fast=False`.
Traceback (most recent call last):
  File "C:\EPN\Semestre_7\RI\proyectoIIB\backend\api.py", line 6, in <module>
    from rag_chat import responder_pregunta
  File "C:\EPN\Semestre_7\RI\proyectoIIB\backend\rag_chat.py", line 8, in <module>
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
                            ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "<frozen os>", line 714, in __getitem__
KeyError: 'GOOGLE_API_KEY'

- Poner en terminal de visual code y se arregla el problema:
```bash
$env:GOOGLE_API_KEY="Colocar API"
```

### 🖲️ Ejecutar en ruta del backend Flask
```bash
python api.py
```

## 🌐 Ejcutar en ruta de la Interfaz Web
```bash
python -m http.server 5500
```
En navegador ingresar -> localhost:5500

Permite:
- Búsqueda por texto o imagen
- Mostrar carta y similares
- Preguntas tipo RAG como:
  - ¿Qué mazo va con [carta]?
  - ¿Qué carta destruye/gana a [carta]?

