import etl.extraction as weather

if __name__ == "__main__":
    locations = ["London", "Tokyo", "Sydney", "Paris", "Berlin", "Moscow", "Madrid", "Rome", "Cairo","Bangalore"]
    weather = weather.WeatherPipeLine(locations)
    weather.extract_weather_data()
    weather.load_to_cloudStorage(overwrite=False)
    df = weather.process_cloud_data().reset_index(drop=True)
    weather.add_processed_metadata()
    print("Ready")