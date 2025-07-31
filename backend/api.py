from flask import Flask, request, jsonify
from flask_cors import CORS
from search_text import buscar_por_descripcion
from flask import send_from_directory
from search_image_clip import buscar_similares_por_imagen_clip
import pickle
import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
CORS(app)

# Configurar Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
modelo = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route('/data/cartas/<path:filename>')
def serve_image(filename):
    abs_path = os.path.abspath("data/cartas")
    return send_from_directory(abs_path, filename)


# Cargar nombres y descripciones
with open("faiss_names.pkl", "rb") as f:
    NOMBRES = pickle.load(f)
with open("faiss_descriptions.pkl", "rb") as f:
    DESCRIPCIONES = pickle.load(f)

@app.route("/api/buscar", methods=["POST"])
def buscar_texto():
    texto = request.json.get("nombre", "").strip()
    cartas_desc = buscar_por_descripcion(texto)
    if cartas_desc:
        return jsonify({
            "carta": cartas_desc[0],
            "similares": cartas_desc[1:]
        })
    return jsonify({"error": "No se encontraron coincidencias en las descripciones."})

@app.route("/api/descripcion/<nombre>", methods=["GET"])
def obtener_descripcion(nombre):
    nombre = nombre.lower()
    for i, n in enumerate(NOMBRES):
        if n.lower() == nombre:
            descripcion_original = DESCRIPCIONES[i]
            prompt = f"Resume esta descripción de una carta de Yu-Gi-Oh! para mostrarla de forma clara al usuario:\n\n{descripcion_original}"
            try:
                respuesta = modelo.generate_content(prompt)
                resumen = respuesta.text
            except Exception:
                resumen = "Error al generar resumen con Gemini."
            return jsonify({"descripcion": resumen})
    return jsonify({"descripcion": "Descripción no encontrada"}), 404

@app.route("/api/similar", methods=["POST"])
def buscar_imagen():
    file = request.files["image"]
    file.save("temp.jpg")
    resultado = buscar_similares_por_imagen_clip("temp.jpg")  # esta función debe estar implementada
    return jsonify(resultado)


if __name__ == "__main__":
    print("Servidor Flask iniciado en http://localhost:5700")
    app.run(port=5000, debug=True)
