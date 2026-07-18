from fastapi import FastAPI,Form,Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
import crud
app=FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/register")#it shows the registration page
def register_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request":request
        }
    )
@app.post("/register")#after button is clicked the browser sends post/register to fastapi then it executes this defination
def register_user(
    username:str=Form(...),
    email:str=Form(...),
    password:str=Form(...),
    db:Session=Depends(get_db)
):
    return crud.create_user(db,username,email,password)


@app.get("/login")#it shows the registration page
def login_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request":request
        }
    )

@app.post("/login")
def login_user(
    email:str=Form(...),
    password:str=Form(...),
    db:Session=Depends(get_db)
):
    return crud.login_user(db,email,password)