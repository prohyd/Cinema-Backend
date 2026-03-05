from uuid import UUID
from utils.config_err import ValidationErr
from model.models import MovieSummary
from repository.models import Movie
from repository.interface import MoviesRepository
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from utils.cursor import decode_cursor, encode_cursor



class SqlMoviesRepository(MoviesRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, movie: Movie) -> MovieSummary:
        return MovieSummary(
            id=movie.id,
            title=movie.title,
            rating=movie.rating
        )

    def get_movie(self, id_movie_input: UUID):
        movie_found = self.session.get(Movie, id_movie_input)

        if not movie_found:
            raise ValidationErr("Фильм по такому ID не найден")

        return self._to_domain(movie_found)

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

    def delete_movie(self, id_movie_input: UUID):
        movie_delete = self.session.get(Movie, id_movie_input)

        if movie_delete:
            self.session.delete(movie_delete)
            self.session.commit()

            return movie_delete

        raise ValidationErr("Элемент по данному ID не найден")

    def update_movie(self, movie_id: UUID, updates: dict):
        movie_update = self.session.get(Movie, movie_id)

        if movie_update is None:
            raise ValidationErr("По заданному ID элемент не найден")

        for field, value in updates.items():
            setattr(movie_update, field, value)

        self.session.commit()
        self.session.refresh(movie_update)

        return self._to_domain(movie_update)

    def get_movie_cursor(self, limit: int, cursor: str | None = None):
        sql_command = select(Movie)

        if cursor:
            created_at, movie_id = decode_cursor(cursor)
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
            ).limit(limit + 1)
        )

        result = self.session.execute(sql_command)
        movies = result.scalars().all()

        has_more = len(movies) > limit
        movies = movies[:limit]

        next_cursor = None
        if has_more:
            next_cursor = encode_cursor(movies[-1].created_at, movie_id)

        MovieList = {
            "movies": movies,
            "next_cursor": next_cursor,
            "has_more": has_more,
            "message": "Успешно"
        }
        return MovieList
