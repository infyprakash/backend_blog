from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import database
import schemas
import utils

models.Base.metadata.create_all(bind=database.engine)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This method return database session objects


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/home')
def home():
    return {"message": "welcome to web technology class"}


# user registration
@app.post('/user/create/')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    the_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if the_user:
        return HTTPException()
    user_obj = models.User(
        email=user.email)
    user_obj.hashed_password = utils.get_password_hash(password=user.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


@app.post("/user/login/")
def create_access_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    the_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if not the_user:
        return HTTPException()
    if not utils.verify_password(plain_password=user.password, hashed_password=the_user.hashed_password):
        return HTTPException()
    access_token = utils.create_access_token(data={'sub': str(the_user.id)})
    return access_token


@app.get('/user/')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()  # select * from "users"
    return users


@app.get('/user/by/email/')
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

# api for category model


@app.post('/category')
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    print(category.dict())
    cat_obj = models.Category(name=category.name)
    db.add(cat_obj)
    db.commit()
    db.refresh(cat_obj)
    return cat_obj


@app.post('/blog/')
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog_obj = models.Blog(
        title=blog.title, content=blog.content, author=blog.author, category=blog.category)
    db.add(blog_obj)
    db.commit()
    db.refresh(blog_obj)
    return blog_obj


@app.get('/blog/')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
