import models,schemas
from security import hash_password,verify_password,create_access_token
from sqlalchemy.orm import Session
from sqlalchemy import func
def create_user(db:Session,username:str,email:str,password:str):
    hashed_password=hash_password(password)
    new_user=models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "message":"User registered successfully"
    }

def login_user(db:Session,email:str,password:str):
    existing_user=db.query(models.User).filter(models.User.email==email).first()
    if not existing_user:
        return "Invalid email or password"
    if not verify_password(password,existing_user.hashed_password):
        return "Invalid email or password"
    token=create_access_token({"sub":existing_user.username,"user_id":existing_user.id})
    return{
        "access_token":token,
        "token_type":"bearer"
    }


def add_expense(db:Session,title:str,amount:float,category:str,date:str,user_id:int):
    expenses=models.Expenses(
        title=title,
        amount=amount,
        category=category,
        date=date,
        user_id=user_id
    )
    db.add(expenses)
    db.commit()
    db.refresh(expenses)
    return expenses


def get_expenses(
    db: Session,
    user_id: int):
    expenses = db.query(models.Expenses).filter(models.Expenses.user_id == user_id).all()
    return expenses

def filter_month(db: Session, user_id: int, month: str):
    expenses = db.query(models.Expenses).filter(
        models.Expenses.user_id == user_id,
        models.Expenses.date.startswith(month)
    ).all()
    return expenses


def update_expense(
    db: Session,
    expense_id: int,
    title: str,
    amount: float,
    category: str,
    date: str
):
    expense = db.query(models.Expenses).filter(models.Expenses.id == expense_id).first()
    expense.title = title
    expense.amount = amount
    expense.category = category
    expense.date = date
    db.commit()

    return {
        "message": "Expense updated successfully"
    }


def get_total_expense(
    db: Session,
    user_id: int):
    total = db.query(func.sum(models.Expenses.amount)).filter(models.Expenses.user_id == user_id).scalar()
    return total or 0

def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expenses).filter(models.Expenses.id == expense_id).first()
    db.delete(expense)
    db.commit()

def get_user(db, user_id):
    return db.query(models.User).filter(models.User.id == user_id).first()