const { readFileSync } = require("node:fs");
const { join } = require("node:path");

const totalFields = ["subtotal", "discount", "tax", "shipping", "total"];
const orderFields = ["items", "customer_type", "discount_code", "distance_km", "is_express"];
const columns = ["test_name", ...orderFields, ...totalFields.map(field => `expected_${field}`), "expected_error"];
const stages = {
  validate_customer: { input: "customer", fields: { valid: "boolean" } },
  create_order: { input: "order", fields: { status: "string" } },
  calculate_total: { fields: { total: "number" }, canReject: true },
  process_payment: { fields: { status: "string" } },
  confirm_order: { fields: { status: "string", total: "number" }, canReject: true }
};

const object = value => value !== null && typeof value === "object" && !Array.isArray(value);

function read(name) {
  return readFileSync(join(__dirname, "..", "test_data", name), "utf8").replace(/^\uFEFF/, "");
}

function requireData(condition, location, message) {
  if (!condition) throw new Error(`${location}: ${message}`);
}

function decodeJson(source, location) {
  try {
    return JSON.parse(source);
  } catch (error) {
    throw new Error(`${location}: ${error.message}`, { cause: error });
  }
}

function readCsvRow(line, location) {
  requireData(/^(?:"(?:[^"]|"")*"|[^",]*)(?:,(?:"(?:[^"]|"")*"|[^",]*))*$/.test(line),
    location, "Malformed CSV row");
  return [...line.matchAll(/(?:^|,)("(?:[^"]|"")*"|[^",]*)/g)].map(([, cell]) =>
    cell.startsWith('"') ? cell.slice(1, -1).replaceAll('""', '"') : cell);
}

function checkOrder(order, location) {
  requireData(object(order), location, "Expected an order object");
  requireData(Array.isArray(order.items), location, "items must be an array");
  for (const [index, item] of order.items.entries()) {
    requireData(object(item) && typeof item.name === "string" &&
      Number.isFinite(item.price) && Number.isSafeInteger(item.quantity) && Number.isFinite(item.weight),
    location, `Invalid item data types at items[${index}]`);
  }
  requireData(["new", "regular"].includes(order.customer_type) &&
    typeof order.discount_code === "string" && order.discount_code.length > 0 &&
    Number.isFinite(order.distance_km) && typeof order.is_express === "boolean",
  location, "Invalid customer type, discount code, distance, or express flag");
}

function loadOrders() {
  const name = "order_calculations.csv";
  const [header, ...lines] = read(name).trimEnd().split(/\r?\n/);
  requireData(header === columns.join(","), `${name}:1`, "Unexpected CSV columns");
  const names = new Set();
  return lines.map((line, index) => {
    const location = `${name}:${index + 2}`;
    const cells = readCsvRow(line, location);
    requireData(cells.length === columns.length, location, "Incorrect CSV column count");
    const row = Object.fromEntries(columns.map((column, i) => [column, cells[i]]));
    checkName(row.test_name, names, location);
    requireData(["true", "false"].includes(row.is_express) && row.distance_km.trim() !== "",
      location, "Expected a boolean express flag and numeric distance");
    const order = {
      items: decodeJson(row.items, location),
      customer_type: row.customer_type,
      discount_code: row.discount_code,
      distance_km: Number(row.distance_km),
      is_express: row.is_express === "true"
    };
    checkOrder(order, location);
    const totals = totalFields.map(field => row[`expected_${field}`]);
    if (row.expected_error) {
      requireData(row.expected_error === "RangeError" && totals.every(value => value === ""),
        location, "Expected RangeError and empty totals");
    } else {
      requireData(totals.every(value => value.trim() !== "" && Number.isFinite(Number(value))),
        location, "Expected numeric totals");
    }
    const expected = row.expected_error ? null :
      Object.fromEntries(totalFields.map((field, i) => [field, Number(totals[i])]));
    return { name: row.test_name, ...order, expected };
  });
}

function checkName(name, names, location) {
  requireData(typeof name === "string" && name.trim() && !names.has(name),
    location, "Expected a unique nonempty scenario name");
  names.add(name);
}

function readJsonRows(name, label, key, validate) {
  const source = read(name);
  const data = decodeJson(source, name);
  const rows = key ? data?.[key] : data;
  requireData(Array.isArray(rows), name, "Expected an array of scenarios");
  const lines = source.split(/\r?\n/);
  const marker = new RegExp(`^\\s*"${label}"\\s*:\\s*`);
  const names = new Set();
  let nextLine = 0;
  for (const [index, row] of rows.entries()) {
    const encodedName = JSON.stringify(row?.[label]);
    const line = lines.findIndex((text, i) => i >= nextLine &&
      marker.test(text) && text.replace(marker, "").startsWith(encodedName));
    if (line >= 0) nextLine = line + 1;
    const location = line >= 0 ? `${name}:${line + 1}` : `${name}:1 (scenario ${index + 1})`;
    requireData(object(row), location, "Expected a scenario object");
    checkName(row[label], names, location);
    validate(row, location);
  }
  return rows;
}

function loadCustomers() {
  return readJsonRows("customer_validation.json", "test_name", null, ({ customer, expected }, location) => {
    requireData(object(customer) && object(expected) && typeof expected.is_valid === "boolean" &&
      Array.isArray(expected.errors) && expected.errors.every(error => typeof error === "string") &&
      expected.is_valid === (expected.errors.length === 0),
    location, "Expected a customer object and a consistent validity result");
  });
}

function loadWorkflows() {
  return readJsonRows("order_workflows.json", "name", "workflows", ({ steps }, location) => {
    requireData(Array.isArray(steps) && steps.length > 0, location, "Expected workflow steps");
    for (const [index, step] of steps.entries()) {
      const stepLocation = `${location} (step ${index + 1})`;
      requireData(object(step) && Object.hasOwn(stages, step.action) && object(step.expected),
        stepLocation, "Unknown action or missing expected result");
      const stage = stages[step.action];
      if (stage.input === "customer") {
        requireData(object(step.data), stepLocation, "Expected customer data");
      } else if (stage.input === "order") {
        checkOrder(step.data, stepLocation);
      }
      const fields = stage.canReject && step.expected.status === "rejected" ?
        { status: "string" } : stage.fields;
      requireData(Object.keys(step.expected).length === Object.keys(fields).length &&
        Object.entries(fields).every(([field, type]) => typeof step.expected[field] === type),
      stepLocation, "Unexpected result fields or types");
    }
  });
}

module.exports = { loadOrders, loadCustomers, loadWorkflows };
