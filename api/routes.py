# to define the api endpoints for creating, reading, updating and deleting
from fastapi import APIRouter, Depends, HTTPException, status
# depends is used to inject the dependencies into the route functions

from sqlalchemy.orm import Session 
#Session: Represents the database session for performing queries and transactions.
from typing import List
from ..database import models, db_engine
from .schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()    
# creates a router instance to add api endpoint

def get_db():
    db = db_engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """ 
    create a new user
    """
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    get all users
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    get a user by id
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user's information.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    #to check for uniqueness if username or email is being updated
    if user_update.username and user_update.username != user.username:
        if db.query(models.User).filter(models.User.username == user_update.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        user.username = user_update.username
    
    if user_update.email and user_update.email != user.email:
        if db.query(models.User).filter(models.User.email == user_update.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user.email = user_update.email
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by id
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit
    return 
