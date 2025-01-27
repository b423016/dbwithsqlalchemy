# models are python classes that maps to database tables
#using the orm models pprovides a clear and tructured way to define 
# the database schema and interact with the database.

from sqlalchemy import Column, Integer, String, DateTime, func
from .db_engine import Base

class User(Base): # base is derived  from .db_engine
    """
    it represents a user in the system.
    """
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index=True) #unique id
    username = Column(String, unique=True, index=True, nullable=True) #Username, index is used or faster searches
    email = Column(String, unique=True, index=True, nullable=False) #email
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #time when created
                                               #func.now() is used to get the current time from the server side
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
        #repr provides a string of the user instance helps in logging and debug
        