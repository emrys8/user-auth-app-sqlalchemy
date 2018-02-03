import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_name = Column(String(100), nullable=False)
    email = Column(String(70), nullable=False)
    password = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///user_app.db')
Base.metadata.create_all(engine)
