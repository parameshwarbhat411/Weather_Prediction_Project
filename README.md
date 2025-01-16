# Weather Data Pipeline with Machine Learning

## Overview

This project aims to build a **data pipeline** that extracts past **24-hour weather data** for specified locations, processes the data, and uses it to **predict the next day's weather** using **machine learning models**. The pipeline is orchestrated using **Apache Airflow**, with **Google Cloud Storage (GCS)** serving as the data storage solution and **Google BigQuery (BQ)** for data analysis and prediction.

By leveraging **cloud-based data orchestration, storage, and machine learning**, this pipeline automates the **extraction, transformation, and loading (ETL) process**, followed by **ML-based weather forecasting**, ensuring scalability and reliability.

---

## Components

### **1. ETL Process**
The **Extract, Transform, Load (ETL)** process is the **core of the pipeline** and consists of the following stages:

- **Extraction**: Retrieves weather data for specified locations from the **OpenWeatherMap API**.
- **Transformation**: Processes the raw weather data to extract relevant features and **clean the data** for analysis.
- **Loading**: Stores the **processed data** in **Google Cloud Storage (GCS)** and loads it into **Google BigQuery (BQ)** for further analysis.

### **2. Machine Learning Model for Prediction**
- Uses **supervised learning models** trained on past weather data to forecast **next-day weather conditions**.
- Supports models like **Linear Regression, Random Forest, XGBoost, and LSTMs (if using deep learning)**.
- Trained on **historical weather data**, incorporating features such as temperature, humidity, wind speed, and pressure.

### **3. Apache Airflow**
- Used to **orchestrate the pipeline**, ensuring efficient scheduling, monitoring, and dependency management.
- DAGs (Directed Acyclic Graphs) define the workflow for **extracting, transforming, loading, training ML models, and making predictions**.

### **4. Google Cloud Storage (GCS)**
- Acts as **intermediate storage** for processed weather data before being ingested into BigQuery.

### **5. Google BigQuery (BQ)**
- Used for **storing, querying, and analyzing** weather data.
- Runs **SQL-based queries** to derive insights and store ML model predictions.

---

## Workflow

1. The pipeline starts by **extracting** weather data for the specified locations using the **OpenWeatherMap API**.
2. The **raw data** is **transformed**, formatted, and cleaned for analysis.
3. The **processed data** is stored in **Google Cloud Storage (GCS)**.
4. The data is then **loaded into Google BigQuery (BQ)** for further analysis.
5. **A machine learning model is trained** using historical weather data.
6. **Predictions** are generated for **the next day's weather** and stored in **BigQuery**.

---

## Usage

To use this pipeline, you need to **set up** the following:
- **Apache Airflow** (for orchestration)
- **Google Cloud Storage (GCS)** (for intermediate data storage)
- **Google BigQuery (BQ)** (for querying and analysis)
- A list of **locations** for which you want to fetch weather data.
- A scheduled Airflow DAG run (e.g., **daily**) to ensure continuous updates.
- **Machine Learning Model Training** to periodically retrain the model.

---

## Setup

### **1. Environment Setup**
Follow these steps to set up the development environment:

1. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials:**
   - Obtain a **Google Cloud Service Account JSON key**.
   - Export the credentials as an environment variable:
     ```sh
     export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-service-account.json"
     ```

### **2. Airflow Configuration**
1. **Initialize the Airflow database:**
   ```sh
   airflow db init
   ```

2. **Start the Airflow webserver:**
   ```sh
   airflow webserver --port 8080
   ```

3. **Start the Airflow scheduler:**
   ```sh
   airflow scheduler
   ```

4. **Access the Airflow UI** at: [http://localhost:8080](http://localhost:8080)

### **3. BigQuery Setup**
1. **Create a new dataset** in **Google BigQuery**:
   ```sql
   CREATE SCHEMA weather_data;
   ```

2. **Create a table** in BigQuery to store the **processed weather data**:
   ```sql
   CREATE TABLE weather_data.weather_forecast (
       location STRING,
       timestamp TIMESTAMP,
       temperature FLOAT64,
       humidity INT64,
       wind_speed FLOAT64,
       weather_condition STRING,
       predicted_temperature FLOAT64,
       predicted_humidity INT64,
       predicted_wind_speed FLOAT64
   );
   ```

---

## Running the Pipeline

1. **Trigger the Airflow DAG**:
   - Navigate to the Airflow UI ([http://localhost:8080](http://localhost:8080)).
   - Locate the DAG named **`load_weather_data`**.
   - Click on **"Trigger DAG"** to start the pipeline.

2. **Monitor the DAG Execution**:
   - Check the **logs** for each task to verify execution.

3. **Train the Machine Learning Model**:
   - The ML model is trained on historical data stored in **BigQuery**.
   - Run the ML training script:
     ```sh
     python train_model.py
     ```
   - The trained model is used to predict **the next day's weather**.

4. **Verify Data in BigQuery**:
   - Run the following query in BigQuery to check if the predictions have been successfully loaded:
     ```sql
     SELECT * FROM weather_data.weather_forecast ORDER BY timestamp DESC LIMIT 10;
     ```

---

## DAG Structure

Below is a high-level structure of the **Airflow DAG** used for this pipeline:

```mermaid
graph TD;
    A[Start Pipeline] --> B[Extract Weather Data]
    B --> C[Transform & Clean Data]
    C --> D[Store Processed Data in GCS]
    D --> E[Load Data into BigQuery]
    E --> F[Train Machine Learning Model]
    F --> G[Generate Next-Day Predictions]
    G --> H[Store Predictions in BigQuery]
    H --> I[End Pipeline]
```

---

## Expected Output

- **BigQuery Table:** Stores processed weather data along with **predicted values** (temperature, humidity, wind speed).
- **Weather Predictions:** Generates **next-day forecasts** using a trained machine learning model.
- **Airflow DAG Execution Logs:** Logs each step of the ETL process, allowing monitoring and debugging.

---

## Troubleshooting

### **1. Airflow Issues**
- If the **Airflow webserver** does not start, try:
  ```sh
  airflow webserver --port 8080 --debug
  ```

- If DAGs are not appearing, ensure the correct `AIRFLOW_HOME` path:
  ```sh
  echo $AIRFLOW_HOME
  ```

### **2. Google Cloud Issues**
- Ensure that your **Google Cloud Service Account** has `BigQuery Data Editor` and `Storage Admin` roles.
- Verify that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is correctly set.

### **3. Machine Learning Issues**
- If predictions are inaccurate, try **retraining the model** with more historical data.
- Experiment with **different models** (e.g., Random Forest, XGBoost, LSTMs) to improve accuracy.

---

## Conclusion

This **weather data pipeline project** demonstrates how to **leverage cloud services, machine learning, and data orchestration tools** to build a **scalable and automated system for weather data analysis and prediction**. By using **Apache Airflow**, **Google Cloud Storage**, **Google BigQuery**, and **machine learning models**, the pipeline efficiently extracts, processes, and analyzes weather data while enabling **automated predictions**.

---

## References

- [Apache Airflow Documentation](https://airflow.apache.org/)
- [Google Cloud Storage Docs](https://cloud.google.com/storage/docs/)
- [Google BigQuery Docs](https://cloud.google.com/bigquery/docs/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Scikit-Learn ML Models](https://scikit-learn.org/stable/)
