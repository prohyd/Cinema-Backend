from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func

Base = declarative_base()


class Movies(Base):
    __tablename__ = 'movies'

    id_movie = Column(Integer, primary_key=True)
    name_movie = Column(String(50), nullable=False)
    rating = Column(Numeric(5, 2), nullable=False)
    description = Column(String(300), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
