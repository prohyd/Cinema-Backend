from abc import ABC, abstractmethod


class MoviesRepository(ABC):
    @abstractmethod
    def get_by_id(self, movie_id: int):
        pass

    @abstractmethod
    def create(self, creates: dict):
        pass

    @abstractmethod
    def update(self, updates: dict):
        pass

    @abstractmethod
    def delete(self, movie_id: int):
        pass

    @abstractmethod
    def get_by_cursor(self, limit: int, cursor: str | None = None):
        pass
