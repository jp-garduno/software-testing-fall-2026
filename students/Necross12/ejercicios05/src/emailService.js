class EmailService {
  /**
   * Simulates an external email service API.
   * @param {string} apiKey - API authentication key
   */
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.sentEmails = []; // For testing purposes
  }

  /**
   * Send an email via external API.
   * @param {string} toAddress - Recipient email address
   * @param {string} subject - Email subject
   * @param {string} body - Email body content
   * @returns {boolean} True if email sent successfully
   * @throws {Error} If API is unreachable or email is invalid
   */
  sendEmail(toAddress, subject, body) {
    if (!this._isValidEmail(toAddress)) {
      throw new Error(`Invalid email address: ${toAddress}`);
    }

    // Simulate API call
    this.sentEmails.push({
      to: toAddress,
      subject: subject,
      body: body,
    });
    return true;
  }

  /**
   * Validate email format.
   * @private
   */
  _isValidEmail(email) {
    return email.includes("@") && email.includes(".");
  }
}

module.exports = EmailService;
