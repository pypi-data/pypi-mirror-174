import logging
import os
from pathlib import Path
import sys
import warnings
import mlflow
from sklearn.datasets import load_iris
import numpy as np
import random
from metrics import eval_metrics
from rich import print
from config import cfg

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


class NotFoundErr(Exception):
    pass


def get_latest_run_id(model_name):
    client = mlflow.client.MlflowClient()
    for rm in client.list_registered_models():
        if rm.name == model_name:
            return rm.latest_versions[0].run_id
    raise NotFoundErr(f"Given model_name `{model_name}` is not found.")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(42)
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 10  # noise steps

    # load trained model
    artifact_location = Path(cfg["artifact_location"])

    latest_run_id = get_latest_run_id(cfg["model_name"])
    model_uri = f"runs:/{latest_run_id}/model"

    print(f"\n🚀 Testing with model_uri={model_uri}\n")
    model = mlflow.sklearn.load_model(model_uri)

    # use best estimator obtained by CV
    model = model.best_estimator_

    step_size = 1.0 / steps

    # Load pure iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    y = (y == 0).astype(int)  # Use binary labels: setosa or not

    experiment = mlflow.get_experiment_by_name(cfg["name"])
    for i in range(steps):
        with mlflow.start_run(experiment_id=experiment.experiment_id):
            noise_level = float(f"{step_size * i:2f}")  # noise_level: [0,1]

            mlflow.log_param("noise_level", noise_level)

            # Test data with noise varing with `noise_level`
            noisy_X = X + noise_level * random.random() * X.max()

            y_pred = model.predict(noisy_X)
            (precision, recall, f1, auc) = eval_metrics(y, y_pred)

            print("[Noise level]: %s" % noise_level)
            print("-  Precision: %s" % precision)
            print("-  Recall: %s" % recall)
            print("-  Auc: %s" % auc)
            print()

            mlflow.log_metric("precision", precision, step=i)
            mlflow.log_metric("auc", auc, step=i)
            mlflow.log_metric("recall", recall, step=i)
