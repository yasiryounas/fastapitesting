from .database import client, session
from app import schemas
import pytest
from jose import jwt
from app.config import env_settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password": "test123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


# /users/ is right path, though /users will redirect the api to /users/
# but initially it will send the 307 status code and pytest will only test the first status code

def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test1@gmail.com", "password": "test123"})
    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "test1@gmail.com"
    assert res.status_code == 201


def test_login(test_user, client):
    res = client.post(
        "/login", data={"username": "test1@gmail.com", "password": "test123"})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, env_settings.secret_key, algorithms=[
                         env_settings.algorithm])
    print(res.json())
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    print(res.json())
    assert res.status_code == 200
