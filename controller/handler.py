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



@app.get("/cinema/{movie_id_input}")
def get_movie_handler(movie_id_input: int, db: Session = Depends(get_bd)):
    repository = SqlMoviesRepository(db)

    movie_get = repository.get_movie(movie_id_input)

    logger.info("Кинотеатр id={} успешно найден", movie_id_input)
    return movie_get


@app.get("/cinema/")
def get_movie_cursor_handler(limit: int, cursor: str | None = None, db: Session = Depends(get_bd)):
    repository = SqlMoviesRepository(db)

    movies_get_cursor = repository.get_movie_cursor(limit, cursor)

    logger.info("Найдено {} кинотеатров", len(movies_get_cursor["movies"]))
    return movies_get_cursor


@app.post("/cinema/")
def create_movie_handler(movie_create: MoviesForAPICreate, db: Session = Depends(get_bd)):
    repository = SqlMoviesRepository(db)

    movie_create_answer = repository.create_movie(
        movie_create.name_movie,
        movie_create.rating,
        movie_create.description
    )

    logger.success("Кинотеатр успешно создан")
    return movie_create_answer


@app.patch("/cinema/{movie_id_input}")
def update_movie_handler(movie_id_input: int, columns: str, new_value, db: Session = Depends(get_bd)):
    repository = SqlMoviesRepository(db)

    movie_update_answer = repository.update_movie(movie_id_input, columns, new_value)

    logger.success("Кинотеатр id={} успешно обновлён", movie_id_input)
    return movie_update_answer


@app.delete("/cinema/{movie_id_input}")
def delete_movie_handler(movie_id_input: int, db: Session = Depends(get_bd)):
    repository = SqlMoviesRepository(db)

    movie_delete_answer = repository.delete_movie(movie_id_input)

    logger.success("Кинотеатр id={} успешно удалён", movie_id_input)
    return movie_delete_answer
