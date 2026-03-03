from uuid import UUID
import uuid
from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict


class MovieSummary(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)

    model_config = ConfigDict(validate_assignment=True)


class Movie:
    def __init__(self, id: UUID, title: str, year: int, genre: str | None, rating: float | None, description: str | None, ):
        self.id = id
        self.title = title
        self.year = year
        self.genre = genre
        self.rating = rating
        self.description = description
