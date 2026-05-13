# load model

import mlflow.sklearn

model = mlflow.sklearn.load_model("models:/iris_model/Production")

preds = model.predict([[5.1, 3.5, 1.4, 0.2]])
print(preds)