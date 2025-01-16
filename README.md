# Weather Data Pipeline

## Overview

This project aims to build a **data pipeline** that extracts past **24-hour weather data** for specified locations, processes the data, and uses it to **predict the next day's weather**. The pipeline is orchestrated using **Apache Airflow**, with **Google Cloud Storage (GCS)** serving as the data storage solution and **Google BigQuery (BQ)** for data analysis and prediction.

By leveraging **cloud-based data orchestration and storage**, this pipeline automates the **extraction, transformation, and loading (ETL) process** while ensuring scalability and reliability.

---

## Components

### **1. ETL Process**
The **Extract, Transform, Load (ETL)** process is the **core of the pipeline** and consists of the following stages:

- **Extraction**: Retrieves weather data for specified locations from the **OpenWeatherMap API**.
- **Transformation**: Processes the raw weather data to extract relevant features and **clean the data** for analysis.
- **Loading**: Stores the **processed data** in **Google Cloud Storage (GCS)** and loads it into **Google BigQuery (BQ)** for further analysis.

### **2. Apache Airflow**
- Used to **orchestrate the pipeline**, ensuring efficient scheduling, monitoring, and dependency management.
- DAGs (Directed Acyclic Graphs) define the workflow for **extracting, transforming, and loading** the weather data.

### **3. Google Cloud Storage (GCS)**
- Acts as **intermediate storage** for processed weather data before being ingested into BigQuery.

### **4. Google BigQuery (BQ)**
- Used for **storing, querying, and analyzing** weather data.
- Runs **SQL-based queries** to derive insights and predict the **next day's weather**.

---

## Workflow

1. The pipeline starts by **extracting** weather data for the specified locations using the **OpenWeatherMap API**.
2. The **raw data** is **transformed**, formatted, and cleaned for analysis.
3. The **processed data** is stored in **Google Cloud Storage (GCS)**.
4. The data is then **loaded into Google BigQuery (BQ)** for further analysis.
5. **Predictions** are generated based on the **past 24-hour weather data** to forecast the **next day's weather**.

---

## Usage

To use this pipeline, you need to **set up** the following:
- **Apache Airflow** (for orchestration)
- **Google Cloud Storage (GCS)** (for intermediate data storage)
- **Google BigQuery (BQ)** (for querying and analysis)
- A list of **locations** for which you want to fetch weather data.
- A scheduled Airflow DAG run (e.g., **daily**) to ensure continuous updates.

---

## Setup

### **1. Environment Setup**
Follow these steps to set up the development environment:

1. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
