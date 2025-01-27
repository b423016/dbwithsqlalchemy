# to write the test cases for the database operations
import pytest # a framework fro writing test
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from backend.database.models import Base, User
from backend.database.db_engine import get_db
from typing import Any

TEST_DB_URL = "sqlite:///./test.db"# to create a in memory sqlite db testing
#efficient and no need to make a seperate database 

#to set up the engien and session maker
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # create databse seesion to test the databse engine

@pytest.fixture(scope="session") # runs once per session
def setup_database():
    """
    creating the atbles before the test and dropping after the test
    """
    Base.metadata.create_all(bind=engine)
    yield # provides the session to the test func
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(setup_database):
    """
    to make a sqlaclhemy session for the test
    """
    connection= engine.connect()
    transaction= connection.begin()
    session= TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_user(session: Any) -> User:
    """
    sample use
    """
    user = User(username="pussy", email="billodiyejatni@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def test_create_user(session):
    """
    testing fro new user creation
    """
    user = User(username="chinar", email="abhijeet0569@gmail.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.username == "chinar"
    assert user.email == "abhijeet0569@gmail.com"

def test_create_user_duplicate(session, test_user):
    """
    testing for duplicate user creation which should raise the integrity error

    """
    user1 = User(username="user1", email="duplicate@example.com")
    session.add(user1)
    session.commit()

    user2 = User(username="user1", email="duplicate@example.com")
    session.add(user2)

    with pytest.raises(IntegrityError):
        session.commit()
    
def test_read_user(session, test_user):
    """
    Test retrieving a user by ID.
    """
    retrieved_user = session.query(User).filter(User.id == test_user.id).first()
    assert retrieved_user is not None
    assert retrieved_user.username == test_user.username
    assert retrieved_user.email == test_user.email

def test_update_user(session, test_user):
    """
    Test updating a user's email.
    """
    test_user.email = "updated@example.com"
    session.commit()
    session.refresh(test_user)
    
    assert test_user.email == "updated@example.com"

def test_delete_user(session, test_user):
    """
    Test deleting a user from the database.
    """
    user_id = test_user.id
    session.delete(test_user)
    session.commit()
    
    deleted_user = session.query(User).filter(User.id == user_id).first()
    assert deleted_user is None    