from sqlalchemy import Column, String, Integer
from config.db import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=False, nullable=False)
    password = Column(String, nullable=False)  


class Admin(Base):
    __tablename__="Admin"

    id=Column(Integer,primary_key=True,index=True)