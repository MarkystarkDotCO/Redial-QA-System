<!-- Airflow Install -->
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.4/docker-compose.yaml'
AIRFLOW_UID=50000
<!-- run on background -->
docker-compose up -d

<!-- run on session -->
docker-compose up

<!-- login  -->
username: airflow
password: airflow