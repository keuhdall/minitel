import urequests as requests

API_KEY = ""
CITY = "Paris,FR"
REFRESH = 60

def get_weather():
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={API_KEY}&units=metric&lang=fr"
    )
    try:
        r = requests.get(url)
        data = r.json()
        r.close()
        return {
            "temp": data["main"]["temp"],
            "hum": data["main"]["humidity"],
            "pres": data["main"]["pressure"],
            "desc": data["weather"][0]["description"],
            "id": data["weather"][0]["id"]
        }

    except:
        return None