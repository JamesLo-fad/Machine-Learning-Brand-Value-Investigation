from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    'Mobile_price_eager',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
    catchup=False,
) as dag:

    kubernetes_min_pod = KubernetesPodOperator(
        task_id='Mobile_price_eager',
        name='mobile',
        namespace='default',
        image='gcr.io/arcane-grin-346209/mobile_meme')
