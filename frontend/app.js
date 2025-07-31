async function buscarTexto() {
  const texto = document.getElementById("texto").value;
  const res = await fetch("http://localhost:5000/api/buscar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre: texto })
  });
  const data = await res.json();

  const resultadoDiv = document.getElementById("resultado");
  if (data.error) {
    resultadoDiv.innerHTML = `<p><strong>${data.error}</strong></p>`;
    document.getElementById("descripcion").innerText = "";
    document.getElementById("similares").innerHTML = "";
    return;
  }

  mostrarCarta(data.carta, "resultado");
  mostrarSimilares(data.similares);
  cargarDescripcion(data.carta.name);
}

function mostrarCarta(carta, divId) {
  const div = document.getElementById(divId);
  const host = "http://localhost:5000"; // o usa tu IP o dominio si estás en red
  const imgTag = carta.image_url ? `<img src="${host + carta.image_url}" class="card-img"><br>` : "";
  div.innerHTML = `
    <h3>Resultados obtenidos:</h3>
    ${imgTag}
    <p><strong>Name:</strong> ${carta.name}</p>
    <p><strong>Resumen:</strong> <span id="descripcion">Cargando resumen...</span></p>
  `;
}


function mostrarSimilares(similares) {
  const div = document.getElementById("similares");
  const host = "http://localhost:5000";
  div.innerHTML = `<h3>Resultados similares:</h3><div class="similares-grid"></div>`;

  const grid = div.querySelector(".similares-grid");
  grid.style.display = "flex";
  grid.style.flexWrap = "wrap";
  grid.style.gap = "20px";
  grid.style.justifyContent = "center";

  similares.forEach(carta => {
    const cardHTML = `
      <div style="width: 200px; border: 1px solid #ccc; border-radius: 8px; padding: 10px; text-align: center;">
        <img src="${host + carta.image_url}" alt="${carta.name}" style="width: 100%; height: auto; border-radius: 5px;">
        <h4 style="margin-top: 10px;">${carta.name}</h4>
        <p style="font-size: 13px;">${carta.desc}</p>
      </div>
    `;
    grid.innerHTML += cardHTML;
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
  cargarDescripcion(data.carta.name);
}

function cargarDescripcion(nombre) {
  fetch(`http://localhost:5000/api/descripcion/${encodeURIComponent(nombre)}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("descripcion").innerText = data.descripcion;
    })
    .catch(err => {
      document.getElementById("descripcion").innerText = "Descripción no disponible.";
    });
}
