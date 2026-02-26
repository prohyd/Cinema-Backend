from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict


class MovieCreate(BaseModel):
    title: str = Field(max_length=50)
    year: int = Field(ge=1900, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)
    description: str | None = Field(default=None, max_length=300)


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=50)
    year: int | None = Field(default=None, ge=1900, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)
    description: str | None = Field(default=None, max_length=300)
