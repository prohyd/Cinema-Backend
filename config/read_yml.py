from pathlib import Path
import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent


def load_config(path=CONFIG_DIR / "config.yml"):
    path_obj = Path(path)

    if path_obj.suffix.lower() not in [".yml", ".yaml"]:
        return None

    with open(path_obj, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        return config