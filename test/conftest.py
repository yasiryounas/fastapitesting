from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.main import app
from app.config import env_settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
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

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com",
                 "password": "test123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password": "test123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
        },{
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
        },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
        },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
        }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model,posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts