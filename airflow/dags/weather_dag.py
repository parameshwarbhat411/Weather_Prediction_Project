from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import os

from etl.extraction import WeatherPipeLine

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arjunbhat/Downloads/bright-raceway-406701-2ed6ff87c381.json"

locations = ["London", "Tokyo", "Sydney", "Paris", "Berlin", "Moscow", "Madrid", "Rome", "Cairo", "Bangalore"]
weather = WeatherPipeLine(locations)

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id='load_weather_data',
    default_args=default_args,
    start_date=datetime(2023,12,30,1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task #1 - Extract data
    @task
    def extract_weather_data():
        weather.extract_weather_data()


    # Task #1 - load to cloud storage
    @task
    def load_to_cloud():
        weather.load_to_cloudStorage(overwrite=False)


    # Task #3 - load to Big Query
    @task
    def load_to_bigQuery(dataset_name, table_name):
        df = weather.process_cloud_data().reset_index(drop=True)
        weather.add_processed_metadata()
        weather.load_to_bigquery(df, dataset_name, table_name)

    # Dependencies
    extract_weather_data() >> load_to_cloud() >> load_to_bigQuery('weather','weather')

