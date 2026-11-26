// src/tests/transactionProcessor.test.js
const { calculateDiscount } = require("../transactionProcessor");
const notificationService = require("../services/notificationService");

// Mockear el módulo completo antes de los tests
jest.mock("../services/notificationService", () => ({
  sendAlert: jest.fn(() => true),
}));

describe("Exercise 4: Coverage Challenge - calculateDiscount", () => {
  beforeEach(() => {
    // Limpiar el historial de llamadas antes de cada prueba
    jest.clearAllMocks();
  });

  // 1. Manejo de Errores (Guard Clause)
  test("should throw error if user is missing or amount is invalid", () => {
    expect(() => calculateDiscount(-50, { isVIP: false })).toThrow(
      "Invalid transaction input",
    );
    expect(() => calculateDiscount(100, null)).toThrow(
      "Invalid transaction input",
    );
  });

  // 2. Cobertura de Condición Compuesta 1: (amount > 1000 || user.isVIP)
  test("should apply 20% discount if amount > 1000 (even if not VIP)", () => {
    const result = calculateDiscount(1500, {
      isVIP: false,
      email: "test@example.com",
    });
    expect(result).toBe(1200);
  });

  test("should apply 20% discount if user is VIP (even if amount <= 1000)", () => {
    const result = calculateDiscount(400, {
      isVIP: true,
      email: "vip@example.com",
    });
    expect(result).toBe(320);
  });

  // 3. Cobertura de Condición Compuesta 2: (amount >= 500 && user.yearsAsCustomer >= 2)
  test("should apply 10% discount when amount >= 500 AND yearsAsCustomer >= 2", () => {
    const result = calculateDiscount(600, {
      isVIP: false,
      yearsAsCustomer: 3,
      email: "test@example.com",
    });
    expect(result).toBe(540);
  });

  test("should NOT apply 10% discount if amount >= 500 but yearsAsCustomer < 2", () => {
    const result = calculateDiscount(600, {
      isVIP: false,
      yearsAsCustomer: 1,
      email: "test@example.com",
    });
    expect(result).toBe(600);
  });

  // 4. Cobertura de Camino Sin Descuento (Falsos en todas las condiciones de descuento)
  test("should apply 0% discount when no criteria are met", () => {
    const result = calculateDiscount(300, {
      isVIP: false,
      yearsAsCustomer: 1,
      email: "test@example.com",
    });
    expect(result).toBe(300);
  });

  // 5. Cobertura del Mock y Notificación (> 2000 finalAmount)
  test("should trigger sendAlert notification when finalAmount exceeds 2000", () => {
    const finalAmount = calculateDiscount(3000, {
      isVIP: false,
      email: "buyer@example.com",
    });

    expect(finalAmount).toBe(2400);
    expect(notificationService.sendAlert).toHaveBeenCalledTimes(1);
    expect(notificationService.sendAlert).toHaveBeenCalledWith(
      "buyer@example.com",
      "High value transaction processed: $2400",
    );
  });

  test("should NOT trigger sendAlert notification when finalAmount is 2000 or less", () => {
    calculateDiscount(1000, { isVIP: false, email: "buyer@example.com" });
    expect(notificationService.sendAlert).not.toHaveBeenCalled();
  });
});
