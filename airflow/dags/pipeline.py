from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from ..src.download_data import download_data
from ..src.download_data import load_tojson
from ..src.process_data import processing
from ..src.model import model


# # Define the email parameters
# email_params = {
#     'to': 'your_email@example.com',
#     'subject': 'Airflow Alert: Task Failed',
#     'html_content': 'Hi, <br><br> Your Airflow task failed. <br><br> Regards, <br> Airflow'
# }

# # Define the function to send email
# def send_email():
#     send_email(email_params['to'], email_params['subject'], email_params['html_content'])

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'daily_python_scripts',
    default_args=default_args,
    description='Run Python scripts daily',
    schedule_interval=timedelta(days=1),
)

# Define the tasks within the DAG
download_data = PythonOperator(
    task_id='download_data',
    python_callable=download_data.main,
    dag=dag,
)

load_tojson = PythonOperator(
    task_id='load_tojson',
    python_callable=load_tojson.main,
    dag=dag,
)

processing = PythonOperator(
    task_id='processing',
    python_callable=processing.main,
    dag=dag,
)

model = PythonOperator(
    task_id='model',
    python_callable=model.main,
    dag=dag,
)

# Define the task dependencies
download_data >> load_tojson >> processing >> model
