from typing import Any
from flask import Flask, render_template, request
import requests
import time
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache',
                      'CACHE_DEFAULT_TIMEOUT' : 600
                      })
cache.init_app(app)

@app.route("/weather", methods=["GET", "POST"])
def get_weather():
    weather = None
    city_name = None
    country_code = None
    state = None
    lat = None
    lon = None

    if request.method == "POST":

        city = request.form.get("city")
        country = request.form.get("country")
        city_name = city

        geo = get_geo_data(city, country)

        if geo.get("results"):
            place = geo["results"][0]
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            city_name = place.get("name")
            country_code = place.get("country_code")
            state = place.get("admin1")
            data = fetch_weather(lat, lon)
            weather = data["hourly"]

    return render_template(
        "index.html",
        weather=weather,
        city_name=city_name,
        country_code=country_code,
        state=state,
        lat=lat,
        lon=lon
    )

counter = 0

@cache.memoize(timeout=3600)
def fetch_weather(lat, lon) -> Any:
    print("Getting data from API.")
    print(cache.cache._cache.keys())
    start = time.time()
    global counter
    counter += 1

    print(f"Executing API request nr {counter}")
    data = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
            "forecast_days": 2,
        }
    ).json()
    print(f"Downloading time: {time.time() - start:.3f} s")
    return data


@cache.memoize(timeout=6000)
def get_geo_data(city: str | None, country: str | None) -> Any:
    print("Getting geo data from API.")
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
            "countryCode": country
        }
    ).json()
    return geo

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
