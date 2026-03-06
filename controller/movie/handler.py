from fastapi import Depends, HTTPException, APIRouter, Query
from uuid import UUID
from model.models import MovieCreate, MovieUpdate
from repository.connection import get_db
from repository.implementation import SqlMoviesRepository
from loguru import logger

movies = APIRouter()


def get_repository(db=Depends(get_db)) -> SqlMoviesRepository:
    return SqlMoviesRepository(db)


@movies.get("/movies/{id}")
def get_movie(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = repository.get_movie(id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.info("Фильм id={} успешно найден", id)
    return movie


@movies.get("/movies")
def get_movie_cursor(
        limit: int = Query(default=10, ge=1, le=100),
        cursor: str | None = None,
        repository: SqlMoviesRepository = Depends(get_repository)
):
    movies = repository.get_movie_cursor(limit, cursor)

    logger.info("Найдено {} фильмов", len(movies["movies"]))
    return movies


@movies.post("/movies")
def create_movie(movie_create: MovieCreate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = repository.create_movie(movie_create.model_dump(exclude_unset=True))

    logger.success("Фильм успешно создан")
    return movie


@movies.patch("/movies/{id}")
def update_movie(id: UUID, updates: MovieUpdate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = repository.update_movie(id, updates.model_dump(exclude_unset=True))

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.success("Фильм id={} успешно обновлён", id)
    return movie


@movies.delete("/movies/{id}")
def delete_movie(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = repository.delete_movie(id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.success("Фильм id={} успешно удалён", id)
    return movie
