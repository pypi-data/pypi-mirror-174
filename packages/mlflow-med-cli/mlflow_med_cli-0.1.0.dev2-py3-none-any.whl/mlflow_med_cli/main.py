import glob
import os
from pathlib import Path
from shutil import copy, rmtree
from urllib.parse import urlparse
from click import Choice
from dotenv import load_dotenv
from .utils import clear_console, load_cfg
import typer
import mlflow

from rich import print
from rich.console import Console
from rich.table import Table

import yaml as py_yaml
import ruamel.yaml

MODULE_HOME = os.path.dirname(os.path.abspath(__file__))

app = typer.Typer()

# load .env
load_dotenv()

MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
MLFLOW_BACKEND_STORE_URI = os.environ.get("MLFLOW_BACKEND_STORE_URI")

# set tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


@app.command()
def create(init: bool = True):
    """
    Initialize project and Create experiment
    """
    clear_console()

    task_type = typer.prompt(
        "What is your task type?",
        type=Choice(["clf", "reg", "det", "seg", "generation"]),
        default="clf",
    )
    experiment_name = typer.prompt("Experiment name")
    experiment_root = typer.prompt("Experiment root", default="./experiments")
    model_name = typer.prompt("Model name", default="MyModel")
    artifact_root = typer.prompt(f"MLFlow artifact root", default=f"/mlartifacts")
    artifact_location = Path(artifact_root) / experiment_name
    framework_type = typer.prompt(
        f"Select ML/DL framework",
        type=Choice(["sklearn", "pytorch", "keras"]),
        default=f"sklearn",
    )
    experiment_path = Path(experiment_root) / task_type / experiment_name

    experiment_info = {"name": experiment_name, "path": str(experiment_path)}

    with open("config.yaml", "w") as f:
        py_yaml.dump(experiment_info, f)

    # Create folder of experiment in {experiment_root}/{task_type}/{experiment_name}
    os.makedirs(experiment_path, exist_ok=True)

    # Write MLFlow code template
    for example_file in glob.glob(
        str(Path(MODULE_HOME) / "examples" / f"{framework_type}" / "*")
    ):
        if not os.path.isfile(example_file):
            continue
        if os.path.basename(example_file) == "MLproject":
            yaml = ruamel.yaml.YAML()
            with open(example_file) as fp:
                cfg = yaml.load(fp)

            # update config
            cfg["name"] = experiment_name
            cfg["model_name"] = model_name
            cfg["artifact_location"] = str(artifact_location)

            with open(experiment_path / "MLproject", "w") as f:
                yaml.dump(cfg, f)
        else:
            copy(example_file, experiment_path)

    # Create MLFlow experiment
    # Note: Remote artifact_location is recommended!! (default: NFS mount)

    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        print(f"Creating a new experiment named as `{experiment_name}`")
        experiment_id = mlflow.create_experiment(
            experiment_name, artifact_location=artifact_location.absolute().as_uri()
        )
        experiment = mlflow.get_experiment(experiment_id)

    print()
    print("=" * 8, "Experiment has been created successfully 🎉", "=" * 8)
    print(f"Experiment_path = {experiment_path}")
    print(f"Experiment_name = {experiment_name}")
    print(f"Task_type = {task_type} ")
    print("Experiment_id = {}".format(experiment.experiment_id))
    print("Artifact Location = {}".format(experiment.artifact_location))
    print("Tags = {}".format(experiment.tags))
    print("Lifecycle_stage = {}".format(experiment.lifecycle_stage))
    print("Creation timestamp = {}".format(experiment.creation_time))


@app.command()
def ls():
    """
    Show existing experiments
    """
    experiment_list = mlflow.list_experiments()

    console = Console()

    # show simple information about experiments in table format
    columns = [
        "experiment_id",
        "name",
        "artifact_location",
        "lifecycle_stage",
        "last_update_time",
        "creation_time",
    ]

    table = Table(*columns)
    for exp in experiment_list:
        row = [str(getattr(exp, col)) for col in columns]
        table.add_row(*row)
    console.print(table)


@app.command()
def update():
    """
    Update experiment information
    """
    create(init=False)


@app.command()
def remove():
    """
    Remove all current experiments
    """
    name = load_cfg()["name"]  # current experiment_name

    experiment = mlflow.get_experiment_by_name(name)
    if not experiment:
        print(f"Experiment `{name}` has already been removed!")
        return
    experiment_id = experiment.experiment_id

    current_experiment = [
        exp for exp in mlflow.list_experiments() if exp.experiment_id == experiment_id
    ]

    # Step 1: delete all artifacts of current experiment
    current_artifact_location = urlparse(current_experiment[0].artifact_location).path
    rmtree(current_artifact_location, ignore_errors=True)

    print(
        f"Deleted entire artifacts at {current_artifact_location} (experiment_name='{name}')"
    )

    # Step 2: delete from DB
    mlflow.delete_experiment(experiment_id)

    # Step 3: delete experiments in `deleted` lifecycle stage. (Note: permanently deletion here)
    os.system(f"mlflow gc --backend-store-uri {MLFLOW_BACKEND_STORE_URI}")


@app.command()
def run(
    entry_point: str = typer.Option(
        "main",
        help="""If specified, corresponding entry_point (custom commands within your project) listed in your `MLproject` is executed. 
        For more detail see https://www.mlflow.org/docs/latest/projects.html
        """,
    )
):
    """
    Run MLFLow experiment
    """
    cfg = load_cfg()
    os.system(
        f"mlflow run -e {entry_point} --experiment-name {cfg['name']} {cfg['path']} --no-conda"
    )


@app.command()
def serve(run_id, host="0.0.0.0", port: int = 3000):
    """
    Runs API server
    """
    # TODO: Introduce Fast API following https://medium.com/analytics-vidhya/fundamentals-of-mlops-part-4-tracking-with-mlflow-deployment-with-fastapi-61614115436
    model_uri = f"runs:/{run_id}/model"
    os.system(f"mlflow models serve -m {model_uri} -h {host} -p {port} --no-conda")


@app.command()
def deploy(target_uri: str = "127.0.0.1"):
    """
    Deploy to custom target.
    """
    pass


@app.command()
def ui(
    port: int = typer.Option(5000, help="Port number"),
    host: str = typer.Option(
        "localhost",
        help="If you want allow all external access, use `0.0.0.0`",
    ),
):
    """
    Run UI server
    """
    os.system(
        f"mlflow ui --backend-store-uri {MLFLOW_BACKEND_STORE_URI} --port {port} --host {host}"
    )


if __name__ == "__main__":
    app()
