const Order = require("../src/orderCalculator");
const { Customer } = require("../src/customerValidator");
const { workflows } = require("../test_data/orderWorkflows.json");

// Fecha fija para que la prubas de las fehca funcionen de manera correcta
const AHORA = new Date(2026, 10, 11);

// "ctx" guarda el estado compartido entre pasos (cliente, pedido, total).
function ejecutarPaso(paso, ctx) {
  switch (paso.action) {
    case "validate_customer": {
      const r = Customer.fromJSON(paso.data).validate(AHORA);
      ctx.clienteValido = r.is_valid;
      return { valid: r.is_valid, errors: r.errors };
    }
    case "create_order": {
      if (!ctx.clienteValido)
        return { status: "rejected" };
      const d = paso.data;
      ctx.order = new Order(d.items, d.customer_type);
      if (d.discount_code)
        ctx.order.applyDiscount(d.discount_code);
      ctx.order.setShipping(d.distance_km, d.is_express);
      return { status: "created" };
    }
    case "calculate_total": {
      try {
        ctx.total = ctx.order.calculateTotal();
        return ctx.total;
      } catch (e) {
        ctx.total = null;
        return { error: e.message };
      }
    }
    case "process_payment": {
      if (!ctx.total)
        return { status: "not_processed" };
      return { status: "success", amount: ctx.total.total };
    }
    default:
      throw new Error(`Acción desconocida: ${paso.action}`);
  }
}

describe("Integración: flujos de pedido completos (orderWorkflows.json)", () => {
  test("el JSON tiene al menos 3 workflows", () => {
    expect(workflows.length).toBeGreaterThanOrEqual(3);
  });

  test.each(workflows.map((w) => [w.name, w]))("%s", (_nombre, wf) => {
    const ctx = {};
    for (const paso of wf.steps) {
      const real = ejecutarPaso(paso, ctx);
      for (const [clave, esperado] of Object.entries(paso.expected)) {
        if (typeof esperado === "number")
          expect(real[clave]).toBeCloseTo(esperado, 2);
        else
          expect(real[clave]).toEqual(esperado);
      }
    }
  });
});
