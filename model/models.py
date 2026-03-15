from uuid import UUID
import uuid
import datetime
from datetime import datetime
from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict
from model.transformees.camelCase import CamelModel


class MovieSummary(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)

    model_config = ConfigDict(validate_assignment=True)


class MovieCreate(BaseModel):
    title: str = Field(max_length=50)
    year: int = Field(ge=1888, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)
    description: str | None = Field(default=None, max_length=300)

    model_config = ConfigDict(extra="forbid")


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=50)
    year: int | None = Field(default=None, ge=1900, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)
    description: str | None = Field(default=None, max_length=300)

    model_config = ConfigDict(extra="forbid")


class Movie(CamelModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(max_length=50)
    year: int = Field(ge=1888, le=2100)
    genre: str | None = Field(default=None, max_length=50)
    rating: float | None = Field(default=None, ge=0, le=100)
    description: str | None = Field(default=None, max_length=300)
    created_at: datetime = Field(default_factory=datetime.utcnow)