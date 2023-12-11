
import etl.extraction as weather

if __name__ == "__main__":
    locations = ["London", "Tokyo", "Sydney", "Paris", "Berlin", "Moscow", "Madrid", "Rome", "Cairo"]
    weather = weather.WeatherPipeLine(locations)
    lat, lon =  weather.extract_lat_lon("Sydney")
    weather.extract_weather_data(lat,lon)