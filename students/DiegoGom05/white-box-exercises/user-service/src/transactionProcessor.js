// src/transactionProcessor.js
const { sendAlert } = require("./services/notificationService");

function calculateDiscount(amount, user) {
  // Manejo de casos de borde / guard clause
  if (!user || amount <= 0) {
    throw new Error("Invalid transaction input");
  }

  let discountRate = 0;

  // Condición compuesta 1: Evaluaremos múltiples sub-expresiones
  if (amount > 1000 || user.isVIP) {
    discountRate = 0.2;
  } else if (amount >= 500 && user.yearsAsCustomer >= 2) {
    // Condición compuesta 2
    discountRate = 0.1;
  }

  const finalAmount = amount - amount * discountRate;

  // Notificación opcional basada en monto final
  if (finalAmount > 2000) {
    sendAlert(user.email, `High value transaction processed: $${finalAmount}`);
  }

  return finalAmount;
}

module.exports = { calculateDiscount };
