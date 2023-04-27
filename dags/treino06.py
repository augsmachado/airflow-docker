# Learn place: https://betterdatascience.com/apache-airflow-rest-api/

import json
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

#
# def save_posts(ti) -> None:
#    posts = ti.xcom_pull(task_ids=['get_posts'])
#    with open('/Users/augsmachado/Desktop/Development/airflow-docker/files/posts.json', 'w') as f:
#        json.dump(posts[0], f)

# handle response


def handle_response(response):
    if response.status_code == 200:
        print('200 OK')
        return True
    else:
        print("Error")
        return False


with DAG(
    dag_id='treino-06',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False
) as dag:

    # 1. Check if the API is up
    task_is_api_active = HttpSensor(
        task_id="is_api-active",
        http_conn_id="treino_06_api_posts",
        method='POST',
        endpoint="",
        dag=dag,
    )

    # 2. Save the posts
#    task_save = PythonOperator(
#        task_id='save_posts',
#        python_callable=save_posts
#    )

    # 3. POST
    task_post_to_webhook = SimpleHttpOperator(
        task_id='post_to_webhook',
        http_conn_id="treino_06_api_posts",
        # method='POST',
        endpoint='/',
        data=json.dumps({"priority": 3}),
        headers=({"Content-Type": "application/json"}),
        response_check=lambda response: handle_response(response),
        log_response=True,
        dag=dag,
    )

    # 4. GET horizon status
    task_get_horizon_status = SimpleHttpOperator(
        task_id='get_horizon_status',
        http_conn_id="horizon_api",
        method='GET',
        endpoint='/',
        headers=({"Content-Type": "application/json"}),
        response_check=lambda response: handle_response(response),
        log_response=True,
        dag=dag
    )

task_is_api_active >> task_get_horizon_status
task_is_api_active >> task_post_to_webhook
