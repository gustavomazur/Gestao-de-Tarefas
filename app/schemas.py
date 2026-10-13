
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    name:str
    descricao:str 

class TaskResponse(BaseModel):
    id: int 
    name:str
    descricao:str
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True) 

class UserResponse(BaseModel):
    id: int
    name:str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class User_Task(BaseModel):
    user: UserResponse
    task: TaskResponse 
    model_config = ConfigDict(from_attributes=True) 

class TaskAtualizacao(BaseModel):
    name: Optional[str] = None
    descricao: Optional[str] = None

class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None    
