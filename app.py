from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    weather = None
    city_name = None
    country_code = None
    state = None

    if request.method == "POST":

        city = request.form.get("city")
        country = request.form.get("country")
        city_name = city

        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "countryCode": country
            }
        ).json()

        if geo.get("results"):
            place = geo["results"][0]
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            city_name = place.get("name")
            country_code = place.get("country_code")
            state = place.get("admin1")
            print(geo["results"][0]["admin1"])
            data = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
                    "forecast_days": 3,

                }
            ).json()

            weather = data["hourly"]
            # print(data["hourly"])
            # print(data["timezone"])
            # print(data["hourly_units"])

    return render_template(
        "index.html",
        weather=weather,
        city_name=city_name,
        country_code=country_code,
        state=state,
        lat=lat,
        lon=lon
    )

@app.route("/xx/", methods=["GET", "POST"])
def xx():
    return "xx"

# @app.route("/yy/", methods=["GET", "POST"])
# def hello():
    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
