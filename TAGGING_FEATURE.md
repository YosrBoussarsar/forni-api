# Tagging and Filtering Feature

## Overview
This feature adds a tagging system to products and surplus bags, allowing users to filter and search by tags.

## Changes Made

### 1. Database Models

#### Product Model ([models/product.py](models/product.py))
- Added `tags` field (String, 500 chars) to store comma-separated tags
- Example: `"croissant,pastry,breakfast"`

#### Surplus Bag Model ([models/surplus_bag.py](models/surplus_bag.py))
- Added `tags` field (String, 500 chars) to store comma-separated tags
- Example: `"sweet,savory,vegan"`

### 2. Schemas ([schemas.py](schemas.py))
Updated all product and surplus bag schemas to include the `tags` field:
- `PlainProductSchema`
- `ProductCreateSchema`
- `ProductUpdateSchema`
- `PlainSurplusBagSchema`
- `SurplusBagCreateSchema`
- `SurplusBagUpdateSchema`

### 3. API Endpoints

#### Products Endpoint ([resources/products.py](resources/products.py))
- **GET /product** - Added optional `tags` query parameter
- Usage: `/product?tags=croissant,pastry`
- Returns products that have ANY of the specified tags

#### Surplus Bags Endpoint ([resources/surplus_bags.py](resources/surplus_bags.py))
- **GET /surplus_bag** - Added optional `tags` query parameter
- Usage: `/surplus_bag?tags=sweet,savory`
- Returns surplus bags that have ANY of the specified tags

#### Bakeries Endpoint ([resources/bakeries.py](resources/bakeries.py))
- **GET /bakery** - Added optional `product_tags` query parameter
- Usage: `/bakery?product_tags=croissant,bread`
- Returns bakeries that sell products with ANY of the specified tags

## Database Migration

To apply the changes to your database, run:

```powershell
# Initialize migrations (only if not already done)
flask db init

# Create a migration for the new tags columns
flask db migrate -m "Add tags to products and surplus bags"

# Apply the migration
flask db upgrade
```

## Usage Examples

### 1. Creating a Product with Tags
```json
POST /product
{
  "bakery_id": 1,
  "name": "Croissant",
  "price": 3.50,
  "tags": "croissant,pastry,breakfast,french"
}
```

### 2. Creating a Surplus Bag with Tags
```json
POST /surplus_bag
{
  "bakery_id": 1,
  "title": "Sweet Pastries Mix",
  "sale_price": 5.00,
  "original_value": 15.00,
  "quantity_available": 10,
  "tags": "sweet,pastry,dessert",
  "pickup_start": "2026-01-04T16:00:00",
  "pickup_end": "2026-01-04T20:00:00"
}
```

### 3. Searching Products by Tags
```bash
# Find all products tagged with "croissant"
GET /product?tags=croissant

# Find all products tagged with either "croissant" OR "pastry"
GET /product?tags=croissant,pastry
```

### 4. Searching Surplus Bags by Tags
```bash
# Find all surplus bags with sweet items
GET /surplus_bag?tags=sweet

# Find all surplus bags with sweet OR savory items
GET /surplus_bag?tags=sweet,savory
```

### 5. Finding Bakeries by Product Tags
```bash
# Find all bakeries that sell croissants
GET /bakery?product_tags=croissant

# Find all bakeries that sell bread OR pastries
GET /bakery?product_tags=bread,pastry
```

## Tag Suggestions

### Product Tags
- **Bread Types**: `baguette`, `sourdough`, `whole-wheat`, `multigrain`, `rye`
- **Pastries**: `croissant`, `danish`, `eclair`, `macaron`, `tart`
- **Cakes**: `chocolate-cake`, `vanilla-cake`, `cheesecake`, `layer-cake`
- **Cookies**: `chocolate-chip`, `oatmeal`, `sugar-cookie`
- **Dietary**: `vegan`, `gluten-free`, `dairy-free`, `sugar-free`, `organic`
- **Occasions**: `breakfast`, `dessert`, `party`, `wedding`, `birthday`
- **Flavors**: `chocolate`, `vanilla`, `strawberry`, `lemon`, `caramel`

### Surplus Bag Tags
- **Category**: `sweet`, `savory`, `mixed`
- **Meal Time**: `breakfast`, `lunch`, `dinner`, `snack`
- **Dietary**: `vegan`, `vegetarian`, `gluten-free`, `dairy-free`
- **Type**: `pastry`, `bread`, `cake`, `cookies`, `sandwiches`

## Implementation Notes

1. **Case-Insensitive Search**: All tag searches are case-insensitive
2. **OR Logic**: When multiple tags are provided, items matching ANY tag are returned
3. **Partial Matching**: Tags must match exactly (not partial word matching)
4. **Comma-Separated**: Tags in the database and search queries use comma separation
5. **Whitespace Handling**: Leading/trailing spaces are automatically trimmed

## Testing

After migration, you can test the feature by:
1. Adding tags to existing products via PUT requests
2. Creating new products/bags with tags
3. Testing the filter endpoints with various tag combinations
4. Verifying bakery filtering works correctly
