
# Buscador de Cartas Yu-Gi-Oh!

Este proyecto implementa un sistema de búsqueda híbrido para cartas Yu-Gi-Oh!, permitiendo consultas por texto y por imagen. También se incluye un resumen generado automáticamente de la carta principal utilizando Gemini.

## 📁 Estructura del Proyecto

```
proyectoIIB-final/
├── backend/
│   ├── api.py                       # API Flask principal
│   ├── cards_downloader.py         # Descarga cartas desde la API oficial
│   ├── build_all_faiss_indexes.py  # Genera vectores de imagen (CLIP + FAISS) y texto
│   ├── search_text.py              # Búsqueda basada en descripciones
│   ├── search_image_clip.py        # Búsqueda basada en imagen
│   ├── faiss_names.pkl             # Nombres para búsqueda por texto
│   ├── faiss_descriptions.pkl      # Descripciones de cartas
│   ├── faiss_clip.index            # Índice FAISS (CLIP - imágenes)
│   ├── faiss_nombres.pkl           # Nombres para búsqueda por imagen
│   └── data/
│       └── cartas/                 # Carpeta local con imágenes de las cartas
├── frontend/
│   ├── index.html                  # Interfaz gráfica
│   ├── app.js                      # Lógica JS para interacción con backend
│   └── estilos.css                 # Estilos personalizados
```

## ⚙️ Instalación y Requisitos

```bash
pip install flask flask-cors requests numpy faiss-cpu pillow transformers google-generativeai
```

### Modelos Utilizados
- `openai/clip-vit-base-patch32` (para embeddings de imagen)
- Google Gemini Flash (`GOOGLE_API_KEY` desde `.env` o variable de entorno)

## 🔧 Comandos Importantes

### 1. Descargar Cartas Yu-Gi-Oh! (con imágenes)
```bash
python backend/cards_downloader.py
```
📌 Se descargan ~2000 cartas en la carpeta `backend/data/cartas`

### 2. Generar Índice de Imágenes (CLIP + FAISS)
```bash
python backend/build_all_fais_indexes.py
```
📦 Genera:
- `faiss_clip.index`
- `faiss_nombres.pkl`

## 🟡 Ejecutar el Backend Flask

Antes de ejecutar, asegúrate de exportar la API key de Gemini:

```bash
$env:GOOGLE_API_KEY="TU_API_KEY_AQUI"  # En PowerShell
```

Luego ejecuta el backend desde la carpeta `backend`:

```bash
python api.py
```

## 🌐 Ejecutar la Interfaz Web

Desde la carpeta `frontend`, usa un servidor simple:

```bash
python -m http.server 5500
```

Abre en el navegador:  
📎 `http://localhost:5500`

## ✨ Funcionalidades Soportadas

- ✅ Buscar carta por texto (por nombre, tipo o contenido en la descripción)
- ✅ Buscar carta por imagen (mediante CLIP)
- ✅ Ver imagen y resumen de la carta principal (usando Gemini)
- ✅ Mostrar cartas similares con sus imágenes y descripciones
