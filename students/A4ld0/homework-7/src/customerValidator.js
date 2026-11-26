const states = new Set(
  ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ " +
    "NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split(" ")
);

function isLuhnValid(number) {
  if (typeof number !== "string" || !/^\d{13,19}$/.test(number)) return false;

  let sum = 0;
  for (let index = number.length - 1; index >= 0; index--) {
    let digit = Number(number[index]);
    if ((number.length - index) % 2 === 0) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    sum += digit;
  }
  return sum % 10 === 0;
}

function isExpirationValid(expiration, today) {
  if (typeof expiration !== "string" || !/^(0[1-9]|1[0-2])\/\d{4}$/.test(expiration)) {
    return false;
  }

  const [month, year] = expiration.split("/").map(Number);
  const currentYear = today.getUTCFullYear();
  return year > currentYear || (year === currentYear && month >= today.getUTCMonth() + 1);
}

function matches(value, pattern) {
  return typeof value === "string" && pattern.test(value);
}

function validateCustomer(customer, today = new Date()) {
  const { email, phone, billing_address: address, credit_card: card } = customer ?? {};
  const errors = [];

  if (!matches(email, /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/)) errors.push("Invalid email format");
  if (!matches(phone, /^\(\d{3}\) \d{3}-\d{4}$/)) errors.push("Invalid phone format");
  if (!matches(address?.street, /\S/) || !matches(address?.city, /\S/) ||
      !states.has(address?.state) || !matches(address?.zip, /^\d{5}(?:-\d{4})?$/)) {
    errors.push("Invalid billing address");
  }
  if (!isLuhnValid(card?.number)) errors.push("Invalid credit card number");
  if (!isExpirationValid(card?.expiration, today)) errors.push("Invalid credit card expiration");

  return { is_valid: errors.length === 0, errors };
}

module.exports = { validateCustomer };
