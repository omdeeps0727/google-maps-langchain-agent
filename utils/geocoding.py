import googlemaps
gmaps = googlemaps.Client(key="GOOGLE_MAPS_API_KEY")
geocode_result = gmaps.geocode("1600 Amphitheatre Parkway")
print(geocode_result)