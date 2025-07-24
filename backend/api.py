
from flask import Flask, request, jsonify
from flask_cors import CORS
from search_text import buscar_por_nombre, buscar_similares_por_nombre, buscar_por_tipo
from search_image_clip import buscar_similares_por_imagen_clip
from rag_chat import responder_pregunta

app = Flask(__name__)
CORS(app)

@app.route("/api/buscar", methods=["POST"])
def buscar_texto():
    nombre = request.json.get("nombre", "")
    carta = buscar_por_nombre(nombre)
    if carta:
        similares = buscar_similares_por_nombre(carta["name"])
        return jsonify({"carta": carta, "similares": similares})
    # Si no encuentra por nombre, prueba por tipo
    cartas_tipo = buscar_por_tipo(nombre)
    if cartas_tipo:
        return jsonify({
            "error": f"No se encontró una carta exacta con ese nombre, pero se encontraron cartas del tipo '{nombre}'.",
            "similares": cartas_tipo
        })
    else:
        return jsonify({"error": "Carta no encontrada"})

@app.route("/api/similar", methods=["POST"])
def buscar_imagen():
    file = request.files["image"]
    file.save("temp.jpg")
    resultado = buscar_similares_por_imagen_clip("temp.jpg")
    return jsonify(resultado)


@app.route("/api/rag", methods=["POST"])
def rag_chat():
    pregunta = request.json.get("query", "")
    respuesta = responder_pregunta(pregunta)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
