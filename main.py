from fastapi import FastAPI
from utils.logging_config import start
from controller.movie.handler import movies
from loguru import logger

app = FastAPI()
app.include_router(movies)


@app.on_event("startup")
def startup():
    config = start()

    env = config["env"]

    server_config = config["server"][env]
    log_config = config["logging"][env]

    logger.info("Приложение запускается в окружении {}", env)