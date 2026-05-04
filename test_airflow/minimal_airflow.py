from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def say_hello():
    print("Hello from Airflow!")

dag = DAG(
    dag_id="minimal_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",   # 👈 use schedule (not schedule_interval)
    catchup=False,
)

start = PythonOperator(
    task_id="start_task",
    python_callable=lambda: print("Start"),
    dag=dag,
)

hello = PythonOperator(
    task_id="hello_task",
    python_callable=say_hello,
    dag=dag,
)

end = PythonOperator(
    task_id="end_task",
    python_callable=lambda: print("End"),
    dag=dag,
)

start >> hello >> end