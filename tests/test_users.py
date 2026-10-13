import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_create_user(cliente):
    res = cliente.post(
        "/users/", json={"name": "Jão", "email": "jão@gmail.com", "password": "senha123"})
    
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "jão@gmail.com"
    assert res.status_code == 201

def test_login_user(cliente, test_user):
    res = cliente.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})

    login_resp = schemas.Token(**res.json())
    payload = jwt.decode(login_resp.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_resp.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
     ('felipe@gmail.com', 'password321', 403),
     ('keli@gmailcom', 'senhaerrada', 403),
     ('vitoria@gmail.comm', 'seitudo413', 403),
     (None, 'nadaseitudosei123', 422),
     ('pedefeijão@gmail.com', None, 422)
])
def test_incorrect_login(test_user, cliente, email, password, status_code):
    resp = cliente.post(
         "/login", data={'username': email, 'password': password})

    assert resp.status_code == status_code