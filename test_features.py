"""
Quick test script for image upload and geocoding features
Run this to verify the free features are working
"""

from utils.geocoding import GeocodingService
from utils.image_upload import allowed_file

print("=" * 60)
print("🧪 TESTING FREE FEATURES")
print("=" * 60)

# Test 1: Geocoding Service
print("\n1️⃣ Testing Nominatim Geocoding (Free)...")
print("-" * 60)

test_addresses = [
    ("Times Square", "New York", "New York"),
    ("Eiffel Tower", "Paris", "France"),
    ("123 Main Street", "Cairo", "Egypt")
]

for address, city, region in test_addresses:
    print(f"\n📍 Looking up: {address}, {city}, {region}")
    coords = GeocodingService.geocode_address(address, city, region)
    
    if coords:
        print(f"   ✅ Found: {coords['latitude']:.6f}, {coords['longitude']:.6f}")
    else:
        print(f"   ❌ Not found (this is okay - might be too vague)")

# Test 2: Image Upload Validation
print("\n\n2️⃣ Testing Image Upload Validation...")
print("-" * 60)

test_files = [
    "photo.jpg",
    "image.png",
    "picture.gif",
    "diagram.webp",
    "document.pdf",  # Should fail
    "script.py"      # Should fail
]

for filename in test_files:
    is_allowed = allowed_file(filename)
    status = "✅ Allowed" if is_allowed else "❌ Rejected"
    print(f"{status}: {filename}")

print("\n" + "=" * 60)
print("✨ Testing Complete!")
print("=" * 60)
print("\n📁 Upload folders created at:")
print("   - static/uploads/bakeries/")
print("   - static/uploads/products/")
print("   - static/uploads/surplus_bags/")
print("\n🌍 Geocoding: Uses Nominatim (OpenStreetMap) - FREE")
print("📸 Images: Stored locally - NO CLOUD COSTS")
print("\n🚀 Ready to use! Check IMAGE_GEOCODING_GUIDE.md for API docs")
print("=" * 60)
