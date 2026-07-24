from sqlalchemy import Column,Integer,String,ForeignKey,Float
from database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    username=Column(String(100),unique=True)
    email=Column(String(100),unique=True)
    hashed_password=Column(String(200))
    expenses=relationship("Expenses")

class Expenses(Base):
    __tablename__="Expense"
    id=Column(Integer,primary_key=True)
    title=Column(String(100))
    amount=Column(Float)
    category=Column(String(200))
    date=Column(String(100))
    user_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User")