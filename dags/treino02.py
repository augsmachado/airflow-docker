# Dag schedulada para dados do titanic

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

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
    'treino-02',
    description='Extrai dados do Titanic da internet e calcula a idade media dos passageiros',
    default_args=default_args,
    # timedelta(minutes=2) ou None para triggar manualmente ou @<frequencia_arflow>
    schedule_interval='*/2 * * * *'
)

# faz download do arquivo
get_data = BashOperator(
    task_id='get-data',
    bash_command='curl -o ~/titanic.csv https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv',
    dag=dag
)


def calculate_mean_age():
    df = pd.read_csv(
        '~/titanic.csv')
    return df.Age.mean()


def print_age(**context):
    value = context['task_instance'].xcom_pull(tas_ids='calcula-idade-media')
    print(f"A idade media no Titanic era {value} anos")


task_idade_media = PythonOperator(
    task_id='calcula-idade-media',
    python_callable=calculate_mean_age,
    dag=dag
)

task_print_idade = PythonOperator(
    task_id='mostra-idade',
    python_callable=print_age,
    dag=dag
)

get_data >> task_idade_media >> task_print_idade
