from abc import ABC, abstractmethod


class MoviesRepository(ABC):
    @abstractmethod
    def get_movie(self, movie_id: int):
        pass

    @abstractmethod
    def create_movie(self, creates: dict):
        pass

    @abstractmethod
    def update_movie(self, updates: dict):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int):
        pass

    @abstractmethod
    def get_movie_cursor(self, limit: int, cursor: str | None = None):
        pass
