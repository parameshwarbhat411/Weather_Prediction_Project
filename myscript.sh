mkdir data kafka etl preprocessing analysis modeling deployment config logs tests

# Create sub-directories and files
mkdir data/raw data/processed data/models
mkdir deployment/templates deployment/static
touch kafka/data_producer.py kafka/data_consumer.py
touch etl/extraction.py etl/transformation.py etl/loading.py
touch preprocessing/data_cleaning.py preprocessing/feature_engineering.py
touch analysis/eda.ipynb analysis/visualizations.py
touch modeling/train_model.py modeling/evaluate_model.py modeling/predict.py
touch deployment/app.py
touch config/db_config.py config/api_config.py config/kafka_config.py
touch logs/etl_logs.txt logs/kafka_logs.txt
touch tests/test_extraction.py tests/test_transformation.py tests/test_kafka.py
touch README.md requirements.txt
