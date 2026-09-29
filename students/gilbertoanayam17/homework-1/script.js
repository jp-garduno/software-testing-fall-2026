// Muestra el año actual en el pie de página.
const anio = document.getElementById("anio");

if (anio) {
  anio.textContent = new Date().getFullYear();
}
