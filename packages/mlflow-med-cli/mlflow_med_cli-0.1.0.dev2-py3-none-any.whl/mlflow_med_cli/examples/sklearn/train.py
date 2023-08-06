import warnings

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

import logging

from config import cfg
from metrics import eval_metrics
import argparse

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--autolog", action="store_true")
    parser.add_argument("cv", nargs="?", default=5, type=int)  # default: 5-fold CV
    parser.add_argument(
        "bootstrap", nargs="?", default=True, type=bool
    )  # default: use bootstrap during subtree training
    args = parser.parse_args()
    if args.autolog:
        mlflow.autolog()

    np.random.seed(42)

    iris = load_iris()

    X, y = iris.data, iris.target
    y = (y == 0).astype(int)  # Use binary labels: setosa or not

    # Split the data into training and test sets. (0.75, 0.25) split.
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    experiment = mlflow.get_experiment_by_name(cfg["name"])

    with mlflow.start_run(
        experiment_id=experiment.experiment_id,
        description="This is sample description",
        tags={
            "project": "My Awesome project",
            "release.candidate": "beta",
            "release.version": "0.0.1",
        },
    ):
        rf = RandomForestClassifier(random_state=42)
        param_grid = [
            {
                "n_estimators": [100, 300, 1000, 3000],
                "max_depth": [10, 30, 100, 300],
            },
            {"criterion": ["gini", "entropy", "log_loss"], "bootstrap": [False]},
        ]
        rf = GridSearchCV(rf, param_grid, cv=args.cv, verbose=3, n_jobs=-1)

        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)

        (precision, recall, f1, auc) = eval_metrics(y_test, y_pred)

        print("-  Precision: %s" % precision)
        print("-  Recall: %s" % recall)
        print("-  Auc: %s" % auc)

        if not args.autolog:  # manual logging
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("auc", auc)
            mlflow.log_metric("recall", recall)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        iris_train = pd.DataFrame(X, columns=iris.feature_names)
        signature = infer_signature(iris_train, rf.predict(iris_train))

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(
                rf,
                "model",
                registered_model_name=cfg["model_name"],
                signature=signature,
            )
        else:
            mlflow.sklearn.log_model(rf, "model", signature=signature)
