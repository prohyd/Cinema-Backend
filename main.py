import uvicorn
from controller.config_log import load_config
from loguru import logger


if __name__ == "__main__":
    config = load_config()

    env = config["env"]

    server_config = config["server"][env]
    log_config = config["logging"][env]

    uvicorn.run(
        server_config["app"],
        host=server_config["host"],
        port=server_config["port"],
        reload=server_config["reload"],
        log_level=log_config["level"].lower()
    )