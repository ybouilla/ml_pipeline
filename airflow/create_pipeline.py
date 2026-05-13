from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model():
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100, max_depth=5)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("accuracy", acc)

        mlflow.sklearn.log_model(model, "model")

with DAG(
    dag_id="mlflow_training_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    train_task

mlflow.set_tracking_uri("http://mlflow-server:5000")