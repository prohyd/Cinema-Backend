from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict


class MoviesForAPI(BaseModel):
    id_movie: int = Field(ge=0, le=150)
    name_movie: str = Field(max_length=50)
    rating: float = Field(ge=0, le=100)
    description: str = Field(max_length=300)

    model_config = ConfigDict(validate_assignment=True)