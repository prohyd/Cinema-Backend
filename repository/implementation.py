from uuid import UUID
from utils.custom_errors import ValidationErr
from model.models import MovieSummary
from repository.models import Movie
from repository.interface import MoviesRepository
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from controller.pagination.cursor import decode_cursor, encode_cursor


class SqlMoviesRepository(MoviesRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, movie: Movie) -> MovieSummary:
        return MovieSummary(
            id=movie.id,
            title=movie.title,
            rating=movie.rating
        )

    def get_movie(self, id: UUID):
        movie_found = self.session.get(Movie, id)

        if not movie_found:
            raise ValidationErr("Фильм по такому ID не найден")

        return movie_found

    def create_movie(self, creates: dict):

        movie_create = Movie(
            title=creates.get("title"),
            year=creates.get("year"),
            genre=creates.get("genre"),
            rating=creates.get("rating"),
            description=creates.get("description")
        )

        self.session.add(movie_create)
        self.session.commit()
        self.session.refresh(movie_create)
        return self._to_domain(movie_create)

    def delete_movie(self, id: UUID):
        movie_found = self.session.get(Movie, id)

        if movie_found:
            self.session.delete(movie_found)
            self.session.commit()

            return movie_found

        raise ValidationErr("Элемент по данному ID не найден")

    def update_movie(self, id: UUID, updates: dict):
        movie_found = self.session.get(Movie, id)

        if movie_found is None:
            raise ValidationErr("По заданному ID элемент не найден")

        for field, value in updates.items():
            setattr(movie_found, field, value)

        self.session.commit()
        self.session.refresh(movie_found)

        return self._to_domain(movie_found)

    def get_movie_cursor(self, limit: int, cursor: str | None = None):
        sql_command = select(Movie)

        if cursor:
            created_at, id = decode_cursor(cursor)
            sql_command = sql_command.where(
                or_(
                    Movie.created_at < created_at,
                    and_(
                        Movie.created_at == created_at,
                        Movie.id < id
                    )
                )
            )

        sql_command = (
            sql_command
            .order_by(
                Movie.created_at.desc(),
                Movie.id.desc()
            ).limit(limit + 1)
        )

        result = self.session.execute(sql_command)

        movies = []
        for movie in result.scalars().all():
            movies.append(self._to_domain(movie))

        has_more = len(movies) > limit
        movies = movies[:limit]

        next_cursor = None
        if has_more:
            next_cursor = encode_cursor(movies[-1].created_at, id)

        MovieList = {
            "movies": movies,
            "next_cursor": next_cursor,
            "has_more": has_more,
            "message": "Успешно"
        }
        return MovieList
