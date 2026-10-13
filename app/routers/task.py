from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2
from fastapi import APIRouter, Depends, HTTPException, Response, status


router = APIRouter(
    prefix="/task",
    tags=["Task"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskResponse)
def create_task(task: schemas.Task, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    new_task = models.Task(user_id=current_user.id, **task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    task = db.query(models.Task).filter(models.Task.user_id == current_user.id,
    models.Task.name.contains(search)).limit(limit).offset(skip).all()

    return task

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User_Task)
def get_task(id: int, db: Session = Depends(get_db),
            current_user: models.User = Depends(oauth2.get_current_user)):

    task = db.query(models.Task).filter(models.Task.id == id).first()

    if not task:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task com esse id : {id} não existe ")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Não é permitido ver uma task que não seja sua")

    user = db.query(models.User).filter(models.User.id == task.user_id).first()

    return {
        "task": task,
        "user": user
    }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):

    task_query = db.query(models.Task).filter(models.Task.id == id)

    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'task com esse id: {id} não existe')


    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Não é permitido deletar uma task que não seja sua')

    task_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.TaskAtualizacao)
def update_task(id: int, update_task: schemas.TaskAtualizacao, db: Session = Depends(get_db),
                 current_user: models.User = Depends(oauth2.get_current_user)):

    task_query = db.query(models.Task).filter(models.Task.id == id)

    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'task com esse id: {id} não existe')

    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Não é permitido atualizar uma task que não seja sua')

    task_query.update(update_task.model_dump(exclude_unset=True))
    db.commit()

    return task_query.first()


    