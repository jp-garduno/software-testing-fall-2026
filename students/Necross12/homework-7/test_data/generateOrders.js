const { faker } = require("@faker-js/faker");
const fs = require("fs");
const path = require("path");
// faker.seed(); // semilla reproducible

const r2 = (n) => Math.round((n + Number.EPSILON) * 100) / 100;
const CODES = {
  NONE: [0, 0],
  SAVE10: [50, 0.1],
  SAVE20: [100, 0.2],
  FREESHIP: [0, 0],
  NEWUSER: [0, 0.15],
};

const filas = [];
for (let i = 1; i <= 100; i++) {
  const items = Array.from(
    { length: faker.number.int({ min: 1, max: 4 }) },
    () => ({
      name: faker.commerce.product(),
      price: faker.number.int({ min: 5, max: 150 }),
      quantity: faker.number.int({ min: 1, max: 5 }),
      weight: faker.number.float({ min: 0.1, max: 5, fractionDigits: 1 }),
    }),
  );
  const code = faker.helpers.arrayElement(Object.keys(CODES));
  const tipo =
    code === "NEWUSER" ? "new" : faker.helpers.arrayElement(["new", "regular"]);
  const dist = faker.number.int({ min: 0, max: 200 });
  const exp = faker.datatype.boolean();

  // Valores que se esperan calcular
  const sub = r2(items.reduce((s, x) => s + x.price * x.quantity, 0));
  const [min, pct] = CODES[code];
  const ok = sub >= min;
  const desc = ok ? r2(sub * pct) : 0;
  const tax = r2((sub - desc) * 0.08);
  const peso = items.reduce((s, x) => s + x.weight * x.quantity, 0);
  let ship = peso * 0.5 + dist * 0.1;
  if (exp) ship *= 1.5;
  ship = code === "FREESHIP" ? 0 : r2(ship);
  const total = r2(sub - desc + tax + ship);

  const itemsStr = JSON.stringify(items).replace(/"/g, "'");
  filas.push(
    `generated_${i},"${itemsStr}",${tipo},${code},${dist},${exp},` +
      [sub, desc, tax, ship, total].map((n) => n.toFixed(2)).join(","),
  );
}

const header =
  "test_name,items,customer_type,discount_code,distance_km,is_express,expected_subtotal,expected_discount,expected_tax,expected_shipping,expected_total";
fs.writeFileSync(
  path.join(__dirname, "100PruebasAlAzar.csv"),
  [header, ...filas].join("\n"),
);
