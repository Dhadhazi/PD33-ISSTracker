import requests
from datetime import datetime

MY_LAT = 52.370216 # Your latitude
MY_LONG = 4.895168 # Your longitude


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return {"latitude": iss_latitude, "longitude" :  iss_longitude}


def get_sunrise_sunset_hours():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return {"sunrise": sunrise, "sunset": sunset}


def is_it_night():
    time_now = datetime.now()
    sun_time = get_sunrise_sunset_hours()
    return sun_time["sunset"] < time_now.hour < sun_time["sunrise"]


def i_see_lat_long(coordinates):
    return MY_LAT-5 < coordinates["latitude"] < MY_LAT+5 or MY_LONG-5 < coordinates["longitude"] < MY_LONG+5


if i_see_lat_long(get_iss_position()) and is_it_night():
    print("Look up, ISS is here!")
else:
    print("ISS is not here or it is daytime")