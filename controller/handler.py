from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from controller.models_for_API import MoviesForAPICreate
from repository.create_connection_to_bd import get_bd
from repository.implementation_repository_models import SqlMoviesRepository
from controller.config_log import setup_logging
from loguru import logger
import uvicorn

setup_logging()

app = FastAPI()

def get_repository(db = Depends(get_bd)) -> SqlMoviesRepository:
    return SqlMoviesRepository(db)


@app.get("/movies/{id}")
def get_movie_handler(id: int, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_get = repository.get_movie(id)

    logger.info("Фильм id={} успешно найден", id)
    return movie_get


@app.get("/movies/")
def get_movie_cursor_handler(limit: int, cursor: str | None = None, repository: SqlMoviesRepository = Depends(get_repository)):
    movies_get_cursor = repository.get_movie_cursor(limit, cursor)

    logger.info("Найдено {} фильмов", len(movies_get_cursor["movies"]))
    return movies_get_cursor


@app.post("/movies/")
def create_movie_handler(movie_create: MoviesForAPICreate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_create_answer = repository.create_movie(
        movie_create.name_movie,
        movie_create.rating,
        movie_create.description
    )

    logger.success("Фильм успешно создан")
    return movie_create_answer


@app.patch("/movies/{id}")
def update_movie_handler(id: int, columns: str, new_value, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_update_answer = repository.update_movie(id, columns, new_value)

    logger.success("Фильм id={} успешно обновлён", id)
    return movie_update_answer


@app.delete("/movies/{id}")
def delete_movie_handler(id: int, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_delete_answer = repository.delete_movie(id)

    logger.success("Фильм id={} успешно удалён", id)
    return movie_delete_answer
