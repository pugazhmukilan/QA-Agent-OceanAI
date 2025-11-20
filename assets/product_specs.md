# Product Specifications – E-Shop Checkout

## 1. Discount Code Rules
- The discount code **SAVE15** applies a **15% discount** on cart total.
- Discount can only be applied **once per checkout**.
- Invalid codes must display an inline error message.

## 2. Shipping Rules
- **Standard Shipping**: Free
- **Express Shipping**: Costs **$10**

## 3. Payment Rules
- Supported methods:
  - Credit Card
  - PayPal
- Payment must only process if:
  - All required fields are filled
  - Email is valid
  - Address length ≥ 5 characters

## 4. Cart Behavior
- Users may add multiple items.
- No maximum cart limit.
- Total must update after:
  - Adding items
  - Applying discount
  - Choosing shipping method

## 5. Success Message
- After successful validation, show:
  **“Payment Successful!”**
