from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest
from app import models
from app.oauth2 import create_acess_token

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture()
def session():
    # Recria todas as tabelas antes de cada teste
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def cliente(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(cliente):
    user_data = {"name": "Mazur", "email": "mazur@gmail.com", "password": "senha123"}
    res = cliente.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(cliente):
    user_data = {"name": "Mazur 2", "email": "mazur001@gmail.com", "password": "senha123"}
    res = cliente.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_acess_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(cliente, token):
    cliente.headers = {
        **cliente.headers,
        "Authorization": f"Bearer {token}"
    }
    return cliente

@pytest.fixture
def test_tasks(test_user, session, test_user2):
    tasks_data = [
        {
            "name": "primeira task",
            "descricao": "conteudo da primeira task",
            "user_id": test_user['id']
        },
        {
            "name": "segunda task",
            "descricao": "conteudo da segunda task",
            "user_id": test_user['id']
        },
        {
            "name": "terceira task",
            "descricao": "conteudo da terceira task",
            "user_id": test_user['id']
        },
        {
            "name": "task de outro user",
            "descricao": "conteudo do user 2",
            "user_id": test_user2['id']            
        }
    ]

    def creat_task_model(task):
        return models.Task(**task)
    
    tasks = list(map(creat_task_model, tasks_data))
    session.add_all(tasks)
    session.commit()

    return session.query(models.Task).all()