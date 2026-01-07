# Image Upload & Geocoding Guide

## 🆓 Free Features Implemented

### 1. **Local Image Storage** (No Cloud Costs)
- Images stored in `/static/uploads/` folder
- Supports: PNG, JPG, JPEG, GIF, WebP
- Automatic cleanup when images are replaced

### 2. **Nominatim Geocoding** (OpenStreetMap - Free)
- Automatic address → coordinates conversion
- No API key required
- Respects usage limits (max 1 request/second)

---

## 📸 Image Upload Endpoints

### Upload Bakery Image
```bash
POST /bakery/{bakery_id}/upload-image
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- image: (file)
```

**Example with cURL:**
```bash
curl -X POST http://localhost:5000/bakery/1/upload-image \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@/path/to/bakery-photo.jpg"
```

**Response:**
```json
{
  "message": "Image uploaded successfully",
  "image_url": "/static/uploads/bakeries/abc123.jpg"
}
```

### Upload Product Image
```bash
POST /product/{product_id}/upload-image
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- image: (file)
```

### Upload Surplus Bag Image
```bash
POST /surplus_bag/{surplus_bag_id}/upload-image
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- image: (file)
```

---

## 🌍 Auto-Geocoding

### Automatic Geocoding on Bakery Creation
When you create a bakery with an address, coordinates are automatically fetched:

```bash
POST /bakery
Authorization: Bearer <token>

{
  "name": "My Bakery",
  "address": "123 Main St",
  "city": "Cairo",
  "governorate": "Cairo Governorate",
  "description": "Best bread in town"
}
```

The API will automatically:
1. Call Nominatim API with the address
2. Get latitude/longitude
3. Store coordinates in the database

**Response includes:**
```json
{
  "id": 1,
  "name": "My Bakery",
  "address": "123 Main St",
  "city": "Cairo",
  "governorate": "Cairo Governorate",
  "latitude": 30.0444,
  "longitude": 31.2357,
  ...
}
```

### Manual Coordinates (Optional)
You can also provide coordinates manually:

```bash
POST /bakery

{
  "name": "My Bakery",
  "address": "123 Main St",
  "latitude": 30.0444,
  "longitude": 31.2357
}
```

### Update Address → Auto Re-geocode
When updating address fields without providing new coordinates:

```bash
PUT /bakery/{bakery_id}

{
  "address": "456 New Street",
  "city": "Alexandria"
}
```

The API will automatically fetch new coordinates.

---

## 🔍 Find Nearby Bakeries (Using Coordinates)

```bash
GET /bakery/nearby?lat=30.0444&lng=31.2357&radius=5

# Find bakeries within 5km of coordinates
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Nearby Bakery",
    "latitude": 30.0450,
    "longitude": 31.2360,
    "distance_km": 1.2
  }
]
```

---

## 📁 File Structure

```
forni-api/
├── static/
│   └── uploads/
│       ├── bakeries/      # Bakery images
│       ├── products/      # Product images
│       └── surplus_bags/  # Surplus bag images
├── utils/
│   ├── geocoding.py       # Nominatim integration
│   └── image_upload.py    # Local file storage
```

---

## ⚙️ Configuration

### Image Storage Settings (in utils/image_upload.py)

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# Change to add more formats
```

### Geocoding Service (in utils/geocoding.py)

**Important:** Nominatim has usage limits:
- Max 1 request per second
- Must include User-Agent header
- Free for fair use

Current User-Agent: `Forni-API/1.0`

---

## 🖼️ Accessing Images

Images are served at:
```
http://localhost:5000/static/uploads/{folder}/{filename}
```

Examples:
- `http://localhost:5000/static/uploads/bakeries/abc123.jpg`
- `http://localhost:5000/static/uploads/products/def456.png`
- `http://localhost:5000/static/uploads/surplus_bags/ghi789.jpg`

---

## 🛡️ Security & Permissions

### Who Can Upload Images?
- **Bakery Images**: Bakery owner or admin
- **Product Images**: Bakery owner (of that product) or admin
- **Surplus Bag Images**: Bakery owner (of that bag) or admin

### File Validation
- File extension check
- No file size limit (add if needed)
- Unique filenames (UUID-based)
- Old images auto-deleted on replacement

---

## 📱 Frontend Integration Example

### React/JavaScript Image Upload

```javascript
const uploadBakeryImage = async (bakeryId, imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await fetch(`http://localhost:5000/bakery/${bakeryId}/upload-image`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });

  const data = await response.json();
  return data.image_url; // Use this to display the image
};
```

### Display Image
```html
<img src="http://localhost:5000{{image_url}}" alt="Bakery" />
```

---

## 🚀 Testing

### 1. Create a bakery with auto-geocoding:
```bash
POST /bakery
{
  "name": "Test Bakery",
  "address": "Times Square",
  "city": "New York",
  "governorate": "New York"
}
```

### 2. Upload an image:
```bash
POST /bakery/1/upload-image
Form: image=@photo.jpg
```

### 3. Check the result:
```bash
GET /bakery/1
```

Response should include:
```json
{
  "image_url": "/static/uploads/bakeries/xxx.jpg",
  "latitude": 40.758896,
  "longitude": -73.985130
}
```

---

## 💡 Tips

1. **Geocoding Accuracy**: More detailed addresses = better coordinates
2. **Image Optimization**: Compress images before upload to save disk space
3. **Backup**: Backup `/static/uploads/` folder regularly
4. **Production**: Use nginx to serve static files for better performance

---

## 🔧 Troubleshooting

### Geocoding Not Working?
- Check internet connection
- Nominatim might be rate-limited (1 req/sec max)
- Address might be too vague

### Image Upload Failing?
- Check file format (png, jpg, jpeg, gif, webp only)
- Verify JWT token is valid
- Check user permissions (owner or admin)

### Images Not Displaying?
- Verify path starts with `/static/uploads/`
- Check if file exists in folder
- Ensure server is serving static files correctly
