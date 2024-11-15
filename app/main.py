# app/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import os
from schemas import UserRegister, CreatePost, LoginUser
from models import User, Post
import uvicorn

DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+mysqlconnector://root:password@mysql_db:3306/demo_db"
)

app = FastAPI()

# Set up SQLAlchemy database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency for creating and closing database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def welcome():
    return "Welcome to my FastAPI Server"


@app.get("/getusers")
def get_users(db: Session = Depends(get_db)):
    try:
        # Try to execute the query
        users = db.query(User).all()
        return users
    except SQLAlchemyError as e:
        # Handle the exception and return an error message
        return {"error": str(e)}, 400


@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user and db_user.password == user.password:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Invalid username or password")
    except SQLAlchemyError as e:
        return {"error": str(e)}, 400


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        db_user = User(
            username=user.username,
            email=user.email,
            phone=user.phone,
            password=user.password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": f"User {user.username} registered successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}, 400


@app.post("/addposts")
def create_post(post: CreatePost, db: Session = Depends(get_db)):
    try:
        db_post = Post(
            title=post.title, content=post.content, owner_id=1
        )  # Assuming owner_id is 1 for now
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return {"message": f"Post '{post.title}' created successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}, 400


@app.get("/getposts")
def get_users(db: Session = Depends(get_db)):
    try:
        # Try to execute the query
        users = db.query(Post).all()
        return users
    except SQLAlchemyError as e:
        # Handle the exception and return an error message
        return {"error": str(e)}, 400


@app.on_event("startup")
async def startup_event():
    print("Server running at http://127.0.0.1:8000")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
