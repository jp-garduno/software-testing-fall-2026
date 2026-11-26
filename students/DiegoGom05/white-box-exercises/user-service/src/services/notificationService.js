// src/services/notificationService.js
function sendAlert(userEmail, message) {
  // En producción enviaría un correo real
  console.log(`Sending email to ${userEmail}: ${message}`);
  return true;
}

module.exports = { sendAlert };
