from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id='treino-03',
    start_date=datetime(2022, 1, 1),
    schedule='0 0 * * *'
) as dag:

    # tasks are represented as operators
    hello = BashOperator(
        task_id='hello',
        bash_command='echo hello'
    )

    @task
    def airflow():
        print('airflow')

    # set dependencies between tasks
    hello >> airflow()
