from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG

default_args = {

    'owner' : 'daniella',
    'retries' : 5,
    'retry_delay' : timedelta(minutes = 2)
}

with DAG(

    dag_id = "test-dag",
    start_date = datetime(2023, 1, 5),
    catchup = False,
    schedule = "@once",
    default_args = default_args

) as dag:

    task1 = BashOperator(
        task_id = 'teste',
        bash_command = "echo Everything up!"
    )