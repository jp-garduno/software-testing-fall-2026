const min = 0;
const max = 100;
let cont = 0;

const valueDisplay = document.getElementById('contador_valor');
const progressBar = document.getElementById('contador_progress');

const mas10 = document.getElementById('mas10');
const mas1 = document.getElementById('mas1');
const menos1 = document.getElementById('menos1');
const menos10 = document.getElementById('menos10');

function limite(value) {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

function pintar() {
  valueDisplay.textContent = cont;
  progressBar.style.width = `${cont}%`;
  progressBar.setAttribute('aria-valuenow', cont);
  progressBar.classList.remove('bg-danger', 'bg-warning', 'bg-success');

  if (cont < 33) progressBar.classList.add('bg-danger');
  else if (cont < 66) progressBar.classList.add('bg-warning');
  else progressBar.classList.add('bg-success');
}

function cambiarValor(amount) {
  cont = limite(cont + amount);
  pintar();
}

mas10.addEventListener('click', () => cambiarValor(10));
mas1.addEventListener('click', () => cambiarValor(1));
menos1.addEventListener('click', () => cambiarValor(-1));
menos10.addEventListener('click', () => cambiarValor(-10));

pintar();
