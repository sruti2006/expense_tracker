from pydantic import BaseModel
class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class ExpenseCreate(BaseModel):
    title:str
    amount:float
    category:str
    date:str