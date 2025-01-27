from sqlalchemy import create_engine # manaages the connection pool and daabase interaction
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config # retrieve the .env vars.

"""
orm is a prog technique that converts data between incompatible type systems
it helps in interactign with the databse through the objects rathe than the queries.
"""

#to retrieve the database url from the .env file
DATABASE_URL = config('DATABASE_URL',"sqlite:///./test.db")

#creating the sql alchemy-engine
engine = create_engine(DATABASE_URL,
                           echo=True, #for logging of the sql queries\
                           connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
                           future=True) #future implies the sqlalcehmy 2.0\

#craetint the session class
SessionLocal = sessionmaker(autocommit=False, # to commit manually 
                            autoflush=False, 
                            bind=engine,
                            future=True) # links to a specific database 

#Base class 
Base = declarative_base() # base class for orm model
"""
for the declarative base class, it is the base class for all the models
that we will create in the application. It will be used to create the
tables in the database. facilitating the orm operations.
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()