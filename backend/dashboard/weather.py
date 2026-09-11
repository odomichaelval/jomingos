import urllib.request
import json
from django.utils import timezone


# Set your care home location here
CARE_HOME_LAT  = 53.3811  # Sheffield — change to your city
CARE_HOME_LON  = -1.4701
CARE_HOME_NAME = 'Sheffield'


def get_weather_data():
    try:
        url = (
            f'https://api.open-meteo.com/v1/forecast'
            f'?latitude={CARE_HOME_LAT}&longitude={CARE_HOME_LON}'
            f'&current=temperature_2m,relative_humidity_2m,apparent_temperature,'
            f'precipitation,wind_speed_10m,pressure_msl,weather_code'
            f'&hourly=temperature_2m&forecast_days=1&timezone=Europe%2FLondon'
        )
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())

        current = data['current']
        temp        = current['temperature_2m']
        feels_like  = current['apparent_temperature']
        humidity    = current['relative_humidity_2m']
        precip      = current['precipitation']
        wind        = current['wind_speed_10m']
        pressure    = current['pressure_msl']
        code        = current['weather_code']

        # Build health risk warnings
        risks = []

        if temp <= 2:
            risks.append({
                'level': 'danger',
                'icon':  'bi-thermometer-snow',
                'text':  f'Extreme cold ({temp}°C) — high risk of hypothermia and respiratory infection. Ensure all residents are warm and hydrated.',
            })
        elif temp <= 8:
            risks.append({
                'level': 'warning',
                'icon':  'bi-thermometer-low',
                'text':  f'Cold weather ({temp}°C) — increased risk of chest infections and falls on icy surfaces. Monitor respiratory patients closely.',
            })

        if humidity >= 85:
            risks.append({
                'level': 'warning',
                'icon':  'bi-droplet-fill',
                'text':  f'High humidity ({humidity}%) — increased risk of respiratory distress for COPD and asthma patients.',
            })

        if pressure <= 1000:
            risks.append({
                'level': 'warning',
                'icon':  'bi-speedometer',
                'text':  f'Low atmospheric pressure ({pressure} hPa) — associated with increased joint pain, headaches, and agitation in dementia patients.',
            })

        if precip > 2:
            risks.append({
                'level': 'warning',
                'icon':  'bi-cloud-rain-heavy',
                'text':  'Heavy rain — increased fall risk if residents access outdoor areas. Ensure wet floor precautions indoors.',
            })

        if wind >= 40:
            risks.append({
                'level': 'danger',
                'icon':  'bi-wind',
                'text':  f'High winds ({wind} km/h) — outdoor activity not advised. Risk of falls and disorientation.',
            })

        # Weather description from code
        descriptions = {
            0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
            45: 'Foggy', 48: 'Icy fog', 51: 'Light drizzle', 53: 'Drizzle',
            55: 'Heavy drizzle', 61: 'Light rain', 63: 'Rain', 65: 'Heavy rain',
            71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 80: 'Rain showers',
            81: 'Heavy showers', 82: 'Violent showers', 95: 'Thunderstorm',
        }
        description = descriptions.get(code, 'Conditions unknown')

        # Overall risk level
        if any(r['level'] == 'danger' for r in risks):
            overall = 'danger'
            overall_label = 'HIGH Weather Risk'
        elif risks:
            overall = 'warning'
            overall_label = 'Weather Advisory'
        else:
            overall = 'success'
            overall_label = 'Conditions Normal'

        return {
            'success':       True,
            'temp':          temp,
            'feels_like':    feels_like,
            'humidity':      humidity,
            'precip':        precip,
            'wind':          wind,
            'pressure':      pressure,
            'description':   description,
            'risks':         risks,
            'overall':       overall,
            'overall_label': overall_label,
            'location':      CARE_HOME_NAME,
            'updated_at':    timezone.now(),
        }
    except Exception:
        return {'success': False}