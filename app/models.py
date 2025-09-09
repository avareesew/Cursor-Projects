from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Contestant(Base):
    __tablename__ = "contestants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    bio = Column(String(2000), nullable=True)


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(200), nullable=False, index=True)
    email = Column(String(320), nullable=True, index=True)
    picks = Column(JSON, nullable=False)  # list of contestant names/ids
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
