from fastapi import Depends, HTTPException, APIRouter, Query, status
from uuid import UUID
from model.models import MovieCreate, MovieUpdate
from repository.connection import get_db
from repository.implementation import SqlMoviesRepository
from loguru import logger

movies = APIRouter()


def get_repository(db=Depends(get_db)) -> SqlMoviesRepository:
    return SqlMoviesRepository(db)


@movies.get("/movies/{id}")
async def get_movie(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = await repository.get_by_id(id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.info("Фильм id={} найден", id)
    return movie


@movies.get("/movies")
async def get_movie_cursor(
        limit: int = Query(default=10, ge=1, le=100),
        cursor: str | None = None,
        repository: SqlMoviesRepository = Depends(get_repository)
):
    movies = await repository.get_by_cursor(limit, cursor)

    logger.info("Найдено {} фильмов", len(movies["movies"]))
    return movies


@movies.post("/movies", status_code=status.HTTP_201_CREATED)
async def create_movie(movie_create: MovieCreate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = await repository.create(movie_create)

    logger.success("Фильм создан")
    return movie


@movies.patch("/movies/{id}")
async def update_movie(id: UUID, updates: MovieUpdate, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = await repository.update(id, updates)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.success("Фильм id={} обновлён", id)
    return movie


@movies.delete("/movies/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(id: UUID, repository: SqlMoviesRepository = Depends(get_repository)):
    movie = await repository.delete(id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.success("Фильм id={} удалён", id)
