const VALIDAR_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const VALIDAR_TELEFONO = /^\(\d{3}\) \d{3}-\d{4}$/; // (XXX) XXX-XXXX
const VALIDAR_ESTADO = /^[A-Z]{2}$/;
const VALIDAR_ZIP = /^\d{5}(-\d{4})?$/;
const VALIDAR_CVV = /^\d{3,4}$/;
const VALIDAR_EXPIRACION = /^(0[1-9]|1[0-2])\/(\d{4})$/; // MM/YYYY

// Algoritmo de Luhn
function luhn(number) {
    if (!/^\d{13,19}$/.test(number))
        return false;
    let sum = 0;
    let double = false;
    for (let i = number.length - 1; i >= 0; i--) {
        let digit = parseInt(number[i], 10);
        if (double) {
            digit *= 2;
            if (digit > 9)
                digit -= 9;
        }
        sum += digit;
        double = !double;
    }
    return sum % 10 === 0;
}

const esTextoVacio = (v) => typeof v !== "string" || v.trim() === "";

class PhoneNumber {
    constructor(number) {
        this.number = number;
    }

    isValid() {
        return typeof this.number === "string" && VALIDAR_TELEFONO.test(this.number);
    }

    // Convierte "5551234567" -> "(555) 123-4567"
    getFormatted() {
        const match = String(this.number).match(/^(\d{3})(\d{3})(\d{4})$/);
        return match ? `(${match[1]}) ${match[2]}-${match[3]}` : this.number;
    }
}

class Address {
    constructor(street, city, state, zip) {
        this.street = street;
        this.city = city;
        this.state = state;
        this.zip = zip;
    }

    validate() {
        const errors = [];
        if (esTextoVacio(this.street))
            errors.push("Calle inválida");
        if (esTextoVacio(this.city))
            errors.push("Ciudad inválida");
        if (typeof this.state !== "string" || !VALIDAR_ESTADO.test(this.state))
            errors.push("Estado inválido");
        if (typeof this.zip !== "string" || !VALIDAR_ZIP.test(this.zip))
            errors.push("Código postal inválido");
        return errors;
    }
}

class CreditCard {
    constructor(number, expiration, cvv) {
        this.number = number;
        this.expiration = expiration;
        this.cvv = cvv;
    }

    // now se puede inyectar para que los tests no dependan de la fecha actual
    validate(now = new Date()) {
        const errors = [];

        if (typeof this.number !== "string" || !luhn(this.number))
            errors.push("Número de tarjeta de crédito inválido");

        const match =
            typeof this.expiration === "string"
                ? this.expiration.match(VALIDAR_EXPIRACION)
                : null;
        if (!match)
            errors.push("Formato de fecha de vencimiento inválido");
        else {
            const month = parseInt(match[1], 10);
            const year = parseInt(match[2], 10);
            // La tarjeta vale hasta el último día del mes de expiración
            const finMes = new Date(year, month, 0, 23, 59, 59);
            if (finMes < now)
                errors.push("Tarjeta de crédito vencida");
        }

        if (typeof this.cvv !== "string" || !VALIDAR_CVV.test(this.cvv))
            errors.push("CVV inválido");

        return errors;
    }
}

class Expected {
    constructor(is_valid, errors) {
        this.is_valid = is_valid;
        this.errors = errors;
    }
}

class Customer {
    constructor(email, phone, billingAddress, creditCard) {
        this.email = email;
        this.phone = phone; // PhoneNumber
        this.billingAddress = billingAddress; // Address
        this.creditCard = creditCard; // CreditCard
    }

    // Construye un Customer desde el objeto del JSON (snake_case)
    static fromJSON(data = {}) {
        const a = data.billing_address || {};
        const c = data.credit_card || {};
        return new Customer(
            data.email,
            new PhoneNumber(data.phone),
            new Address(a.street, a.city, a.state, a.zip),
            new CreditCard(c.number, c.expiration, c.cvv),
        );
    }

    validate(now = new Date()) {
        const errors = [];

        if (typeof this.email !== "string" || !VALIDAR_EMAIL.test(this.email))
            errors.push("Formato de correo electrónico inválido");

        if (!this.phone.isValid())
            errors.push("Formato de teléfono inválido");

        errors.push(...this.billingAddress.validate());
        errors.push(...this.creditCard.validate(now));

        return new Expected(errors.length === 0, errors);
    }
}

module.exports = { Customer, PhoneNumber, Address, CreditCard, Expected, luhn };