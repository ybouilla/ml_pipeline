import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# Start MLflow run
with mlflow.start_run() as run:

    # Model parameters
    n_estimators = 100
    max_depth = 5

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Predictions
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # Log parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Log metric
    mlflow.log_metric("accuracy", acc)

    # Log model and save for later
    mlflow.sklearn.log_model(sk_model=model, artifact_path="model")
    run_id = run.info.run_id
    model_uri = f"runs:/{run_id}/model"

    print(f"Accuracy: {acc}")
    print(f"run id : {run_id}")


# Register model
model_name = "iris_model"

client = MlflowClient()

# Create registered model (only first time)
try:
    client.create_registered_model(model_name)
except Exception:
    pass

# Create a new version
model_version = client.create_model_version(
    name=model_name,
    source=model_uri,
    run_id=run_id
)

print(f"Registered model version: {model_version.version}")


# Promote model to "Production"
client.transition_model_version_stage(
    name="iris_model",
    version=model_version.version,
    stage="Production"
)

# test

mv = client.get_model_version("iris_model", 1)
print("debug", mv.source)

