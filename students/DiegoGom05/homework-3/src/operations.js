function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error('No se puede dividir entre cero');
  }

  return a / b;
}

function calculate(a, b, operator) {
  if (operator === '+') {
    return add(a, b);
  }

  if (operator === '-') {
    return subtract(a, b);
  }

  if (operator === '*') {
    return multiply(a, b);
  }

  if (operator === '/') {
    return divide(a, b);
  }

  throw new Error('Operador desconocido');
}

export { calculate };
