# Database Migration Guide - Order Items Support

## What Changed

The order system has been updated to support:
- **Products**: Individual products from bakeries
- **Surplus Bags**: Surprise bags with discounted items
- **Mixed Orders**: Combinations of both products and surplus bags in a single order

## New Database Schema

### New Table: `order_items`
- Links orders to products or surplus bags
- Supports quantity and pricing per item
- Enables orders with multiple items

### Updated Table: `orders`
- Added `pickup_time` field
- Added `payment_intent_id` field
- `surplus_bag_id` is now optional (kept for backward compatibility)
- New relationship: `order_items`

## Migration Steps

**⚠️ IMPORTANT: This will delete your existing database and all data!**

1. **Stop the Flask server** (if running)

2. **Run the recreation script:**
   ```powershell
   C:/Users/lenovo/forni-api/venv/Scripts/python.exe recreate_db.py
   ```

3. **Seed the database (optional):**
   ```powershell
   C:/Users/lenovo/forni-api/venv/Scripts/python.exe seed.py
   ```

4. **Restart the Flask server:**
   ```powershell
   C:/Users/lenovo/forni-api/venv/Scripts/python.exe app.py
   ```

## New API Format

### Create Order - New Format

**Endpoint:** `POST /order`

**Old Format (still supported for single surplus bag):**
```json
{
  "surplus_bag_id": 1
}
```

**New Format (recommended):**
```json
{
  "bakery_id": 1,
  "items": [
    {
      "product_id": 5,
      "quantity": 2
    },
    {
      "surplus_bag_id": 3,
      "quantity": 1
    }
  ],
  "pickup_time": "2026-01-04T23:41:02.584Z",
  "payment_intent_id": "mock_pi_12345"
}
```

### Response includes order_items:
```json
{
  "id": 1,
  "status": "pending",
  "total_price": 25.50,
  "bakery_id": 1,
  "order_items": [
    {
      "id": 1,
      "product_id": 5,
      "quantity": 2,
      "unit_price": 8.50,
      "subtotal": 17.00,
      "product": {
        "id": 5,
        "name": "Pain au Chocolat",
        ...
      }
    },
    {
      "id": 2,
      "surplus_bag_id": 3,
      "quantity": 1,
      "unit_price": 8.50,
      "subtotal": 8.50,
      "surplus_bag": {
        "id": 3,
        "title": "Surprise Pastry Bag",
        ...
      }
    }
  ],
  ...
}
```

## Frontend Update Required

Your frontend needs to send the new format:

```javascript
const orderData = {
  bakery_id: bakeryId,
  items: cartItems.map(item => ({
    product_id: item.product_id || undefined,
    surplus_bag_id: item.surplus_bag_id || undefined,
    quantity: item.quantity
  })),
  pickup_time: pickupTime,
  payment_intent_id: paymentIntentId
};

await fetch('http://localhost:5000/order', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(orderData)
});
```
