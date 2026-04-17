from sqlalchemy.orm import Session
from app.models import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, title: str, description: str, user_id: int):
        task = Task(title=title, description=description, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    def get_all_by_user(self, user_id: int):
        return self.db.query(Task).filter(Task.user_id == user_id).all()
    
    def update(self, task_id: int, user_id: int, update_data: dict):
        task = self.get_by_id(task_id, user_id)
        if task:
            for key, value in update_data.items():
                if value is not None:
                    setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task
    
    def delete(self, task_id: int, user_id: int):
        task = self.get_by_id(task_id, user_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False