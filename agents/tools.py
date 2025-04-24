import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()


# Get API key with validation
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
if not api_key:
    raise ValueError(
        "Google Maps API key not found. "
        "Please add it to your .env file as GOOGLE_MAPS_API_KEY=your_key"
    )

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def get_place_details(place_name: str) -> str:
    """Get details about a specific place"""
    try:
        places_result = gmaps.places(place_name)
        if places_result['results']:
            place = places_result['results'][0]
            return f"Name: {place['name']}\nAddress: {place.get('formatted_address', 'N/A')}\nRating: {place.get('rating', 'N/A')}"
        return "No results found for this place."
    except Exception as e:
        return f"Error getting place details: {str(e)}"

def get_directions(origin: str, destination: str, mode: str = "driving") -> str:
    """Get directions between two locations"""
    try:
        directions = gmaps.directions(origin, destination, mode=mode)
        if directions:
            steps = directions[0]['legs'][0]['steps']
            return "\n".join([step['html_instructions'] for step in steps])
        return "No directions found."
    except Exception as e:
        return f"Error getting directions: {str(e)}"

def find_nearby_places(location: str, keyword: str = "", radius: int = 5000) -> str:
    """Find places near a location"""
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            lat_lng = geocode_result[0]['geometry']['location']
            places = gmaps.places_nearby(
                location=f"{lat_lng['lat']},{lat_lng['lng']}",
                radius=radius,
                keyword=keyword
            )
            if places['results']:
                return "\n".join([f"{i+1}. {place['name']} ({place.get('rating', 'N/A')}★)" 
                                for i, place in enumerate(places['results'][:5])])
            return "No nearby places found."
        return "Location not found."
    except Exception as e:
        return f"Error finding nearby places: {str(e)}"

def geocode_address(address: str) -> str:
    """Convert address to geographic coordinates"""
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return f"Latitude: {location['lat']}, Longitude: {location['lng']}"
        return "Address not found."
    except Exception as e:
        return f"Error geocoding address: {str(e)}"