# Database Migration Guide

## Step 1: Run the Database Migration

Since you've added new columns to the database, you need to migrate the database.

### Option A: Using Flask-Migrate (Recommended)

```powershell
# Initialize migrations (only if not already initialized)
flask db init

# Create a migration script
flask db migrate -m "Add tags to products and surplus bags"

# Apply the migration
flask db upgrade
```

### Option B: Re-seed the Database

If you're in development and don't mind losing existing data:

```powershell
# Run the seed script to recreate the database with tags
python seed.py
```

## Step 2: Test the Tagging Feature

### Test 1: Find Bakeries with Croissants
```bash
GET http://localhost:5000/bakery?product_tags=croissant
```

### Test 2: Find Sweet Surprise Bags
```bash
GET http://localhost:5000/surplus_bag?tags=sweet
```

### Test 3: Find Savory Surprise Bags
```bash
GET http://localhost:5000/surplus_bag?tags=savory
```

### Test 4: Find Products with Bread Tag
```bash
GET http://localhost:5000/product?tags=bread
```

### Test 5: Find Multiple Tags (OR logic)
```bash
GET http://localhost:5000/product?tags=croissant,chocolate
```

## Step 3: Verify the Changes

1. Check that products have tags in the response
2. Check that surplus bags have tags in the response
3. Verify filtering works correctly

## Example API Responses

### Product with Tags
```json
{
  "id": 1,
  "name": "Croissant",
  "price": 2.5,
  "tags": "croissant,pastry,breakfast,french",
  "bakery_id": 1,
  ...
}
```

### Surplus Bag with Tags
```json
{
  "id": 1,
  "title": "Morning Pastry Mix",
  "tags": "sweet,pastry,breakfast,french",
  "sale_price": 5.0,
  ...
}
```
