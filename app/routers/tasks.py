from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.services.auth_service import AuthService
from app.services.task_service import TaskService
from app.schem import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.get_current_user(token, db)
    return user.id

@router.post("/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.create_task(task_data, user_id)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.get_user_tasks(user_id)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.get_task(task_id, user_id)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update_data: TaskUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.update_task(task_id, user_id, update_data)

@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.delete_task(task_id, user_id)