from uuid import UUID
from model.models import MovieSummary, MovieCreate, MovieUpdate, Movie
from repository.models import MovieEntity
from repository.interface import MoviesRepository
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
from controller.pagination.cursor import decode_cursor, encode_cursor


class SqlMoviesRepository(MoviesRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, movie: MovieEntity) -> Movie:
        return Movie(
            id=movie.id,
            title=movie.title,
            rating=movie.rating,
            year = movie.year,
            genre = movie.genre,
            description = movie.description,
            created_at = movie.created_at
        )

    def _to_summary(self, movie: MovieEntity) -> MovieSummary:
        return MovieSummary(
            id=movie.id,
            title=movie.title,
            rating=movie.rating
        )

    def get_by_id(self, id: UUID):
        movie_found = self.session.get(MovieEntity, id)

        if movie_found:
            return self._to_domain(movie_found)
        return movie_found

    def create(self, movie: MovieCreate):

        movie_create = MovieEntity(**movie.model_dump(exclude_unset=True))

        self.session.add(movie_create)
        self.session.commit()
        self.session.refresh(movie_create)
        return self._to_domain(movie_create)

    def delete(self, id: UUID):
        movie_found = self.session.get(MovieEntity, id)

        if movie_found:
            self.session.delete(movie_found)
            self.session.commit()

            return movie_found

        return movie_found

    def update(self, id: UUID, updates: MovieUpdate):
        movie_found = self.session.get(MovieEntity, id)

        if movie_found is None:
            return movie_found

        update_data = updates.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(movie_found, field, value)

        self.session.commit()
        self.session.refresh(movie_found)

        return self._to_domain(movie_found)

    def get_by_cursor(self, limit: int, cursor: str | None = None):
        sql_command = select(MovieEntity)

        if cursor:
            created_at, id = decode_cursor(cursor)
            sql_command = sql_command.where(
                or_(
                    MovieEntity.created_at < created_at,
                    and_(
                        MovieEntity.created_at == created_at,
                        MovieEntity.id < id
                    )
                )
            )

        sql_command = (
            sql_command
            .order_by(
                MovieEntity.created_at.desc(),
                MovieEntity.id.desc()
            ).limit(limit + 1)
        )

        result = self.session.execute(sql_command)

        movies = []
        for movie in result.scalars().all():
            movies.append(self._to_summary(movie))

        has_more = len(movies) > limit
        movies = movies[:limit]

        next_cursor = None
        if has_more:
            next_cursor = encode_cursor(movies[-1].created_at, id)

        if next_cursor is not None:
            MovieList = {
                "movies": movies,
                "nextCursor": next_cursor,
                "hasMore": has_more
            }
        MovieList = {
            "movies": movies,
            "hasMore": has_more
        }
        return MovieList
