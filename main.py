from fastapi import FastAPI
from logger.setup import start
from controller.movie.handler import movies
from loguru import logger
from controller.error.handler import register_validation

app = FastAPI()
app.include_router(movies)
register_validation(app)


@app.on_event("startup")
def startup():
    config = start()

    env = config["env"]

    server_config = config["server"][env]
    log_config = config["logging"][env]

    logger.info("Приложение запускается в окружении {}", env)