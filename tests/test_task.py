import pytest
from app import schemas

def test_get_all_tasks(authorized_client, test_tasks, test_user):
    res = authorized_client.get("/task/")
    
    user_tasks = [tarefa for tarefa in test_tasks if tarefa.user_id == test_user['id']]

    assert res.status_code == 200
    assert len(res.json()) == len(user_tasks)

def test_get_other_user_tasks(authorized_client, test_tasks):
    res = authorized_client.get(f"/task/{test_tasks[3].id}")
    assert res.status_code == 403

def test_unauthorized_user_get_one_task(cliente, test_tasks):
    res = cliente.get(f"/task/{test_tasks[0].id}")
    assert res.status_code == 401

def test_get_one_task_not_exist(authorized_client, test_tasks):
    res = authorized_client.get("/task/88888")
    assert res.status_code == 404

def test_get_one_task(authorized_client, test_tasks):
    res = authorized_client.get(f"/task/{test_tasks[0].id}")
    data = res.json()
    assert data["task"]["id"] == test_tasks[0].id
    assert data["task"]["name"] == test_tasks[0].name
    assert data["task"]["descricao"] == test_tasks[0].descricao

@pytest.mark.parametrize('name, descricao', [
    ('Tarefa 1', 'Descrição da tarefa 1'),
    ('Tarefa 2', 'Descrição da tarefa 2'),
    ('Tarefa 3', 'Descrição da tarefa 3')
])
def test_create_task(authorized_client, test_user, test_tasks, name, descricao):
    res = authorized_client.post("/task/", json={
        "name": name,
        "descricao": descricao
    })

    created_task = schemas.TaskResponse(**res.json())
    assert res.status_code == 201
    assert created_task.name == name
    assert created_task.descricao == descricao
    assert created_task.user_id == test_user['id']

def test_unauthorized_user_create_task(cliente, test_tasks):
    res = cliente.post("/task/", json={
        "name": "Tarefa arbitrária",
        "descricao": "Descrição arbitrária"
    })
    assert res.status_code == 401

def test_unauthorized_user_delete_task(cliente, test_tasks):
    res = cliente.delete(f"/task/{test_tasks[0].id}")
    assert res.status_code == 401

def test_delete_task_success(authorized_client, test_user, test_tasks):
    res = authorized_client.delete(f"/task/{test_tasks[0].id}")
    assert res.status_code == 204

def test_delete_task_non_exist(authorized_client, test_user, test_tasks):
    res = authorized_client.delete(f"/task/800000")
    assert res.status_code == 404

def test_delete_other_user_task(authorized_client, test_user, test_tasks):
    res = authorized_client.delete(f"/task/{test_tasks[3].id}")
    assert res.status_code == 403

def test_update_task(authorized_client, test_user, test_tasks):
    data = {
        "name": "nome atualizado",
        "descricao": "descricao atualizada"
    }
    res = authorized_client.put(f"/task/{test_tasks[0].id}", json=data)
    assert res.status_code == 200
    updated_task = schemas.TaskAtualizacao(**res.json())
    assert updated_task.name == data['name']
    assert updated_task.descricao == data['descricao']

def test_update_other_user_task(authorized_client, test_user, test_user2, test_tasks):
    data = {
        "name": "nome atualizado",
        "descricao": "descricao atualizada"
    }
    res = authorized_client.put(f"/task/{test_tasks[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_task(cliente, test_tasks):
    res = cliente.put(f"/task/{test_tasks[0].id}", json={"name": "teste"})
    assert res.status_code == 401

def test_update_task_non_exist(authorized_client, test_user, test_tasks):
    data = {
        "name": "nome atualizado",
        "descricao": "descricao atualizada"
    }
    res = authorized_client.put(f"/task/800000", json=data)
    assert res.status_code == 404