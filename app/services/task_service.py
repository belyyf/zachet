from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositoris.task_repository import TaskRepository
from app.schem import TaskCreate, TaskUpdate, TaskResponse

class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)
    
    def create_task(self, task_data: TaskCreate, user_id: int):
        task = self.task_repo.create(
            title=task_data.title,
            description=task_data.description,
            user_id=user_id
        )
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id
        )
    
    def get_user_tasks(self, user_id: int):
        tasks = self.task_repo.get_all_by_user(user_id)
        return [TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            completed=t.completed,
            user_id=t.user_id
        ) for t in tasks]
    
    def get_task(self, task_id: int, user_id: int):
        task = self.task_repo.get_by_id(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id
        )
    
    def update_task(self, task_id: int, user_id: int, update_data: TaskUpdate):
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
        task = self.task_repo.update(task_id, user_id, update_dict)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id
        )
    
    def delete_task(self, task_id: int, user_id: int):
        deleted = self.task_repo.delete(task_id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}