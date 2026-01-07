"""
Demo script to create sample bakeries with images and locations
This demonstrates the image upload and geocoding features
"""
import requests
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

API_BASE = "http://localhost:5000"

# Sample bakery data with real-world locations
SAMPLE_BAKERIES = [
    {
        "name": "Paris Boulangerie",
        "description": "Authentic French bakery with fresh croissants daily",
        "address": "Champs-Élysées",
        "city": "Paris",
        "governorate": "Île-de-France",
        "specialties": "Croissants, Baguettes"
    },
    {
        "name": "Cairo Sweet House",
        "description": "Traditional Egyptian pastries and desserts",
        "address": "Tahrir Square",
        "city": "Cairo",
        "governorate": "Cairo",
        "specialties": "Baklava, Kunafa"
    },
    {
        "name": "New York Bagel Shop",
        "description": "Fresh bagels and artisan bread",
        "address": "Times Square",
        "city": "New York",
        "governorate": "New York",
        "specialties": "Bagels, Sourdough"
    },
    {
        "name": "London Bakehouse",
        "description": "Classic British baked goods",
        "address": "Piccadilly Circus",
        "city": "London",
        "governorate": "Greater London",
        "specialties": "Scones, Meat Pies"
    },
    {
        "name": "Tokyo Pastry Corner",
        "description": "Japanese-inspired pastries and sweets",
        "address": "Shibuya",
        "city": "Tokyo",
        "governorate": "Tokyo",
        "specialties": "Melon Pan, Anpan"
    }
]

def create_sample_image(bakery_name, color):
    """Create a simple placeholder image for demonstration"""
    # Create a 800x600 image
    img = Image.new('RGB', (800, 600), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 60)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw bakery name
    text = bakery_name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (800 - text_width) // 2
    y = (600 - text_height) // 2
    
    # Draw white text with shadow
    draw.text((x+3, y+3), text, fill=(0, 0, 0), font=font)
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Draw emoji
    emoji = "🥐"
    draw.text((400-30, 150), emoji, font=small_font)
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def register_user(email, password, role="bakery_owner"):
    """Register a new user"""
    response = requests.post(f"{API_BASE}/register", json={
        "email": email,
        "password": password,
        "first_name": "Demo",
        "last_name": "User",
        "role": role
    })
    return response.json()

def login_user(email, password):
    """Login and get JWT token"""
    response = requests.post(f"{API_BASE}/login", json={
        "email": email,
        "password": password
    })
    return response.json().get("access_token")

def create_bakery(token, bakery_data):
    """Create a bakery (will auto-geocode)"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE}/bakery", 
                            json=bakery_data, 
                            headers=headers)
    return response.json()

def upload_bakery_image(token, bakery_id, image_bytes, bakery_name):
    """Upload an image for a bakery"""
    headers = {"Authorization": f"Bearer {token}"}
    files = {'image': (f'{bakery_name}.jpg', image_bytes, 'image/jpeg')}
    response = requests.post(f"{API_BASE}/bakery/{bakery_id}/upload-image",
                            headers=headers,
                            files=files)
    return response.json()

def main():
    print("=" * 70)
    print("🥖 FORNI DEMO: Creating Sample Bakeries with Images & Maps")
    print("=" * 70)
    
    # Check if server is running
    try:
        requests.get(API_BASE)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server!")
        print(f"   Please make sure the Flask app is running on {API_BASE}")
        print("   Run: python app.py")
        return
    
    # Register and login
    print("\n1️⃣ Creating demo user...")
    email = "demo@bakery.com"
    password = "DemoPass123"
    
    try:
        register_user(email, password)
        print(f"   ✅ Registered: {email}")
    except:
        print(f"   ⚠️  User already exists: {email}")
    
    print("\n2️⃣ Logging in...")
    token = login_user(email, password)
    if not token:
        print("   ❌ Login failed!")
        return
    print("   ✅ Logged in successfully")
    
    # Create bakeries with images
    print("\n3️⃣ Creating bakeries with auto-geocoding...")
    colors = [
        (245, 176, 65),   # Orange
        (52, 152, 219),   # Blue
        (46, 204, 113),   # Green
        (155, 89, 182),   # Purple
        (231, 76, 60),    # Red
    ]
    
    created_bakeries = []
    
    for i, bakery_data in enumerate(SAMPLE_BAKERIES):
        print(f"\n   🏪 Creating: {bakery_data['name']}")
        print(f"      Location: {bakery_data['address']}, {bakery_data['city']}")
        
        # Create bakery (auto-geocodes address)
        bakery = create_bakery(token, bakery_data)
        
        if 'id' in bakery:
            bakery_id = bakery['id']
            
            # Check if geocoding worked
            if bakery.get('latitude') and bakery.get('longitude'):
                print(f"      ✅ Geocoded: {bakery['latitude']:.4f}, {bakery['longitude']:.4f}")
            else:
                print(f"      ⚠️  No coordinates (geocoding may have failed)")
            
            # Create and upload image
            print(f"      📸 Uploading sample image...")
            image = create_sample_image(bakery_data['name'], colors[i])
            result = upload_bakery_image(token, bakery_id, image, bakery_data['name'])
            
            if 'image_url' in result:
                print(f"      ✅ Image uploaded: {result['image_url']}")
            else:
                print(f"      ⚠️  Image upload failed")
            
            created_bakeries.append(bakery)
        else:
            print(f"      ❌ Failed to create bakery: {bakery}")
    
    print("\n" + "=" * 70)
    print("✨ DEMO COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Created {len(created_bakeries)} bakeries with images and maps")
    print(f"\n🌐 View them in your browser:")
    print(f"   👉 {API_BASE}/")
    print(f"\n📡 API Endpoints:")
    print(f"   • GET  {API_BASE}/bakery - List all bakeries")
    print(f"   • GET  {API_BASE}/bakery/nearby?lat=48.8566&lng=2.3522&radius=10")
    print(f"   • GET  {API_BASE}/api/docs - Swagger documentation")
    print("=" * 70)

if __name__ == "__main__":
    main()
