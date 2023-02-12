from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.main import app
from app.config import env_settings
from app.database import get_db, Base
# from alembic import command


# To point it to the test DB for testing purpose

SQLALCHEMY_DATABASE_URL = f"postgresql://{env_settings.database_username}:{env_settings.database_password}@{env_settings.database_hostname}:{env_settings.database_port}/{env_settings.database_name}_test"

# Engine is rsponsible for connecting with database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# to communicate with database
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
# all the model will be extending by this base class
# Base.metadata.create_all(bind=engine)

# dependency


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# #To automatically override the get_db with new test db, i.e. override_get_db
# app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)


# @pytest.fixture(scope="module")
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# @pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    # run our code before we run our test
    # command.upgrade("head")
    # command.downgrade("base")
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)
