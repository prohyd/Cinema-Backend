from loguru import logger
from config.read_yml import load_config, CONFIG_DIR

def setup(config):

    env = config.get("env", "dev")
    log_config = config["logging"][env]

    logger.remove()

    log_path = CONFIG_DIR / log_config["file"]
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_path,
        level=log_config["level"],
        rotation=log_config.get("rotation"),
        retention=log_config.get("retention"),
        compression=log_config.get("compression"),
        format="{time} | {level} | {name}:{function}:{line} - {message}",
        enqueue=True
    )

    logger.info(f"Логирование настроено для среды: {env}")

    return config
def start():
    return setup(load_config())