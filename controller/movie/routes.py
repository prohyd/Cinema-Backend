from utils.config_err import ValidationErr
from fastapi import FastAPI, Depends, HTTPException
from uuid import UUID
from model.models import MovieCreate, MovieUpdate
from repository.connection import get_db
from repository.implementation import SqlMoviesRepository
from loguru import logger

cinema_backend = FastAPI()


def get_repository(db=Depends(get_db)) -> SqlMoviesRepository:
    return SqlMoviesRepository(db)


@cinema_backend.get("/movies/{id}")
def get_movie_handler(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    try:
        movie_get = repository.get_movie(id)

    except ValidationErr as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info("Фильм id={} успешно найден", id)
    return movie_get


@cinema_backend.get("/movies/")
def get_movie_cursor_handler(limit: int, cursor: str | None = None,
                             repository: SqlMoviesRepository = Depends(get_repository)):
    if limit<1:
        raise HTTPException(status_code=400, detail = "Некорректный limit")

    try:
        movies_get_cursor = repository.get_movie_cursor(limit, cursor)

    except ValidationErr as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info("Найдено {} фильмов", len(movies_get_cursor["movies"]))
    return movies_get_cursor


@cinema_backend.post("/movies/")
def create_movie_handler(movie_create: MovieCreate, repository: SqlMoviesRepository = Depends(get_repository)):
    try:
        movie_create = repository.create_movie(movie_create.model_dump(exclude_unset=True))
    except ValidationErr as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.success("Фильм успешно создан")
    return movie_create


@cinema_backend.patch("/movies/{id}")
def update_movie_handler(id: UUID, updates: MovieUpdate, repository: SqlMoviesRepository = Depends(get_repository)):
    try:
        movie_update = repository.update_movie(id, updates.model_dump(exclude_unset=True))
    except ValidationErr as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.success("Фильм id={} успешно обновлён", id)
    return movie_update


@cinema_backend.delete("/movies/{id}")
def delete_movie_handler(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    try:
        movie_delete = repository.delete_movie(id)
    except ValidationErr as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.success("Фильм id={} успешно удалён", id)
    return movie_delete
