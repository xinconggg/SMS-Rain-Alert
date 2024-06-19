import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# openweathermap.org
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
# latlong.net
latitude = 1.352083
longitude = 103.819839
# twilio.com
account_psid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_number = os.environ.get("MY_NUMBER")
twilio_number = os.environ.get("TWILIO_NUMBER")

will_rain = False
parameters = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# If it's going to rain in the next 12 hours, send an SMS
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ.get("https_proxy")}
    client = Client(account_psid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring your umbrella☂️☂️☂️",
        from_=twilio_number,
        to=my_number
    )