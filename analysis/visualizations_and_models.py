import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import numpy as np


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/arjunbhat/Downloads/bright-raceway-406701-2ed6ff87c381.json"

class WeatherForecasting:

    def __init__(self, dataset_name, table_name, target_column):
        self.dataset_name = dataset_name
        self.table_name = table_name
        self.target_column = target_column
        self.df = None
        self.model = None
        self.preprocessor = None

    def fetch_bigquery_data(self):
        client = bigquery.Client()
        query = f"SELECT * FROM `{self.dataset_name}.{self.table_name}`"
        query_job = client.query(query)
        self.df = query_job.to_dataframe()

    def perform_eda(self):
        print(self.df.info())
        print(self.df.describe())

        self.df.hist(bins=50, figsize=(20, 15))
        plt.show()

        sns.pairplot(self.df.select_dtypes(include=['float64', 'int64']))
        plt.show()

        # Calculate correlations only for numeric columns
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        corr_matrix = numeric_df.corr()
        sns.heatmap(corr_matrix, annot=True)
        plt.show()

    def prepare_data(self):
        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def preprocess_data(self, X, fit=False):
        categorical_features = ['city', 'weather_main', 'weather_description']
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns

        if fit:
            # Only fit the preprocessor on the training data
            self.preprocessor = ColumnTransformer(
                transformers=[
                    ('num', 'passthrough', numeric_features),
                    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
                ])
            X_transformed = self.preprocessor.fit_transform(X)
        else:
            # Use the fitted preprocessor for the test data
            X_transformed = self.preprocessor.transform(X)

        return X_transformed

    def train_model(self, X_train, y_train, model_type='linear'):
        X_train_transformed = self.preprocess_data(X_train,fit=True)

        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'xgboost':
            self.model = XGBRegressor(n_estimators=50, random_state=42)

        self.model.fit(X_train_transformed, y_train)

    def evaluate_model(self, X_test, y_test):
        x_test_transformed = self.preprocess_data(X_test)
        y_pred = self.model.predict(x_test_transformed)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return mae, rmse

    def fetch_latest_data(self):
        client = bigquery.Client()
        query = f"""
        WITH RankedWeather AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY city ORDER BY datetime DESC) AS rn
            FROM
                `{self.dataset_name}.{self.table_name}`
        )
        SELECT * FROM RankedWeather WHERE rn = 1;
        """
        query_job = client.query(query)
        return query_job.to_dataframe()

    def predict_next_day_weather(self):
        latest_data = self.fetch_latest_data()
        latest_data_processed = self.preprocess_data(latest_data)

        # Predict the temperature for the next day
        next_day_predictions = self.model.predict(latest_data_processed)
        latest_data['predicted_temperature'] = next_day_predictions

        # Add a column for the date of prediction (next day)
        latest_data['prediction_date'] = pd.to_datetime(latest_data['datetime']).dt.date + pd.Timedelta(days=1)
        return latest_data[['city', 'prediction_date', 'predicted_temperature']]


weather_forecasting = WeatherForecasting('weather', 'weather', 'temperature')
weather_forecasting.fetch_bigquery_data()
weather_forecasting.perform_eda()
X_train, X_test, y_train, y_test = weather_forecasting.prepare_data()
weather_forecasting.train_model(X_train, y_train, 'linear')  # or 'xgboost'
mae, rmse = weather_forecasting.evaluate_model(X_test, y_test)
print(f'MAE: {mae}, RMSE: {rmse}')

# Predicting the next day's weather
next_day_weather_predictions = weather_forecasting.predict_next_day_weather()
print(next_day_weather_predictions)