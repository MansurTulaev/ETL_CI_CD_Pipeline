from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import great_expectations as ge
import os
import pandas as pd

def run_extract():
    subprocess.run(["python", "src/extract.py"], check=True)

def run_transform():
    subprocess.run(["python", "src/transform.py"], check=True)

def run_validate():
    try:

        df = pd.read_csv(os.path.join("data", "processed", "weather_transformed.csv"))

        ge_df = ge.from_pandas(df)

        ge_df.expect_column_values_to_not_be_null("time")
        ge_df.expect_column_values_to_be_between("temp_C", min_value=-50, max_value=50)

        results = ge_df.validate()
        print("Validation results:", results)

    except Exception as e:
        print(f"[WARNING] Validation failed but continuing pipeline: {e}")

def run_load():
    subprocess.run(["python", "src/load.py"], check=True)

with DAG(
    dag_id="etl_weather_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["etl", "weather"]
) as dag:

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=run_extract
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=run_transform
    )

    validate = PythonOperator(
        task_id="validate_data",
        python_callable=run_validate
    )

    load = PythonOperator(
    task_id="load_to_s3",
    python_callable=run_load,
    trigger_rule="all_done",  # выполнится даже если предыдущие упали
    )

    extract >> transform >> validate >> load
