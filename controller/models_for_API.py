from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict


class MoviesForAPICreate(BaseModel):
    name_movie: str = Field(max_length=50)
    rating: float = Field(ge=0, le=100)
    description: str = Field(max_length=300)