## 1. Add Single Item to Empty Cart

**Test Case ID**: TC_CART_001  
**Title**: Add a single item to an empty shopping cart  
**Priority**: High  
**Type**: Positive  

**Description**:  
Validates that a user can successfully add one item to an empty cart and that the cart updates correctly.

**Preconditions**:

- User has access to the shopping cart.
- Shopping cart is empty.
- The selected product is available for purchase.

**Test Steps**:

1. Open the shopping page.
2. Select a product with a known price.
3. Click the "Add to Cart" button.
4. Open or view the shopping cart.
5. Verify the cart contents and available buttons.

**Test Data**:

- Product: Product A
- Quantity: 1
- Unit Price: $100.00

**Expected Result**:

- Product A is added successfully to the cart.
- The cart contains exactly 1 item.
- Product quantity is displayed as 1.
- Total price is displayed as $100.00.
- The "Checkout" button is enabled.
- The "Clear Cart" button is available.

**Status**: (To be filled during execution)  
**Notes**: Verify that no duplicate or unexpected items appear in the cart.

---

## 2. Add Maximum Number of Items

**Test Case ID**: TC_CART_002  
**Title**: Add the maximum allowed 10 items to the cart  
**Priority**: High  
**Type**: Positive  

**Description**:  
Validates that the shopping cart allows users to add up to the maximum limit of 10 different items and correctly calculates the total price.

**Preconditions**:

- User has access to the shopping cart.
- Shopping cart is empty.
- At least 10 different products are available.

**Test Steps**:

1. Open the shopping page.
2. Add 10 different products to the cart, one at a time.
3. Open the shopping cart.
4. Verify that all 10 products are displayed.
5. Verify the calculated total price.
6. Verify the state of the "Checkout" button.

**Test Data**:

- Number of different products: 10
- Quantity per product: 1
- Example unit price per product: $10.00
- Expected total: $100.00

**Expected Result**:

- All 10 products are successfully added.
- The cart contains exactly 10 different items.
- Each product has a quantity of 1.
- The total price equals the sum of all 10 products.
- The "Checkout" button is enabled.
- The cart remains functional at the maximum item limit.

**Status**: (To be filled during execution)  
**Notes**: Use unique products to ensure the test validates the 10-item cart limit rather than item quantity.

---

## 3. Try to Add an 11th Item

**Test Case ID**: TC_CART_003  
**Title**: Prevent adding an 11th item to the cart  
**Priority**: Critical  
**Type**: Negative  

**Description**:  
Validates that the shopping cart prevents users from exceeding the maximum limit of 10 different items.

**Preconditions**:

- User has access to the shopping cart.
- The cart already contains 10 different items.
- An additional product is available.

**Test Steps**:

1. Verify that the cart contains exactly 10 different items.
2. Return to the shopping page.
3. Select an 11th different product.
4. Click the "Add to Cart" button.
5. Open or review the shopping cart.

**Test Data**:

- Current number of items: 10
- Additional product: Product K
- Quantity requested: 1

**Expected Result**:

- The 11th product is not added to the cart.
- The cart continues to contain exactly 10 different items.
- The existing cart contents are not modified.
- The total price remains unchanged.
- The application displays an appropriate warning or prevents the add operation.
- The "Checkout" button remains enabled.

**Status**: (To be filled during execution)  
**Notes**: The exact warning message may depend on the application design.

---

## 4. Update Item Quantity to Maximum

**Test Case ID**: TC_CART_004  
**Title**: Update an item's quantity to the maximum allowed value of 99  
**Priority**: High  
**Type**: Positive  

**Description**:  
Validates that the quantity of an item can be updated to the maximum permitted quantity of 99 and that the total price is recalculated correctly.

**Preconditions**:

- User has access to the shopping cart.
- The cart contains at least one product.
- The product quantity can be modified.

**Test Steps**:

1. Open the shopping cart.
2. Select an existing product.
3. Change its quantity to 99.
4. Apply or confirm the quantity change.
5. Verify the displayed quantity and total price.

**Test Data**:

- Product: Product A
- Unit Price: $10.00
- New Quantity: 99
- Expected subtotal: $990.00

**Expected Result**:

- The quantity is successfully updated to 99.
- The displayed quantity is 99.
- The product subtotal is recalculated to $990.00.
- The cart total is updated correctly.
- The "Checkout" button remains enabled.

**Status**: (To be filled during execution)  
**Notes**: Quantity 99 is a valid boundary value and should be accepted.

---

## 5. Try to Set Quantity to Zero or Negative

**Test Case ID**: TC_CART_005  
**Title**: Reject zero or negative item quantities  
**Priority**: Critical  
**Type**: Negative  

**Description**:  
Validates that the shopping cart does not allow an item's quantity to be set below the minimum permitted value of 1.

**Preconditions**:

- User has access to the shopping cart.
- The cart contains at least one product.
- The product currently has a valid quantity.

**Test Steps**:

1. Open the shopping cart.
2. Select an existing product.
3. Enter a quantity of 0.
4. Attempt to apply the change.
5. Verify that the invalid value is rejected.
6. Enter a negative quantity such as -1.
7. Attempt to apply the change.
8. Verify the cart contents and total price.

**Test Data**:

- Product: Product A
- Current Quantity: 1
- Invalid Quantity 1: 0
- Invalid Quantity 2: -1

**Expected Result**:

- Quantity 0 is rejected.
- Quantity -1 is rejected.
- The item quantity is not updated to an invalid value.
- The quantity remains at the previous valid value or the system requests a valid value.
- The cart total is not incorrectly modified.
- An appropriate validation message may be displayed.

**Status**: (To be filled during execution)  
**Notes**: Both 0 and negative values validate the lower boundary rule of 1 item minimum.

---

## 6. Clear Cart With Multiple Items

**Test Case ID**: TC_CART_006  
**Title**: Clear a shopping cart containing multiple items  
**Priority**: High  
**Type**: Positive  

**Description**:  
Validates that the "Clear Cart" button removes all products from the shopping cart and resets the cart state correctly.

**Preconditions**:

- User has access to the shopping cart.
- The cart contains multiple products.
- The "Clear Cart" button is available.

**Test Steps**:

1. Add at least 3 different products to the shopping cart.
2. Open the shopping cart.
3. Verify that the products and total price are displayed.
4. Click the "Clear Cart" button.
5. Confirm the action if a confirmation message is displayed.
6. Verify the cart state after clearing.

**Test Data**:

- Product A: Quantity 1, Price $20.00
- Product B: Quantity 2, Price $15.00 each
- Product C: Quantity 1, Price $50.00
- Total before clearing: $100.00

**Expected Result**:

- All products are removed from the cart.
- The cart contains 0 items.
- The total price is reset to $0.00.
- The "Checkout" button is disabled.
- No previously added products remain in the cart.
- The cart is ready to accept new products.

**Status**: (To be filled during execution)  
**Notes**: If the application uses a confirmation dialog, verify that confirming the action clears the cart successfully.