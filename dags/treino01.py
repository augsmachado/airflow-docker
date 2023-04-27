# Primeira DAG com Airflow

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Argumentos default
default_args = {
    'owner': 'augsmachado',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 23, 19),  # yyyy-mm-dd hh:mm:ss
    'email': ['test@example.com', 'test2@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Vamos definir a DAG - fluxo
dag = DAG(
    'treino-01',
    description='Basico de bash Operators e Python Operators',
    default_args=default_args,
    schedule_interval=timedelta(minutes=2)
)

# Adicionar tarefas

hello_bash = BashOperator(
    task_id='Hello_Bash',
    bash_command='echo "Hello Airflow form Bash"',
    dag=dag
)


def say_hello():
    print("Hello Airflow form Python")


hello_python = PythonOperator(
    task_id='Hello_Python',
    python_callable=say_hello,
    dag=dag,
)

# Vamos adicionar o encadeamento
hello_bash >> hello_python
