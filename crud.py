import models,schemas
from security import hash_password,verify_password,create_access_token
from sqlalchemy.orm import Session
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
        return "user not found"
    if not verify_password(password,existing_user.hashed_password):
        return "wrong password"
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
    return{
        "message":"expenses added successfully"
    }
def get_expenses(
    db: Session,
    user_id: int):
    expenses = db.query(models.Expenses).filter(models.Expenses.user_id == user_id).all()
    return expenses