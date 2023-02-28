from datetime import timedelta
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.utils.dates import days_ago
from twitter_etl import twitter_etl

default_args={
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2022,2,27),
    'email': ['celestianc.73@gmail.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=1)
}

dag = DAG(
    'twitter_dag',
    default_args = default_args,
    description = 'Twitter-etl dag'
)

run_etl = PythonOperator(
    task_id = 'twitter_etl_task',
    python_callable =twitter_etl,
    dag = dag

)
