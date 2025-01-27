# to validate the data  exchange between client and server
# to  creae user creatte and user read and user update 
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """
    It contains the share attributes for user
    """
    username: str = Field(...,min_length=3, max_length=49, example="Ayush Jha")
    email: EmailStr= Field(...,example="chameli420@gmail.com")
          #emailstr is a special tye to validate emails
          # to avoid nullable error
class UserCreate(UserBase):
    """
    schemas for the new user creation
    """    
    password: str =Field(...,min_length=6,example="bitches@69")

class UserRead(UserBase):
    """
    schemas fro seeing user info
    """
    id: int # it should be unique for every user
    created_at: datetime

    class Config:
        orm_mode=True # to make it compatible with the orm model rather than core

class UserUpdate(UserBase):
    """
    schemas for updating the user info
    """
    username: Optional[str]= Field(None, min_length=3,max_length=49, example="Ayush Jha")
    email: Optional[EmailStr]= Field(None, example="chameli420@gmail.com")
    password: Optional[str]=Field(None,min_length=6,example="bitches@69")        
