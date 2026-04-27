from uuid import UUID
from model.models import MovieSummary, MovieCreate, MovieUpdate, Movie
from repository.models import MovieEntity
from repository.interface import MoviesRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from controller.pagination.cursor import decode_cursor, encode_cursor


class SqlMoviesRepository(MoviesRepository):

    def __init__(self, session: AsyncSession):
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

    async def get_by_id(self, id: UUID):
        movie_found = await self.session.get(MovieEntity, id)

        if movie_found:
            return self._to_domain(movie_found)
        return movie_found

    async def create(self, movie: MovieCreate):

        movie_create = MovieEntity(**movie.model_dump(exclude_unset=True))

        self.session.add(movie_create)
        await self.session.commit()
        await self.session.refresh(movie_create)
        return self._to_domain(movie_create)

    async def delete(self, id: UUID):
        movie_found = await self.session.get(MovieEntity, id)

        if movie_found:
            await self.session.delete(movie_found)
            await self.session.commit()

            return movie_found

        return movie_found

    async def update(self, id: UUID, updates: MovieUpdate):
        movie_found = await self.session.get(MovieEntity, id)

        if movie_found is None:
            return movie_found

        update_data = updates.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(movie_found, field, value)

        await self.session.commit()
        await self.session.refresh(movie_found)

        return self._to_domain(movie_found)

    async def get_by_cursor(self, limit: int, cursor: str | None = None):
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

        result = await self.session.execute(sql_command)

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
