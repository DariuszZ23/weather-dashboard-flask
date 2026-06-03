from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    weather = None

    if request.method == "POST":

        city = request.form["city"]
        country = request.form["country"]

        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "countryCode": country
            }
        ).json()

        if geo.get("results"):

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            data = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "temperature_2m",
                    "forecast_days": 1
                }
            ).json()

            weather = data["hourly"]

    return render_template("index.html", weather=weather)

@app.route("/xx/", methods=["GET", "POST"])
def xx():
    return "xx"

# @app.route("/yy/", methods=["GET", "POST"])
# def hello():
    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
