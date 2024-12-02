from collections import defaultdict
from datetime import datetime, timedelta
from itertools import islice

import googleapiclient.discovery
import pytz
import requests
from flask import Flask, render_template
from google.oauth2 import service_account

# Constants
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = '/home/bendi/dashboard/static/my-project-1529023744824-e9991d46a556.json'
MAX_DAYS = 4

# Weather symbols dictionary
wmo_symbols = {
    '0': '☀️ Clear',
    '1': '🌤️ Mostly Clear',
    '2': '⛅ Partly Cloudy',
    '3': '☁️ Cloudy',
    '45': '🌫️ Fog',
    '48': '🌫️❄️ Freezing Fog',
    '51': '🌧️ Light Drizzle',
    '53': '🌧️ Drizzle',
    '55': '🌧️ Heavy Drizzle',
    '56': '🌧️❄️ Light Freezing Drizzle',
    '57': '🌧️❄️ Freezing Drizzle',
    '61': '🌧️ Light Rain',
    '63': '🌧️ Rain',
    '65': '🌧️ Heavy Rain',
    '66': '🌧️❄️ Light Freezing Rain',
    '67': '🌧️❄️ Freezing Rain',
    '71': '🌨️ Light Snow',
    '73': '🌨️ Snow',
    '75': '🌨️ Heavy Snow',
    '77': '🌨️ Snow Grains',
    '80': '🌧️ Light Rain Shower',
    '81': '🌧️ Rain Shower',
    '82': '🌧️ Heavy Rain Shower',
    '85': '🌨️ Snow Shower',
    '86': '🌨️ Heavy Snow Shower',
    '95': '⛈️ Thunderstorm',
    '96': '🌨️ Hailstorm',
    '99': '🌨️ Heavy Hailstorm'
}


app = Flask(__name__)


@app.template_filter('string_to_datetime')
def string_to_datetime(value):
    if value is None:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except (ValueError, TypeError):
        return None


def get_google_calendar_events():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

        now = datetime.utcnow()
        start_time = now
        end_time = now + timedelta(days=7)

        events_result = service.events().list(
            calendarId='bvk.rao@gmail.com',
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return events
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def group_calendar_events(events):
    grouped_events = defaultdict(list)
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))

        start_time = start_time[:-1] if start_time.endswith('Z') else start_time
        end_time = end_time[:-1] if end_time.endswith('Z') else end_time

        start_time_formatted = datetime.fromisoformat(start_time).strftime('%I:%M %p')
        end_time_formatted = datetime.fromisoformat(end_time).strftime('%I:%M %p')


        event['start']['dateTime'] = start_time_formatted
        event['end']['dateTime'] = end_time_formatted

        start_datetime = datetime.fromisoformat(start_time)
        date = start_datetime.strftime('%d-%b-%Y %a')
        grouped_events[date].append(event)
    grouped_events = dict(islice(grouped_events.items(), MAX_DAYS))
    return grouped_events


def get_time_for_regions():
    current_time = datetime.now()
    seattle_timezone = pytz.timezone('America/Los_Angeles')
    india_timezone = pytz.timezone('Asia/Kolkata')
    australia_sydney_timezone = pytz.timezone('Australia/Sydney')
    belgrade_timezone = pytz.timezone('Europe/Belgrade')

    return {
        "seattle": current_time.astimezone(seattle_timezone).strftime('%a %d-%b %I:%M %p'),
        "india": current_time.astimezone(india_timezone).strftime('%a %d-%b %I:%M %p'),
        "sydney": current_time.astimezone(australia_sydney_timezone).strftime('%a %d-%b %I:%M %p'),
        "belgrade": current_time.astimezone(belgrade_timezone).strftime('%a %d-%b %I:%M %p'),
    }


def fetch_weather():
    weatherdata = {}
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.8531,
        "longitude": -3.5881,
        "current": ["temperature_2m", "rain"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "weather_code"],
        "timezone": "Europe/London",
        "forecast_days": 2
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()

            current_temp = weather_data.get("current").get("temperature_2m")
            current_temp_units = weather_data.get("current_units").get("temperature_2m")
            current_rain = weather_data.get("current").get("rain")
            current_temp_max = weather_data.get("daily").get("temperature_2m_max")[0]
            current_temp_min = weather_data.get("daily").get("temperature_2m_min")[0]
            sun_rise = weather_data.get("daily").get("sunrise")[0]
            sun_set = weather_data.get("daily").get("sunset")[0]
            current_weather_code = weather_data.get("daily").get("weather_code")[0]
            next_day_temp_max = weather_data.get("daily").get("temperature_2m_max")[1]
            next_day_temp_min = weather_data.get("daily").get("temperature_2m_min")[1]
            next_day_sun_rise = weather_data.get("daily").get("sunrise")[1]
            next_day_sun_set = weather_data.get("daily").get("sunset")[1]
            next_day_weather_code = weather_data.get("daily").get("weather_code")[1]

            weatherdata.update({
                "temp_units": current_temp_units,
                "todays_temperature": current_temp,
                "todays_rain": current_rain,
                "todays_weather_code": wmo_symbols[str(current_weather_code)],
                "todays_max_temp": current_temp_max,
                "todays_min_temp": current_temp_min,
                "todays_sunrise": sun_rise,
                "todays_sunset": sun_set,
                "tomorrows_weather_code": wmo_symbols[str(next_day_weather_code)],
                "tomorrows_max_temp": next_day_temp_max,
                "tomorrows_min_temp": next_day_temp_min,
                "tomorrows_sunrise": next_day_sun_rise,
                "tomorrows_sunset": next_day_sun_set
            })
            return weatherdata
        else:
            print(f"Failed to retrieve weather data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def fetch_todays_weather_details():
    weather_data = fetch_weather()
    if weather_data:
        todays_sunrise = datetime.strptime(weather_data.get("todays_sunrise"), "%Y-%m-%dT%H:%S").strftime("%I:%S %p")
        todays_sunset = datetime.strptime(weather_data.get("todays_sunset"), "%Y-%m-%dT%H:%S").strftime("%I:%S %p")
        return {
            "todays_weather_code": weather_data.get("todays_weather_code"),
            "temp_units": weather_data.get("temp_units"),
            "todays_temperature": weather_data.get("todays_temperature"),
            "todays_rain": weather_data.get("todays_rain"),
            "rain_units": "mm",
            "todays_max_temp": weather_data.get("todays_max_temp"),
            "todays_min_temp": weather_data.get("todays_min_temp"),
            "todays_sunrise": todays_sunrise,
            "todays_sunset": todays_sunset,
        }
    else:
        return {}


def fetch_tomorrows_weather_details():
    weather_data = fetch_weather()
    if weather_data:
        tomorrows_sunrise = datetime.strptime(weather_data.get("tomorrows_sunrise"), "%Y-%m-%dT%H:%S").strftime(
            "%I:%S %p")
        tomorrows_sunset = datetime.strptime(weather_data.get("tomorrows_sunset"), "%Y-%m-%dT%H:%S").strftime(
            "%I:%S %p")
        return {
            "tomorrows_weather_code": weather_data.get("tomorrows_weather_code"),
            "temp_units": weather_data.get("temp_units"),
            "tomorrows_max_temp": weather_data.get("tomorrows_max_temp"),
            "tomorrows_min_temp": weather_data.get("tomorrows_min_temp"),
            "tomorrows_sunrise": tomorrows_sunrise,
            "tomorrows_sunset": tomorrows_sunset,
        }
    else:
        return {}


@app.route('/')
def index():
    today_weather = fetch_todays_weather_details()
    tomorrow_weather = fetch_tomorrows_weather_details()
    events = get_google_calendar_events()
    grouped_events = group_calendar_events(events)
    time_for_regions = get_time_for_regions()

    return render_template('index.html', today_weather=today_weather,
                           tomorrow_weather=tomorrow_weather,
                           grouped_events=grouped_events,
                           time_for_regions=time_for_regions)


if __name__ == '__main__':
    app.run(debug=True)
