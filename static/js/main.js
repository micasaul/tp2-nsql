document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("capitulos-container");

  const tempMap = {
    1: "Temporada 1 (2019)",
    2: "Temporada 2 (2020)",
    3: "Temporada 3 (2023)"
  };

  async function cargarCapitulos() {
    const res = await fetch("/capitulos");
    const capitulos = await res.json();

    container.innerHTML = "";

    for (const temp in tempMap) {
      const divTemp = document.createElement("div");
      divTemp.classList.add("temporada");

      const title = document.createElement("h2");
      title.textContent = tempMap[temp];
      title.style.cursor = "pointer";

      const lista = document.createElement("ul");
      lista.style.display = "none"; 

      title.addEventListener("click", () => {
        lista.style.display = lista.style.display === "none" ? "block" : "none";
      });

      const capTemp = capitulos.filter(c => {
        const num = parseInt(c.numero);
        if (temp == 1) return num >= 1 && num <= 8;
        if (temp == 2) return num >= 9 && num <= 16;
        if (temp == 3) return num >= 17 && num <= 24;
      });

      capTemp.forEach(c => {
        const li = document.createElement("li");
        li.textContent = `${c.numero}: ${c.nombre} [${c.estado}] `;

        if (c.estado === "disponible") {
          const btn = document.createElement("button");
          btn.textContent = "Reservar";
          btn.addEventListener("click", () => reservarCap(c.numero));
          li.appendChild(btn);
        } else if (c.estado === "reservado") {
          const btn = document.createElement("button");
          btn.textContent = "Confirmar";
          btn.addEventListener("click", () => confirmarCap(c.numero, 1500));
          li.appendChild(btn);
        } 
        lista.appendChild(li);
      });

      divTemp.appendChild(title);
      divTemp.appendChild(lista);
      container.appendChild(divTemp);
    }
  }

  async function reservarCap(id) {
    const res = await fetch(`/reservar/${id}`, { method: "POST" });
    const data = await res.json();
    alert(data.mensaje || data.error);
    cargarCapitulos(); 
  }

  async function confirmarCap(id, precio) {
    const res = await fetch(`/confirmar/${id}/${precio}`, { method: "POST" });
    const data = await res.json();
    alert(data.mensaje || data.error);
    cargarCapitulos(); 
  }

  cargarCapitulos();
});