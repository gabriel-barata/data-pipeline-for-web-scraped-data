from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.utils import scrape_data
from selenium import webdriver
from airflow import DAG

default_args = {

    'owner' : 'daniella',
    'retries' : 5,
    'retry_delay' : timedelta(minutes = 2)
}

with DAG(

    dag_id = "web-scraping-dag",
    start_date = datetime(2023, 1, 5),
    catchup = False,
    schedule = "@once",
    default_args = default_args

) as dag:

    scrape_data = PythonOperator(

        task_id = "scrape-data",
        python_callable = scrape_data,
        op_kwargs = {

            "url" : "https://www.belezanaweb.com.br/cuidados-pessoais/acessorios/toilette/"

        }

    )