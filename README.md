# Weather Alert SMS Notification

This project fetches weather forecast data from the OpenWeatherMap API to determine if it will rain in the next 12 hours. If rain is forecasted, it sends an SMS notification via the Twilio API to remind the user to bring an umbrella.
![11fd869c-20fd-4af7-b7c6-2049a47e1e55](https://github.com/xinconggg/SMS-Rain-Alert/assets/82378681/b954d880-273a-4e4d-975f-3344996aa9ab)

## Features

- Fetches weather forecast data for a specified location using OpenWeatherMap API.
- Checks if it will rain in the next 12 hours.
- Sends an SMS alert to a specified phone number if rain is forecasted.

## Requirements

- Python 3.x
- `requests` library
- `twilio` library
- OpenWeatherMap API key
- Twilio Account SID and Auth Token
- Twilio phone number

## Installation

#### 1. Clone the repository:
```
git clone https://github.com/your-username/weather-alert-sms.git
cd weather-alert-sms
```
#### 2. Install the required Python libraries:
```
pip install requests twilio
```
#### 3. Set up environment variables for your API keys and phone numbers. You can add these to a .env file or set them directly in your environment:
```
OWM_API_KEY=your_openweathermap_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
MY_NUMBER=your_phone_number
TWILIO_NUMBER=your_twilio_phone_number
https_proxy=your_proxy_url  # Optional, if behind a proxy
```

## Usage
#### 1. Open weather_alert_sms.py and configure the latitude and longitude for your location:
```
latitude = 1.352083  # Example: Singapore latitude
longitude = 103.819839  # Example: Singapore longitude
```
#### 2. Run the script:
```
python weather_alert_sms.py
```
The script will fetch the weather forecast for the next 12 hours and send an SMS if rain is expected.

## Code Explanation
### Fetching Weather Data
The script uses the `requests` library to fetch weather forecast data from OpenWeatherMap API:
```
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
parameters = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key,
    "cnt": 4  # Fetch data for the next 12 hours (4 time slots, each 3 hours apart)
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
```

### Checking for Rain
The script checks if any of the weather conditions in the next 12 hours indicate rain:
```
will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
```
### Sending SMS Alert
If rain is forecasted, the script sends an SMS alert using the Twilio API:
```
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ.get("https_proxy")}
    client = Client(account_psid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring your umbrella☂️☂️☂️",
        from_=twilio_number,
        to=my_number
    )
```
