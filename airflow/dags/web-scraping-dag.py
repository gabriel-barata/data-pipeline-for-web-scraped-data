from airflow.providers.postgres.operators.postgres import PostgresOperator
from scripts.utils import scrape_data, concat_data, clean_data
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
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
    schedule_interval = "@once",
    template_searchpath = '/otp/airflow/dags/scripts/sql/',
    default_args = default_args

) as dag:

    scrape_data_1 = PythonOperator(

        task_id = "scrape-data-sh",
        python_callable = scrape_data,
        op_kwargs = {

            "url" : "https://www.belezanaweb.com.br/cabelos/shampoo/",
            "table_name" : "shampoo"

        }

    )

    scrape_data_2 = PythonOperator(

        task_id = "scrape-data-cd",
        python_callable = scrape_data,
        op_kwargs = {

            "url" : "https://www.belezanaweb.com.br/cabelos/condicionador/",
            "table_name" : "condicionador"

        }

    )

    scrape_data_3 = PythonOperator(

        task_id = "scrape-data-fl",
        python_callable = scrape_data,
        op_kwargs = {

            "url" : "https://www.belezanaweb.com.br/cabelos/finalizador/",
            "table_name" : "finalizador"

        }

    )

    scrape_data_4 = PythonOperator(

        task_id = "scrape-data-md",
        python_callable = scrape_data,
        op_kwargs = {

            "url" : "https://www.belezanaweb.com.br/cabelos/modelador/",
            "table_name" : "modelador"

        }

    )

    data_concat = PythonOperator(

        task_id = 'concat-data',
        python_callable = concat_data,
        op_kwargs = {'table_name' : 'all_data'}
    
    )

    clean_data = PythonOperator(

        task_id = 'clean-data',
        python_callable = clean_data,
        op_kwargs = {'file_name' : 'all_data'}

    )

    create_table = PostgresOperator( 

        task_id = 'create-table',
        postgres_conn_id = 'airflow-RDS',
        sql = 'create-table.sql',
        autocommit = True

    )

    insert_values = PostgresOperator(

        task_id = 'insert-values',
        postgres_conn_id = 'airflow-RDS',
        sql = 'insert-values.sql',
        autocommit = True
    
    )

scrape_data_1 >> data_concat
scrape_data_2 >> data_concat
scrape_data_3 >> data_concat
scrape_data_4 >> data_concat
data_concat >> clean_data >> create_table >> insert_values