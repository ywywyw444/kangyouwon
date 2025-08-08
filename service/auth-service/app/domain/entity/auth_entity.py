from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, func, text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuthEntity(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)