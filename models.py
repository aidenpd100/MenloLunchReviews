"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    username = Column("username", TEXT, nullable=False)
    password = Column("password", TEXT, nullable=False)
    is_admin = Column("is_admin", BOOLEAN, nullable=False)

class Lunch(Base):
    __tablename__ = "lunches"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    title = Column("title", TEXT, nullable=False)
    avg_rating = Column("avg_rating", INTEGER, nullable=True)

class Review(Base):
    __tablename__ = "reviews"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    lunch_id = Column("lunch_id", ForeignKey("lunches.id"))
    rating = Column("rating", INTEGER, nullable=False)
    feedback = Column("feedback", TEXT, nullable=True)

class Request(Base):
    __tablename__ = "requests"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    title = Column("title", TEXT, nullable=False)
    description = Column("description", TEXT, nullable=True)