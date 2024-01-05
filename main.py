from fastapi import FastAPI, Request, Depends, Form, HTTPException, Response
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connection import Base, engine, sess_db
from sqlalchemy.orm import Session
from scurity import get_password_hash, create_access_token, verify_token, verify_password, COOKIE_NAME

# Repository
from repositoyuser import SendEmailVerify, UserRepository
# Model
from models import UserModel

templates = Jinja2Templates(directory='templates')

app = FastAPI()
app.mount("/static", StaticFiles(directory='static', html=True), name="static")

# db engine
Base.metadata.create_all(bind=engine)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse('about.html',{'request': request})


@app.get("/user/signin")
def login(req: Request):
    return templates.TemplateResponse("signin.html",{"request": req})


@app.post("/signinuser")
def signin_user(response: Response, db: Session = Depends(sess_db), username: str = Form(), password: str = Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"

    if verify_password(password, db_user.password):
        token = create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return {COOKIE_NAME: token, "token_type": "cairocoders"}


@app.get("/user/signup")
def signup(req: Request):
    return templates.TemplateResponse("signup.html", {"request": req})


@app.post("/signupuser")
def signup_user(db: Session = Depends(sess_db), username: str = Form(), email: str = Form(), password: str = Form()):
    print(username)
    print(email)
    print(password)
    userRepository= UserRepository(db)

    db_user = userRepository.get_user_by_username(username)
    if db_user:
        return "Имя пользователя уже существует"

    signup = UserModel(email=email, username=username, password=get_password_hash(password))
    success = userRepository.create_user(signup)
    token = create_access_token(signup)
    print(token)
    SendEmailVerify.sendVerify(token)

    if success:
        return "Успешное создание пользователя"
    else:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")


@app.get('/user/verify/{token}')
def verify_user(token, db: Session = Depends(sess_db)):
    userRepository = UserRepository(db)
    payload = verify_token(token)
    username = payload.get("username")
    db_user = userRepository.get_user_by_username(username)

    if not username:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    if not db_user.is_active == True:
        return "Ваш аккаунт уже активен"
    db_user.is_active = True
    db.commit()
    response = RedirectResponse(url="/user/signin")
    return response
