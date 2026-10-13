from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, task, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestão de Tarefas")

app.include_router(user.router)
app.include_router(task.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API Gestão de Tarefas"}
