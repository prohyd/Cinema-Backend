from abc import ABC, abstractmethod


class MoviesRepository(ABC):
    @abstractmethod
    def get_movie(self, movie_id: int):
        pass

    @abstractmethod
    def create_movie(self, title: str, rating: float, description: str,year: int,genre: str):
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, update_colums: str, new_value):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        pass

    @abstractmethod
    def get_movie_cursor(self, limit: int, cursor: str | None = None):
        pass
