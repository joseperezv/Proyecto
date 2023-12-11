from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.etl_functions import get_asteroid_data, load_data_to_redshift





api_key = 'vaJwtaRz3N8gCPfOQeh9rOtjRJvchtNyRyvPMZEl'
start_date = '2023-10-10'
end_date = '2023-10-17'


default_args = {
    'owner': 'Jose Daniel Pérez',
    'start_date': datetime(2023, 10, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'ETL_NASA',
    default_args=default_args,
    description='Asteroides',
    schedule_interval=timedelta(days=1),  # Run daily
)


get_asteroid_task = PythonOperator(
    task_id='get_asteroid_data_task',
    python_callable=get_asteroid_data,
    op_args=[api_key, start_date, end_date],
    dag=dag,
)

load_to_redshift_task = PythonOperator(
    task_id='load_data_to_redshift_task',
    python_callable=load_data_to_redshift,
    op_args=[api_key, start_date, end_date],
    provide_context=True,  
    dag=dag,
)


get_asteroid_task >> load_to_redshift_task


