class Item {
  /**
   * Represents an item in the shopping cart.
   * @param {string} name - Item name
   * @param {number} price - Item price (must be positive)
   * @param {number} quantity - Number of items (must be positive)
   */
  constructor(name, price, quantity = 1) {
    if (price <= 0) {
      throw new Error("Price must be positive");
    }
    if (quantity <= 0) {
      throw new Error("Quantity must be positive");
    }

    this.name = name;
    this.price = price;
    this.quantity = quantity;
  }

  /**
   * Calculate total cost for this item.
   */
  getTotal() {
    return this.price * this.quantity;
  }
}

class ShoppingCart {
  /**
   * A shopping cart that can hold multiple items.
   */
  constructor() {
    this.items = [];
    this.discountPercent = 0;
  }

  /**
   * Add an item to the cart. If item already exists, increase quantity.
   * @param {Item} item - Item object to add
   */
  addItem(item) {
    // Check if item already exists
    const existing = this.items.find((i) => i.name === item.name);
    if (existing) {
      existing.quantity += item.quantity;
      return;
    }

    // Add new item
    this.items.push(item);
  }

  /**
   * Remove an item from the cart by name.
   * @param {string} itemName - Name of the item to remove
   * @returns {boolean} True if item was removed, false if not found
   */
  removeItem(itemName) {
    const index = this.items.findIndex((item) => item.name === itemName);
    if (index !== -1) {
      this.items.splice(index, 1);
      return true;
    }
    return false;
  }

  /**
   * Calculate subtotal before discount.
   */
  getSubtotal() {
    return this.items.reduce((sum, item) => sum + item.getTotal(), 0);
  }

  /**
   * Apply a discount percentage to the cart.
   * @param {number} percent - Discount percentage (0-100)
   */
  applyDiscount(percent) {
    if (percent < 0 || percent > 100) {
      throw new Error("Discount must be between 0 and 100");
    }
    this.discountPercent = percent;
  }

  /**
   * Calculate total after discount.
   */
  getTotal() {
    const subtotal = this.getSubtotal();
    const discountAmount = subtotal * (this.discountPercent / 100);
    return subtotal - discountAmount;
  }

  /**
   * Remove all items from the cart.
   */
  clear() {
    this.items = [];
    this.discountPercent = 0;
  }

  /**
   * Get total number of items (sum of all quantities).
   */
  getItemCount() {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }

  /**
   * Check if cart is empty.
   */
  isEmpty() {
    return this.items.length === 0;
  }
}

module.exports = { Item, ShoppingCart };
