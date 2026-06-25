from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "2708868d46b1a0fe47b412a0298741cc"


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    forecast = []
    hourly_forecast = []
    rain_probability = []
    alerts = []
    aqi_data = None
    ai_advice = ""
    clothing = ""
    error = None

    current_time = datetime.now().strftime("%d %B %Y | %I:%M %p")

    if request.method == "POST":

        city = request.form.get("city")

        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(weather_url)
        data = response.json()

        if data.get("cod") != 200:

            error = "City not found"

        else:

            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            weather = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "visibility": round(data["visibility"] / 1000, 1),
                "wind": data["wind"]["speed"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],

                "sunrise": datetime.utcfromtimestamp(
                    data["sys"]["sunrise"] + data["timezone"]
                ).strftime("%I:%M %p"),

                "sunset": datetime.utcfromtimestamp(
                    data["sys"]["sunset"] + data["timezone"]
                ).strftime("%I:%M %p"),

                "lat": lat,
                "lon": lon
            }

            # ======================
            # AQI DATA
            # ======================

            aqi_url = (
                f"http://api.openweathermap.org/data/2.5/air_pollution?"
                f"lat={lat}&lon={lon}&appid={API_KEY}"
            )

            aqi_response = requests.get(aqi_url)
            aqi_json = aqi_response.json()

            if "list" in aqi_json:

                aqi_value = aqi_json["list"][0]["main"]["aqi"]

                aqi_status = {
                    1: "Good 😊",
                    2: "Fair 🙂",
                    3: "Moderate 😐",
                    4: "Poor 😷",
                    5: "Very Poor ☠️"
                }

                aqi_data = {
                    "value": aqi_value,
                    "status": aqi_status.get(aqi_value)
                }
                            # ======================
            # 5 DAY FORECAST
            # ======================

            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast?"
                f"q={city}&appid={API_KEY}&units=metric"
            )

            forecast_response = requests.get(forecast_url)
            forecast_json = forecast_response.json()

            added_dates = set()

            for item in forecast_json["list"]:

                date = datetime.strptime(
                    item["dt_txt"].split(" ")[0],
                    "%Y-%m-%d"
                ).strftime("%d %b")

                if date not in added_dates:

                    forecast.append({
                        "date": date,
                        "temp": round(item["main"]["temp"]),
                        "icon": item["weather"][0]["icon"]
                    })

                    added_dates.add(date)

                if len(forecast) == 5:
                    break

            # ======================
            # HOURLY FORECAST
            # ======================

            for item in forecast_json["list"][:8]:

                hourly_forecast.append({

                    "time": datetime.strptime(
                        item["dt_txt"],
                        "%Y-%m-%d %H:%M:%S"
                    ).strftime("%I %p"),

                    "temp": round(item["main"]["temp"]),

                    "icon": item["weather"][0]["icon"]

                })

                rain_probability.append({

                    "time": datetime.strptime(
                        item["dt_txt"],
                        "%Y-%m-%d %H:%M:%S"
                    ).strftime("%I %p"),

                    "chance": int(item.get("pop", 0) * 100)

                })
                            # ======================
            # AI WEATHER ADVICE
            # ======================

            temp = weather["temperature"]
            condition = weather["description"].lower()

            if temp >= 38:
                ai_advice = (
                    "🥵 Extremely hot today. Stay hydrated, avoid direct sunlight "
                    "and wear light cotton clothes."
                )
                clothing = "👕 Cotton T-Shirt • 🧢 Cap • 🕶 Sunglasses"

            elif temp >= 30:
                ai_advice = (
                    "☀️ Warm weather. Carry a water bottle and sunscreen."
                )
                clothing = "👕 Half Sleeves • 🧢 Cap"

            elif temp >= 20:
                ai_advice = (
                    "🌤 Pleasant weather. Great day for outdoor activities."
                )
                clothing = "👕 Casual Wear"

            elif temp >= 10:
                ai_advice = (
                    "🧥 Cool weather. Consider wearing a light jacket."
                )
                clothing = "🧥 Light Jacket"

            else:
                ai_advice = (
                    "❄ Very cold outside. Wear warm clothes."
                )
                clothing = "🧥 Winter Jacket • 🧤 Gloves"

            if "rain" in condition:
                ai_advice += " ☔ Carry an umbrella."
                clothing += " ☔ Umbrella"

            if "snow" in condition:
                ai_advice += " ❄ Roads may be slippery."
                clothing += " 🥾 Boots"

            if weather["wind"] > 10:
                ai_advice += " 💨 Strong winds expected."

            if weather["humidity"] > 80:
                ai_advice += " 💧 High humidity today."

            # ======================
            # WEATHER ALERTS
            # ======================

            if weather["temperature"] > 40:
                alerts.append("🔥 Heat Wave Alert")

            if weather["wind"] > 10:
                alerts.append("🌪 High Wind Alert")

            if weather["humidity"] > 85:
                alerts.append("💧 High Humidity Alert")

            if weather["visibility"] < 2:
                alerts.append("🌫 Low Visibility Alert")
                return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        hourly_forecast=hourly_forecast,
        rain_probability=rain_probability,
        alerts=alerts,
        aqi_data=aqi_data,
        ai_advice=ai_advice,
        clothing=clothing,
        current_time=current_time,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)