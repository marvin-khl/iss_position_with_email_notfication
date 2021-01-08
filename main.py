import time
import requests
import datetime as dt
import os
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from twilio.rest import Client

SUNSET_ENDPOINT = 'https://api.sunrise-sunset.org/json'
ISS_ENDPOINT = 'http://api.open-notify.org/iss-now.json'
account_sid = os.environ.get('TWILLIO_ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')

# Set latitude and longitude for Berlin
LAT = 52.520008
LNG = 13.404954


def is_night():
    parameter = {
        'lat': LAT,
        'lng': LNG,
        'formatted': 0
    }

    weather_response = requests.get(url=SUNSET_ENDPOINT, params=parameter)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    # get sunrise time and create time delta
    sunrise_time = weather_data['results']['sunrise']
    srt = dt.datetime.fromisoformat(sunrise_time)
    sunrise_time_delta = dt.timedelta(hours=srt.hour, minutes=srt.minute, seconds=srt.second)

    # get sunset time and create time delta
    sunset_time = weather_data['results']['sunset']
    sst = dt.datetime.fromisoformat(sunset_time)
    sunset_time_delta = dt.timedelta(hours=sst.hour, minutes=sst.minute, seconds=sst.second)

    # get current time and create time delta
    ct = dt.datetime.now()
    current_time_delta = dt.timedelta(hours=ct.hour, minutes=ct.minute, seconds=ct.second)

    # check if is night
    if sunrise_time_delta > current_time_delta or current_time_delta > sunset_time_delta:
        # its dark
        return True
    else:
        return False


def get_iss_position():
    # get iss position api
    iss_response = requests.get(ISS_ENDPOINT)
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    lat = float(iss_data['iss_position']['latitude'])
    lng = float(iss_data['iss_position']['longitude'])
    position = (lat, lng)
    return position


def send_sms(location):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"The ISS is in the near 👀 Look up! 🛰👆🏻At the moment it is: {location}",
        from_='+0000000',  # enter your Twilio phone number here
        to='+000000000'  # enter your verified phone number here
    )

    print(message.status)


while is_night():
    iss_location = get_iss_position()
    my_location = (LAT, LNG)
    circle_distance = great_circle(iss_location, my_location).kilometers

    if circle_distance < 500:  # change the distance if you want
        geolocator = Nominatim(user_agent="iss_at_the_night")
        iss_address = geolocator.reverse(f"{iss_location[0]},{iss_location[1]}")

        if iss_address is not None:
            send_sms(iss_address)
        else:
            send_sms('Somewhere above the sea!')

    time.sleep(60)
