from loguru import logger
from pathlib import Path
import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent


def load_config(path=CONFIG_DIR / "config.yml"):
    path_obj = Path(path)

    if path_obj.suffix.lower() not in [".yml", ".yaml"]:
        return None

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    env = config.get("env", "dev")
    log_config = config["logging"][env]

    logger.remove()

    logger.add(
        log_config["file"],
        level=log_config["level"],
        rotation=log_config.get("rotation"),
        retention=log_config.get("retention"),
        compression=log_config.get("compression"),
        format="{time} | {level} | {name}:{function}:{line} - {message}",
        enqueue=True,
        mode = "w"
    )

    logger.info(f"Логирование настроено для среды: {env}")
    return config
