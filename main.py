import uvicorn
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_config(path: str ="config.yml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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