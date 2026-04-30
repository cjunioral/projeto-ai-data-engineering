from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow')

from scripts.extract_to_bronze import extract_supermarket_data
from scripts.transform_to_silver import clean_supermarket_data
from scripts.ai_processor import enrich_with_ai


default_args = {
    'owner': 'cjunior',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pipeline_ia_supermercado',
    default_args=default_args,
    description='Pipeline com IA para supermercado',
    schedule_interval='@daily', 
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id='extrair_postgres_para_bronze',
        python_callable=extract_supermarket_data
    )

    task_transform = PythonOperator(
        task_id='limpar_dados_pyspark',
        python_callable=clean_supermarket_data
    )

    task_enrich = PythonOperator(
        task_id='enriquecer_com_ia_groq',
        python_callable=enrich_with_ai
    )

    task_extract >> task_transform >> task_enrich