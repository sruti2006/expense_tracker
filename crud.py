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
    token=create_access_token({"sub":existing_user.username})
    return{
        "access_token":token,
        "token_type":"bearer"
    }
