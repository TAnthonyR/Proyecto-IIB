async function buscarTexto() {
  const texto = document.getElementById("texto").value;
  const res = await fetch("http://localhost:5000/api/buscar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre: texto })
  });
  const data = await res.json();
  if (data.error) {
    document.getElementById("resultado").innerHTML = `<p><strong>${data.error}</strong></p>`;
    document.getElementById("rag-respuesta").innerHTML = "";

    if (data.similares && data.similares.length > 0) {
      mostrarSimilares(data.similares);
    } else {
      document.getElementById("similares").innerHTML = "";
    }

    return;
  }
  mostrarCarta(data.carta, "resultado");
  mostrarSimilares(data.similares);
  document.getElementById("rag-respuesta").innerHTML = ""; // Limpiar respuesta RAG
}

function mostrarCarta(carta, divId) {
  const div = document.getElementById(divId);
  div.innerHTML = `
  <h3>Resultados obtenidos:</h3>
  <img src="${carta.card_images?.[0]?.image_url}" class="card-img"><br>
  <p><strong>Name:</strong> ${carta.name}</p>
  <p><strong>Type:</strong> ${carta.type}</p>
  <p><strong>Description:</strong> ${carta.desc}</p>
  <p><strong>Race:</strong> ${carta.race}</p>
  <p><strong>Archetype:</strong> ${carta.archetype ?? '---'}</p>

  <div class="preguntas-rag">
    <h4>🤖 Preguntas comunes sobre esta carta:</h4>
    <button onclick="preguntarRAGDesdeBoton('¿Cómo se usa en un duelo la carta', '${carta.name}')">
        ¿Cómo se usa esta carta?
      </button>
    <button onclick="preguntarRAGDesdeBoton('¿Qué mazo va con', '${carta.name}')">
      ¿Qué tipo va con esta carta?
    </button>
  </div>
`;
}

function mostrarSimilares(similares) {
  const div = document.getElementById("similares");
  div.innerHTML = `<h3>Resultados similares:</h3>`;
  similares.forEach(carta => {
    div.innerHTML += `
      <div class="similares-container">
        <img src="${carta.card_images?.[0]?.image_url}" />
      </div>
    `;
  });
}

async function buscarImagen() {
  const input = document.getElementById("imgInput");
  const formData = new FormData();
  formData.append("image", input.files[0]);
  const res = await fetch("http://localhost:5000/api/similar", {
    method: "POST",
    body: formData
  });
  const data = await res.json();
  mostrarCarta(data.carta, "resultado");
  mostrarSimilares(data.similares);
  document.getElementById("rag-respuesta").innerHTML = ""; // Limpiar respuesta RAG
}

function markdownToHTML(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Negrita
    .replace(/\n/g, "<br>"); // Saltos de línea
}

async function preguntarRAGDesdeBoton(preguntaBase, cartaNombre) {
  const pregunta = `${preguntaBase} ${cartaNombre}?`;

  const res = await fetch("http://localhost:5000/api/rag", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: pregunta })
  });

  const data = await res.json();
  const respuestaCruda = data.respuesta || "No se pudo obtener respuesta.";
  const respuestaHTML = markdownToHTML(respuestaCruda);

  document.getElementById("rag-respuesta").innerHTML = `
    🤖 <strong>${pregunta}</strong><br>
    👉 ${respuestaHTML}
  `;
}