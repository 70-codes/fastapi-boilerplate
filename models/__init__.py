from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Float,
)

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    fname = Column(String, unique=True)
    lname = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean)
    is_superuser = Column(Boolean)
    is_verified = Column(Boolean)
    created_at = Column(String)
    updated_at = Column(String)
