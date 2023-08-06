from pathlib import Path
import os
import yaml

EXPERIMENT_ROOT = Path(os.path.abspath(__file__)).parent
with open(EXPERIMENT_ROOT / "MLproject") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)
