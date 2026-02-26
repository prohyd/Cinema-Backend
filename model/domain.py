from uuid import UUID
import uuid
from pydantic import BaseModel, ValidationError, field_validator, Field, ConfigDict


class MovieSummary(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(max_length=50)
    rating: float | None = Field(default = None,ge=0, le=100)

    model_config = ConfigDict(validate_assignment=True)