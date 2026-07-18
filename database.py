from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
DATABASE_URL="mysql+pymysql://root:lina123@localhost:3306/expense_tracker"
engine=create_engine(DATABASE_URL)
class Base(DeclarativeBase):
    pass
SessionLocal=sessionmaker(bind=engine)