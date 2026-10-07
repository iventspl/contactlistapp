import requests
from django.core.cache import cache

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
USER_AGENT = "ContactListApp/1.0 (https://github.com/iventspl/contactlistapp)"
REQUEST_TIMEOUT = 5  # seconds

# City coordinates almost never change, so they can be cached for a long time.
COORDINATES_CACHE_TIMEOUT = 60 * 60 * 24 * 30  # 30 days
WEATHER_CACHE_TIMEOUT = 60 * 30  # 30 minutes


def get_coordinates(city):
    """Return (lat, lon) for given city or None if the city was not found"""
    response = requests.get(NOMINATIM_URL,
                            params={"q": city, "format": "json", "limit": 1},
                            headers={"User-Agent": USER_AGENT},
                            timeout=REQUEST_TIMEOUT,
                            )

    response.raise_for_status()

    data = response.json()
    if not data:
        return None
    lat, lon = data[0]["lat"], data[0]["lon"]
    return (float(lat), float(lon))


def get_current_weather(lat, lon):
    """Return current temp, humidity and wind speed for given coords"""
    response = requests.get(OPEN_METEO_URL,
                            params={
                                "latitude": lat, 
                                "longitude": lon, 
                                "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
                            },
                            headers={"User-Agent": USER_AGENT},
                            timeout=REQUEST_TIMEOUT)

    response.raise_for_status()

    current = response.json()["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
    }


def get_weather_for_city(city):
    """Return current weather for given city or None if city was not found"""

    city_key = city.strip().casefold()

    coordinates = cache.get_or_set(
        f"coordinates:{city_key}",
        lambda: get_coordinates(city),
        COORDINATES_CACHE_TIMEOUT,
    )

    if coordinates is None:
        return None

    lat, lon = coordinates

    return cache.get_or_set(
        f"weather:{lat},{lon}",
        lambda: get_current_weather(lat, lon),
        WEATHER_CACHE_TIMEOUT
    )