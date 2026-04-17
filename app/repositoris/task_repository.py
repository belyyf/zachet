from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Task

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, title: str, description: str, user_id: int):
        task = Task(title=title, description=description, user_id=user_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def get_by_id(self, task_id: int, user_id: int):
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_by_user(self, user_id: int):
        result = await self.db.execute(select(Task).where(Task.user_id == user_id))
        return result.scalars().all()
    
    async def update(self, task_id: int, user_id: int, update_data: dict):
        task = await self.get_by_id(task_id, user_id)
        if task:
            for key, value in update_data.items():
                if value is not None:
                    setattr(task, key, value)
            await self.db.commit()
            await self.db.refresh(task)
        return task
    
    async def delete(self, task_id: int, user_id: int):
        task = await self.get_by_id(task_id, user_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
            return True
        return False