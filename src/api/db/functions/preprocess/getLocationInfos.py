from geopy.exc import GeocoderTimedOut
import json
from geopy.geocoders import Nominatim

def getLocationInfos(city):
    geolocator = Nominatim(user_agent="city_mapper")
    print(city.capitalize())
    try:
        location = geolocator.geocode(city.capitalize(), language='fr')
        if location:
            if city.lower() == "paris":
                department = "Paris"
                region = "Île-de-France"

                department_coords = {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }

                region_coords = {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }
            else:
                reverse_location = geolocator.reverse((location.latitude, location.longitude), language='fr')

                department = reverse_location.raw.get('address', {}).get('county')
                department_location = geolocator.geocode(f"{department}, France")

                region = reverse_location.raw.get('address', {}).get('state')
                region_location = geolocator.geocode(f"{region}, France")
                
                if department_location is not None and region_location is not None:
                    department_coords = {
                        "latitude": department_location.latitude,
                        "longitude": department_location.longitude
                    }
                    region_coords = {
                        "latitude": region_location.latitude,
                        "longitude": region_location.longitude
                    }
                else:
                    return None

            city_coords = {
                "latitude": location.latitude,
                "longitude": location.longitude
            }

            return {
                "city": {"name": city, "coordinates": json.dumps(city_coords)},
                "department": {"name": department, "coordinates": json.dumps(department_coords)},
                "region": {"name": region, "coordinates": json.dumps(region_coords)}
            }
        else:
            print(f"Location not found for {city}")
            return None

    except GeocoderTimedOut as e:
        print(f"Geocoding timed out for {city}")
        return None