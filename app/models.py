from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String,nullable=False, unique=True)
    password = Column(String, nullable=False,)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())


class Task(Base):
    __tablename__='task'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)