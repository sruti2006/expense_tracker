from fastapi import FastAPI,Form,Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,HTMLResponse
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from security import verify_token
import models
import crud
app=FastAPI()

@app.get("/")
def home():
    return RedirectResponse(url="/register")


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
    result=crud.login_user(db,email,password)
    if isinstance(result,str):
        return HTMLResponse(result,status_code=401)
    response=RedirectResponse(url="/dashboard",status_code=303)
    response.set_cookie(key="access_token",value=result["access_token"])
    return response



@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login",status_code=303)
    user_id = verify_token(token)
    user=crud.get_user(db,user_id)
    print(user.username)
    expenses = crud.get_expenses(db, user_id)
    total = crud.get_total_expense(db, user_id)
    return templates.TemplateResponse(request=request, name="dashboard.html",
        context={
            "request": request,
            "expenses": expenses,
            "total": total,
            "username":user.username
        }
    )

@app.post("/filter-month")
def filter_month(request: Request, month: str = Form(...), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    user_id = verify_token(token)
    expenses = crud.filter_month(db, user_id, month)
    total = crud.get_total_expense(db, user_id)
    return templates.TemplateResponse(request=request,name="dashboard.html",
        context={
            "request": request,
            "expenses": expenses,
            "total": total
        }
    )
@app.post("/filter-month")
def filter_month(
    request: Request,
    month: str = Form(...),
    db: Session = Depends(get_db)
):
    print(month)

@app.post("/add-expense")
def expenses(
    request:Request,
    title:str=Form(...),
    amount:float=Form(...),
    category:str=Form(...),
    date:str=Form(...),
    db:Session=Depends(get_db)
):
    token = request.cookies.get("access_token")
    user_id = verify_token(token)
    crud.add_expense(db,title,amount,category,date,user_id)
    return RedirectResponse(url="/dashboard",status_code=303)

@app.get("/edit-expense/{expense_id}")
def edit_expense(expense_id: int, request: Request, db: Session = Depends(get_db)):
    expense = db.query(models.Expenses).filter(
        models.Expenses.id == expense_id
    ).first()
    return templates.TemplateResponse( request=request, name="edit_expense.html",
        context={
            "request": request,
            "expense": expense
        }
    )


@app.post("/update-expense/{expense_id}")
def update_expense(
    expense_id: int,
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    crud.update_expense( db,expense_id,title,amount,category,date)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )

@app.post("/delete-expense/{expense_id}")
def delete_expense(expense_id: int,db: Session = Depends(get_db)):
    crud.delete_expense(db, expense_id)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/logout")
def logout():

    response = RedirectResponse( url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response

