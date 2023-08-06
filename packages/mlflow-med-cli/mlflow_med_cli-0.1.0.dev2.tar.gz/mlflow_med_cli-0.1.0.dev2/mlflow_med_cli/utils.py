import os
import yaml as py_yaml


def clear_console():
    """
    Clearn console
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def load_cfg():
    if not os.path.exists("config.yaml"):
        raise FileNotFoundError(
            f"File not found: `config.yaml` file does not exist. Please configure experiment first through `mlflow-med-cli create` command."
        )
    with open("config.yaml", "r") as f:
        cfg = py_yaml.load(f, Loader=py_yaml.FullLoader)

    return cfg
