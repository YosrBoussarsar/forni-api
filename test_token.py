"""
Test script to verify JWT token generation and validation
"""
import requests
import json

API_BASE = "http://localhost:5000"

def test_login_and_create_bakery():
    print("=" * 70)
    print("Testing Login and Bakery Creation")
    print("=" * 70)
    
    # Step 1: Login
    print("\n1. Logging in as bakery owner...")
    login_response = requests.post(f"{API_BASE}/login", json={
        "email": "owner@forni.tn",
        "password": "Owner123!"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    login_data = login_response.json()
    token = login_data.get("access_token")
    
    print(f"✅ Login successful")
    print(f"Token (first 50 chars): {token[:50]}...")
    print(f"Token length: {len(token)}")
    print(f"Token segments (should be 3): {len(token.split('.'))}")
    
    # Step 2: Create bakery
    print("\n2. Creating bakery...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    bakery_data = {
        "name": "Test Bakery",
        "description": "Test description",
        "address": "123 Test St",
        "city": "Tunis"
    }
    
    create_response = requests.post(
        f"{API_BASE}/bakery",
        headers=headers,
        json=bakery_data
    )
    
    print(f"\nResponse Status: {create_response.status_code}")
    
    if create_response.status_code == 201:
        print(f"✅ Bakery created successfully!")
        print(f"Response: {json.dumps(create_response.json(), indent=2)}")
    else:
        print(f"❌ Failed to create bakery")
        print(f"Response: {create_response.text}")
        try:
            print(f"Response JSON: {json.dumps(create_response.json(), indent=2)}")
        except:
            pass
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        test_login_and_create_bakery()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
