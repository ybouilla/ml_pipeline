from mlflow.tracking import MlflowClient

client = MlflowClient()

for rm in client.search_registered_models():
    client.delete_registered_model(rm.name)