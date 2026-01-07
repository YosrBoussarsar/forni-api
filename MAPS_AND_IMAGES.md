# 🗺️ Viewing Bakeries with Images and Maps

## Quick Start

### 1. Start the API
```bash
python app.py
```

### 2. Open in Browser
Go to: **http://localhost:5000/**

You'll see:
- 🗺️ **Interactive main map** with all bakery locations
- 🏪 **Bakery cards** showing images, details, and individual maps
- 📍 **Clickable markers** with bakery information

---

## Features

### ✅ What's Working

1. **Free Geocoding** (Nominatim/OpenStreetMap)
   - Automatic address → coordinates conversion
   - No API key required
   - Works when creating/updating bakeries

2. **Local Image Storage**
   - Images saved to `/static/uploads/`
   - No cloud costs
   - Supports: PNG, JPG, JPEG, GIF, WebP

3. **Interactive Maps**
   - Main map showing all bakeries
   - Individual maps for each bakery card
   - Uses Leaflet.js + OpenStreetMap (free)

---

## How to Use

### Create a Bakery (Auto-Geocodes)

When you create a bakery with an address, coordinates are automatically fetched:

```bash
POST /bakery
{
  "name": "My Bakery",
  "address": "Eiffel Tower",
  "city": "Paris",
  "governorate": "France",
  "description": "Fresh pastries"
}
```

The API will:
1. Contact Nominatim API
2. Get latitude/longitude
3. Store in database
4. Display on maps automatically

### Upload an Image

```bash
POST /bakery/{id}/upload-image
Content-Type: multipart/form-data

Form field: image (file)
```

The image will:
1. Save to `/static/uploads/bakeries/`
2. Return URL path
3. Display on bakery card

### View on Map

The frontend automatically:
- Loads all bakeries from API
- Shows them on the main map
- Creates individual maps for each
- Displays images if available

---

## Frontend Display

The **index.html** page shows:

```
┌─────────────────────────────────────┐
│     🥐 Forni Bakeries              │
├─────────────────────────────────────┤
│                                     │
│  📍 All Bakeries Map                │
│  ┌───────────────────────────────┐ │
│  │  Interactive OpenStreetMap    │ │
│  │  with bakery markers          │ │
│  └───────────────────────────────┘ │
│                                     │
│  🏪 Bakery Directory                │
│  ┌──────────┐  ┌──────────┐       │
│  │ [Image]  │  │ [Image]  │       │
│  │ Name     │  │ Name     │       │
│  │ Rating ⭐│  │ Rating ⭐│       │
│  │ Location │  │ Location │       │
│  │ [Map]    │  │ [Map]    │       │
│  └──────────┘  └──────────┘       │
└─────────────────────────────────────┘
```

---

## API Endpoints

### Bakeries
- `GET /bakery` - List all bakeries (with images & coordinates)
- `POST /bakery` - Create bakery (auto-geocodes address)
- `PUT /bakery/{id}` - Update bakery (re-geocodes if address changes)
- `POST /bakery/{id}/upload-image` - Upload bakery image

### Products
- `POST /product/{id}/upload-image` - Upload product image

### Surplus Bags
- `POST /surplus_bag/{id}/upload-image` - Upload surplus bag image

### Location-Based
- `GET /bakery/nearby?lat={lat}&lng={lng}&radius={km}` - Find nearby bakeries

---

## Example Response

```json
{
  "id": 1,
  "name": "Paris Bakery",
  "description": "French pastries",
  "address": "Eiffel Tower",
  "city": "Paris",
  "governorate": "France",
  "latitude": 48.8584,
  "longitude": 2.2945,
  "image_url": "/static/uploads/bakeries/abc123.jpg",
  "rating": 4.5,
  "review_count": 10
}
```

---

## Files Created

1. **static/index.html** - Interactive frontend with maps
2. **utils/geocoding.py** - Free Nominatim geocoding
3. **utils/image_upload.py** - Local image storage
4. **static/uploads/** - Image storage folders

---

## Why You See Maps & Images

### Maps Appear When:
✅ Bakery has `latitude` and `longitude` values
✅ Either auto-geocoded from address
✅ Or manually provided in API request

### Images Appear When:
✅ Image uploaded via `/bakery/{id}/upload-image`
✅ Image stored in `/static/uploads/bakeries/`
✅ `image_url` field populated in database

### If Missing:
❌ No coordinates → "⚠️ No location data" message
❌ No image → Colored placeholder with bakery initial

---

## Technology Stack

- **Maps**: Leaflet.js + OpenStreetMap tiles
- **Geocoding**: Nominatim (OpenStreetMap)
- **Storage**: Local filesystem
- **Frontend**: Vanilla JavaScript + HTML/CSS

**Total Cost: $0** (Everything is free!)

---

## Next Steps

1. Create bakeries with addresses → See them on map
2. Upload images → See them in cards
3. Test nearby search → Find bakeries by distance
4. Integrate with your frontend app

Enjoy! 🥖✨
