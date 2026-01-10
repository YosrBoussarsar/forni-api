# Product Templates & Recommendations Guide

## Overview
Bakery owners can use product recommendations to quickly add common products (bread, croissants, cakes, etc.) to their bakery without manually entering all the details each time.

## How It Works

### 1. Each Bakery Has Independent Products
- Every bakery creates and owns their own product instances
- Products with the same name (e.g., "Baguette") are separate records
- Each bakery controls their own **price**, **quantity_available**, and **availability**

### 2. Product Recommendations
When creating products, bakery owners can:
- **See recommendations** of products already used by other bakeries
- **Clone a template** to auto-fill common fields (name, description, category, allergens, tags, image)
- **Customize bakery-specific fields** (price, quantity, availability)

---

## API Endpoints

### GET /product/recommendations
Get product suggestions based on popular products from other bakeries.

**Query Parameters:**
- `exclude_bakery_id` (optional): Exclude products from a specific bakery (usually your own)
- `category` (optional): Filter by category

**Response:**
```json
{
  "recommendations": [
    {
      "template_product_id": 5,
      "name": "Baguette",
      "description": "Traditional French bread",
      "category": "Bread",
      "allergens": "Gluten",
      "tags": "bread,french,artisan",
      "image_url": "/static/uploads/products/baguette.jpg",
      "popularity": 12,
      "avg_price": 2.50,
      "categories": ["Bread", "Artisan"]
    },
    ...
  ]
}
```

**Example Usage:**
```javascript
// Get recommendations excluding my bakery's products
fetch('/product/recommendations?exclude_bakery_id=3', {
  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
})
```

---

### POST /product/from-template/{template_product_id}
Create a product for your bakery based on an existing product template.

**URL Parameter:**
- `template_product_id`: ID of the product to use as template

**Request Body:**
```json
{
  "bakery_id": 3,
  "price": 2.99,
  "quantity_available": 50,
  "is_available": true
}
```

**Response:**
Returns the newly created `ProductSchema` for your bakery.

**Example Usage:**
```javascript
// Clone product ID 5 (Baguette) for my bakery
fetch('/product/from-template/5', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    bakery_id: 3,
    price: 2.99,
    quantity_available: 50,
    is_available: true
  })
})
```

---

## Frontend Implementation Guide

### Step 1: Show Recommendations
```javascript
// When user clicks "Add Product" button
async function showProductRecommendations(bakeryId) {
  const response = await fetch(
    `/product/recommendations?exclude_bakery_id=${bakeryId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  const data = await response.json();
  
  // Display recommendations in UI
  displayRecommendations(data.recommendations);
}
```

### Step 2: Create Product from Template
```javascript
async function addProductFromTemplate(templateId, bakeryId) {
  // Show form to set bakery-specific fields
  const price = prompt("Enter your price:");
  const quantity = prompt("Enter quantity available:");
  
  const response = await fetch(`/product/from-template/${templateId}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      bakery_id: bakeryId,
      price: parseFloat(price),
      quantity_available: parseInt(quantity),
      is_available: true
    })
  });
  
  if (response.ok) {
    alert("Product added successfully!");
    refreshProductList();
  }
}
```

### Step 3: Create Custom Product
```javascript
// User can also create completely custom products
async function createCustomProduct(data) {
  const response = await fetch('/product', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}
```

---

## UI/UX Recommendations

### Product Creation Flow

1. **Show Two Options:**
   ```
   [Use Product Template]  [Create Custom Product]
   ```

2. **Template Selection:**
   - Display recommendations grid with:
     - Product name and image
     - Category and popularity
     - Average price (as reference)
     - "Add" button
   
3. **Customize Template:**
   When user clicks "Add" on a template:
   - Show pre-filled form with:
     - Name, description, category, allergens, tags (read-only or editable)
     - **Price** (required, can use avg_price as placeholder)
     - **Quantity Available** (required)
     - **Is Available** (checkbox, default: true)

4. **Create Custom:**
   - Show empty form for completely new products

---

## Benefits

✅ **Faster Product Creation** - Clone common products with one click
✅ **Consistency** - Same product names/descriptions across bakeries  
✅ **Independence** - Each bakery controls their own pricing and inventory
✅ **Discovery** - See what products other bakeries offer
✅ **Flexibility** - Can still create completely custom products

---

## Example Workflow

1. Bakery owner creates their bakery
2. Goes to "Manage Products" page
3. Clicks "Add Product"
4. Sees recommendations: "Baguette (used by 12 bakeries)", "Croissant (used by 18 bakeries)"
5. Clicks "Add" on "Baguette"
6. Form auto-fills: name="Baguette", description="Traditional French bread", category="Bread"
7. Owner sets their price: 2.99 TND
8. Owner sets quantity: 50
9. Clicks "Save"
10. Product is created for their bakery with their specific pricing and inventory
