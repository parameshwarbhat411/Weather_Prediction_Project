import os

import pandas as pd
import requests
import json
from datetime import datetime

from google.cloud.exceptions import Conflict

import etl.util as ut
from typing import Tuple
from google.cloud import storage

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d").replace("-", "_")
DIRECTORY = f"{ut.Util.WORK_DIR}/{CURRENT_DATE}"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arjunbhat/Downloads/bright-raceway-406701-2ed6ff87c381.json"
storage_client = storage.Client()


class WeatherPipeLine:

    def __init__(self, locations=None) -> None:
        self.locations = locations

    def extract_weather_data(self):

        try:
            if not os.path.exists(DIRECTORY):
                os.makedirs(DIRECTORY)
        except OSError as error:
            print(f"Error creating directory {DIRECTORY}: {error}")
            return

        for location in self.locations:
            try:
                lat, lon = self.extract_lat_lon(location)
                url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&units=metric&appid={ut.Util.API_KEY}'
                response = requests.get(url)
                response.raise_for_status()  # Raises HTTPError for bad status codes
                data = response.json()
            except requests.RequestException as e:
                print(f"Request error for location {location}: {e}")
                continue
            except ValueError as e:
                print(f"Error processing data for location {location}: {e}")
                continue

            formatted_json = json.dumps(data, sort_keys=True, indent=4)
            try:
                with open(f"{DIRECTORY}/{location}.txt", "w") as write_file:
                    write_file.write(formatted_json)
            except IOError as e:
                print(f"Error writing to file for location {location}: {e}")

    def extract_lat_lon(self, city_name) -> Tuple[float, float]:
        try:
            url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={ut.Util.API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data and 'lat' in data[0] and 'lon' in data[0]:
                return float(data[0]['lat']), float(data[0]['lon'])
            else:
                raise ValueError("Invalid data received from API")
        except requests.RequestException as e:
            print(f"Request error for city {city_name}: {e}")
            raise
        except ValueError as e:
            print(f"Data processing error for city {city_name}: {e}")
            raise

    def list_buckets(self):
        buckets = storage_client.list_buckets()

        for bucket in buckets:
            print(bucket.name)

    def getOrCreate_bucket(self, bucket_name=f'weather_bucket_{CURRENT_DATE}'):
        try:
            # Try creating the bucket
            bucket = storage_client.create_bucket(bucket_or_name=bucket_name)
            print(f"Bucket {bucket_name} created.")
        except Conflict:
            print(f"Bucket {bucket_name} already exists. Retrieving the existing bucket.")
            bucket = storage_client.get_bucket(bucket_or_name=bucket_name)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
        return bucket

    def load_to_cloudStorage(self, bucket_name=f'weather_bucket_{CURRENT_DATE}', overwrite=False):
        """
                Description:
                    - getOrCreate a Cloud Storage bucket
                    - Load today's text files
                    - For cleanup, set overwrite = True
                Args:
                    bucket_name(str)
                    overwrite(bool)
                Returns:
                    None
                """

        bucket = self.getOrCreate_bucket(bucket_name)

        if overwrite:
            # If overwrite is True, delete existing files in the bucket
            blobs = bucket.list_blobs()
            for blob in blobs:
                blob.delete()

        os.chdir(DIRECTORY)
        for file_name in os.listdir():
            file_path = os.path.join(DIRECTORY, file_name)
            if os.path.isfile(file_path):
                blob = bucket.blob(file_name + f'_{CURRENT_DATE}_{datetime.now().strftime("%H-%M-%S")}')
                blob.upload_from_filename(file_path)
                print(f"Uploaded {file_name} to {bucket_name}.")

    def process_data(self):
        """
            Process raw weather data into a Pandas DataFrame
            Args:
                None
            Returns
                - df(pandas.DataFrame)
        """
        os.chdir(DIRECTORY)
        files = os.listdir()
        df = pd.DataFrame()

        for file in files:
            with open(file,'r') as read_file:
                data = json.loads(read_file.read())
                processed_data = []
                # Iterate over each record in the data
                for record in data['list']:
                    # Extract relevant fields
                    entry = {
                        'city': file.split('.')[0],
                        'datetime': pd.to_datetime(record['dt'], unit='s'),
                        'temperature': record['main']['temp'],
                        'feels_like': record['main']['feels_like'],
                        'pressure': record['main']['pressure'],
                        'humidity': record['main']['humidity'],
                        'temp_min': record['main']['temp_min'],
                        'temp_max': record['main']['temp_max'],
                        'wind_speed': record['wind']['speed'],
                        'wind_deg': record['wind']['deg'],
                        'cloudiness': record['clouds']['all'],
                        'weather_main': record['weather'][0]['main'],
                        'weather_description': record['weather'][0]['description']
                    }
                    processed_data.append(entry)

                # Convert list to DataFrame
                weather_df = pd.DataFrame(processed_data)
                df = pd.concat([df,weather_df])

                read_file.close()
        return df

    def process_cloud_data(self, bucket_name=f'weather_bucket_{CURRENT_DATE}'):
        """
        Process raw weather data from Google Cloud Storage into a Pandas DataFrame
        Args:
            bucket_name(str): The name of the Google Cloud Storage bucket
        Returns:
            df(pandas.DataFrame): The processed data
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        df = pd.DataFrame()
        try:
            # List all files in the specified bucket
            blobs = bucket.list_blobs()  # Adjust prefix if needed

            for blob in blobs:
                # Read the file content
                file_content = blob.download_as_string()
                data = json.loads(file_content.decode('utf-8'))
                processed_data = []
                print(blob.name)
                # Iterate over each record in the data
                for record in data['list']:
                    # Extract relevant fields
                    entry = {
                        'city': blob.name.split('.')[0],
                        'datetime': pd.to_datetime(record['dt'], unit='s'),
                        'temperature': record['main']['temp'],
                        'feels_like': record['main']['feels_like'],
                        'pressure': record['main']['pressure'],
                        'humidity': record['main']['humidity'],
                        'temp_min': record['main']['temp_min'],
                        'temp_max': record['main']['temp_max'],
                        'wind_speed': record['wind']['speed'],
                        'wind_deg': record['wind']['deg'],
                        'cloudiness': record['clouds']['all'],
                        'weather_main': record['weather'][0]['main'],
                        'weather_description': record['weather'][0]['description']
                    }
                    processed_data.append(entry)

                # Convert list to DataFrame and concatenate
                weather_df = pd.DataFrame(processed_data)
                df = pd.concat([df, weather_df])

        except Exception as e:
            print(f"An error occurred: {e}")

        return df

    def add_processed_metadata(self,bucket_name=f'weather_bucket_{CURRENT_DATE}'):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.metadata = {'processed': 'true'}
            blob.patch()
            print(f"Added processed metadata to {blob.name}")