import requests
import pandas as pd
import json
from datetime import datetime
import etl.util as ut
from typing import Tuple

class WeatherPipeLine:

    def __init__(self, locations=None) -> None:
        self.locations = locations

    def extract_weather_data(self, lat, lon):
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&appid={ut.Util.API_KEY}'

        r = requests.get(url)

        data = r.json()

        formatted_json = json.dumps(data, sort_keys=True, indent=4)

        print(data)

    def extract_lat_lon(self, city_name) -> Tuple[float, float]:
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={ut.Util.API_KEY}'

        r = requests.get(url)
        data = r.json()

        # Ensure that you have valid data and the expected fields are present
        if data and 'lat' in data[0] and 'lon' in data[0]:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            raise ValueError("Invalid data received from API")
