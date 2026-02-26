from uuid import UUID
from model.domain import MovieSummary
from repository.models_for_sql import Movie
from repository.interface_repository_model import MoviesRepository
from sqlalchemy.orm import Session
from sqlalchemy import select,and_,or_
from controller.utils.cursor import decode_cursor, encode_cursor
from loguru import logger


class SqlMoviesRepository(MoviesRepository):

    def __init__(self, session: Session):
        self.session = session
        logger.info("SqlMoviesRepository инициализирован")

    def _to_domain(self, movie: Movie) -> MovieSummary:
        logger.debug(f"Преобразование ORM в Domain. id={movie.id}")
        return MovieSummary(
            id=movie.id,
            title=movie.title,
            rating=movie.rating
        )

    def get_movie(self, id_movie_input: UUID):
        logger.info(f"get_movie вызван. id={id_movie_input}")

        movie_found = self.session.get(Movie, id_movie_input)

        if not movie_found:
            logger.warning(f"Фильм не найден. id={id_movie_input}")
            answer = {
                "movie": None,
                "message": "Фильм по такому ID не был найден"
            }
            return answer

        logger.info(f"Фильм найден успешно. id={id_movie_input}")
        answer = {
            "movie": self._to_domain(movie_found),
            "message": "Удачно"
        }
        return answer

    def create_movie(self, title: str, year: int, genre: str, rating: float, description: str):
        logger.info(f"create_movie вызван. name={title}, rating={rating}")

        try:
            movie_create = Movie(
                title=title,
                year = year,
                genre = genre,
                rating = rating,
                description = description
            )
        except ValueError as e:
            logger.error(f"Ошибка создания объекта Movies: {e}")
            answer = {
                "movie": None,
                "message": "Некорректные данные"
            }
            return answer

        self.session.add(movie_create)
        self.session.commit()
        self.session.refresh(movie_create)

        logger.info(f"Фильм успешно создан. id={movie_create.id}")

        answer = {
            "movie": self._to_domain(movie_create),
            "message": "Успешно"
        }
        return answer

    def delete_movie(self, id_movie_input: UUID):
        logger.info(f"delete_movie вызван. id={id_movie_input}")

        movie_delete = self.session.get(Movie, id_movie_input)

        if movie_delete:
            self.session.delete(movie_delete)
            self.session.commit()

            logger.info(f"Фильм успешно удалён. id={id_movie_input}")

            answer = {
                "movie": movie_delete,
                "message": "Успешно"
            }
            return answer

        logger.warning(f"Фильм для удаления не найден. id={id_movie_input}")

        answer = {
            "movie": None,
            "message": "Обьект для удаления не был найден"
        }
        return answer

    def update_movie(self, movie_id: UUID, updates: dict):
        logger.info(f"update_movie вызван. id={movie_id}")

        movie_update = self.session.get(Movie, movie_id)

        if movie_update is None:
            logger.warning(f"Некорректный ID для обновления: {movie_id}")
            answer = {
                "movie": None,
                "message": "Некорректный ID"
            }
            return answer

        for field, value in updates.items():
            if not hasattr(movie_update, field):
                logger.warning(f"Некорректное имя столбца: {field}")
                answer = {
                    "movie": None,
                    "message": "Некорретное название столбца"
                }
                return answer

            try:
                setattr(movie_update, field, value)
            except ValueError as e:
                logger.error(f"Некорректное новое значение: {e}")
                answer = {
                    "movie": None,
                    "message": "Некорретное новое значение"
                }
                return answer

        self.session.commit()
        self.session.refresh(movie_update)

        logger.info(f"Фильм успешно обновлён. id={movie_id}")

        answer = {
            "movie": self._to_domain(movie_update),
            "message": "Успешно"
        }
        return answer

    def get_movie_cursor(self, limit: int, cursor: str | None = None):
        logger.info(f"get_movie_cursor вызван. limit={limit}, cursor={cursor}")

        if limit <= 0:
            logger.warning(f"Некорректный limit: {limit}")
            answer = {
                "movies": None,
                "next_cursor": None,
                "has_more": False,
                "message": "Некорретный limit"
            }
            return answer

        sql_command = select(Movie)

        if cursor:
            created_at,movie_id = decode_cursor(cursor)
            logger.debug(f"Cursor декодирован. last_id={movie_id}")
            sql_command = sql_command.where(
                or_(
                    Movie.created_at < created_at,
                    and_(
                        Movie.created_at == created_at,
                        Movie.id < movie_id
                    )
                )
            )

        sql_command = (
            sql_command
            .order_by(
                Movie.created_at.desc(),
                Movie.id.desc()
            ).limit(limit+1)
        )

        result = self.session.execute(sql_command)
        movies = result.scalars().all()

        has_more = len(movies) > limit
        movies = movies[:limit]

        next_cursor = None
        if has_more:
            next_cursor = encode_cursor(movies[-1].created_at, movie_id)
            logger.debug(f"Сгенерирован next_cursor={next_cursor}")

        logger.info(
            f"Cursor-запрос завершён. Возвращено={len(movies)}, has_more={has_more}"
        )

        answer = {
            "movies": movies,
            "next_cursor": next_cursor,
            "has_more": has_more,
            "message": "Успешно"
        }
        return answer
