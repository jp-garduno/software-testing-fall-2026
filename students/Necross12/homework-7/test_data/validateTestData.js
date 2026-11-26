const fs = require("fs");
const { parse } = require("csv-parse/sync");

// campos del csv
const COLUMNAS = [
  "test_name",
  "items",
  "customer_type",
  "discount_code",
  "distance_km",
  "is_express",
  "expected_subtotal",
  "expected_discount",
  "expected_tax",
  "expected_shipping",
  "expected_total",
];

function validarCSV(ruta) {
  const errores = [];
  const filas = parse(fs.readFileSync(ruta, "utf8"), {
    columns: true,
    skip_empty_lines: true, // puede aver salto de lina y no romper nada, yei
    info: true,
  });

  if (filas.length < 25)
    errores.push(`${ruta}: se requieren al menos 25 casos; hay ${filas.length}`);

  for (const { record: r, info } of filas) {
    const l = info.lines;
    for (const c of COLUMNAS)
      if (r[c] === undefined || r[c] === "")
        errores.push(`Línea ${l}: falta "${c}"`);
    if (typeof r.items === "string") {
      try {
        const items = JSON.parse(r.items.replace(/'/g, '"'));
        if (!Array.isArray(items) && !r.test_name.startsWith("(invalida)"))
            errores.push(`Línea ${l}: "items" debe ser un arreglo`);
      }
      catch {
        errores.push(`Línea ${l}: "items" no es JSON válido`);
      }
    }
    if (!["new", "regular"].includes(r.customer_type))
      errores.push(`Línea ${l}: customer_type inválido`);
    if (!["true", "false"].includes(r.is_express))
      errores.push(`Línea ${l}: is_express debe ser true/false`);
    if (!Number.isFinite(Number(r.distance_km)))
      errores.push(`Línea ${l}: distance_km no es numérico`);
    if (r.expected_subtotal !== "ERROR") {
      for (const c of COLUMNAS.slice(6))
        if (!Number.isFinite(Number(r[c])))
            errores.push(`Línea ${l}: ${c} no es numérico`);
    } else {
      for (const c of COLUMNAS.slice(7))
        if (!Number.isFinite(Number(r[c])))
            errores.push(`Línea ${l}: ${c} no es numérico`);
    }
  }

  return errores;
}

function validarCustomerJSON(ruta) {
  const errores = [];
  const casos = JSON.parse(fs.readFileSync(ruta, "utf8"));
  const minimos = {
    "valido": 3,
    "email invalido": 4,
    "telefono invalido": 4,
    "direccion invalida": 5,
    "tarjeta invalida": 8,
    "errores multiples": 6,
  };

  if (!Array.isArray(casos)) {
    return ["customerValidation.json debe contener un arreglo"];
  }
  if (casos.length < 30)
    errores.push(`customerValidation.json: se requieren al menos 30 casos; hay ${casos.length}`);

  for (const [indice, caso] of casos.entries()) {
    const nombre = caso?.test_name || `caso ${indice + 1}`;
    if (typeof caso?.test_name !== "string" || !caso.test_name)
      errores.push(`${nombre}: falta test_name`);
    if (!caso?.customer || typeof caso.customer !== "object")
      errores.push(`${nombre}: customer debe ser un objeto`);
    else {
      for (const campo of ["email", "phone"])
        if (typeof caso.customer[campo] !== "string")
            errores.push(`${nombre}: customer.${campo} debe ser texto`);
      for (const [objeto, campos] of [
        ["billing_address", ["street", "city", "state", "zip"]],
        ["credit_card", ["number", "expiration", "cvv"]],
      ]) {
        const valor = caso.customer[objeto];
        if (!valor || typeof valor !== "object") {
            errores.push(`${nombre}: customer.${objeto} debe ser un objeto`);
            continue;
        }
        for (const campo of campos)
            if (typeof valor[campo] !== "string")
                errores.push(`${nombre}: customer.${objeto}.${campo} debe ser texto`);
      }
    }
    if (typeof caso?.expected?.is_valid !== "boolean" ||
      !Array.isArray(caso?.expected?.errors))
      errores.push(`${nombre}: expected debe incluir is_valid y errors`);
    else if (caso.expected.is_valid !== (caso.expected.errors.length === 0))
      errores.push(`${nombre}: is_valid no coincide con expected.errors`);
  }

  for (const [categoria, minimo] of Object.entries(minimos)) {
    const cantidad = casos.filter((caso) => caso.category === categoria).length;
    if (cantidad < minimo)
      errores.push(`customerValidation.json: ${categoria} requiere ${minimo} casos; hay ${cantidad}`);
  }

  return errores;
}

function validarWorkflowsJSON(ruta) {
  const documento = JSON.parse(fs.readFileSync(ruta, "utf8"));
  if (!Array.isArray(documento.workflows))
    return ["orderWorkflows.json debe incluir un arreglo workflows"];

  const errores = [];
  if (documento.workflows.length < 3)
    errores.push(`orderWorkflows.json: se requieren al menos 3 flujos; hay ${documento.workflows.length}`);

  for (const [indice, flujo] of documento.workflows.entries()) {
    const nombre = flujo?.name || `flujo ${indice + 1}`;
    if (typeof flujo?.name !== "string" || !flujo.name)
      errores.push(`${nombre}: falta name`);
    if (!Array.isArray(flujo?.steps) || flujo.steps.length === 0) {
      errores.push(`${nombre}: steps debe ser un arreglo no vacío`);
      continue;
    }
    for (const [pasoIndice, paso] of flujo.steps.entries()) {
      if (!["validate_customer", "create_order", "calculate_total", "process_payment"]
        .includes(paso?.action))
        errores.push(`${nombre}, paso ${pasoIndice + 1}: action inválida`);
      if (!paso?.expected || typeof paso.expected !== "object")
        errores.push(`${nombre}, paso ${pasoIndice + 1}: falta expected`);
    }
  }
  return errores;
}

module.exports = { validarCSV, validarCustomerJSON, validarWorkflowsJSON };
