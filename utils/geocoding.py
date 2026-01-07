"""
Free geocoding utility using Nominatim (OpenStreetMap)
No API key required - completely free to use
"""
import requests
from time import sleep

class GeocodingService:
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    @staticmethod
    def geocode_address(address, city=None, governorate=None):
        """
        Convert address to latitude/longitude coordinates using Nominatim.
        
        Args:
            address: Street address
            city: City name (optional)
            governorate: Governorate/state (optional)
            
        Returns:
            dict with 'latitude' and 'longitude' keys, or None if not found
        """
        # Build search query
        query_parts = []
        if address:
            query_parts.append(address)
        if city:
            query_parts.append(city)
        if governorate:
            query_parts.append(governorate)
        
        query = ", ".join(query_parts)
        
        if not query:
            return None
        
        try:
            # Nominatim requires a User-Agent header
            headers = {
                'User-Agent': 'Forni-API/1.0'
            }
            
            params = {
                'q': query,
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(GeocodingService.BASE_URL, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                return {
                    'latitude': float(data[0]['lat']),
                    'longitude': float(data[0]['lon'])
                }
            
            return None
            
        except Exception as e:
            print(f"Geocoding error: {str(e)}")
            return None
    
    @staticmethod
    def reverse_geocode(latitude, longitude):
        """
        Convert coordinates to address (reverse geocoding).
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            dict with address information, or None if not found
        """
        try:
            headers = {
                'User-Agent': 'Forni-API/1.0'
            }
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json'
            }
            
            response = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params=params,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Reverse geocoding error: {str(e)}")
            return None
