from fastapi import FastAPI, Depends
from uuid import UUID
from controller.models_for_API import MovieCreate,MovieUpdate
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
def get_movie_handler(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_get = repository.get_movie(id)

    logger.info("Фильм id={} успешно найден", id)
    return movie_get


@app.get("/movies/")
def get_movie_cursor_handler(limit: int, cursor: str | None = None, repository: SqlMoviesRepository = Depends(get_repository)):
    movies_get_cursor = repository.get_movie_cursor(limit, cursor)

    logger.info("Найдено {} фильмов", len(movies_get_cursor["movies"]))
    return movies_get_cursor


@app.post("/movies/")
def create_movie_handler(movie_create: MovieCreate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_create = repository.create_movie(
        movie_create.title,
        movie_create.year,
        movie_create.genre,
        movie_create.rating,
        movie_create.description
    )

    logger.success("Фильм успешно создан")
    return movie_create


@app.patch("/movies/{id}")
def update_movie_handler(id: UUID, updates: MovieUpdate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_update = repository.update_movie(id,updates.dict(exclude_unset=True))

    logger.success("Фильм id={} успешно обновлён", id)
    return movie_update


@app.delete("/movies/{id}")
def delete_movie_handler(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie_delete = repository.delete_movie(id)

    logger.success("Фильм id={} успешно удалён", id)
    return movie_delete
