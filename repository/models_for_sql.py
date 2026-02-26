import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(50), nullable=True)
    rating = Column(Numeric(5, 2), nullable=True)
    description = Column(String(300), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
