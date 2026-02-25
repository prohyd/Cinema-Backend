from abc import ABC, abstractmethod


class MoviesRepository(ABC):
    @abstractmethod
    def get_movie(self, movie_id: int):
        pass

    @abstractmethod
    def create_movie(self, name_movie: str, rating: float, description: str):
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, update_colums: str, new_value):
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int) -> None:
        pass

    @abstractmethod
    def get_movie_cursor(self, skip: int, limit: int):
        pass
