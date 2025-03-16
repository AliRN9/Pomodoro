from dataclasses import dataclass
from typing import List, Optional, Sequence
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.models import Tasks as DBTasks
from app.models import Categories as DBCategories
from app.shema import TaskCreateShema


@dataclass
class TaskRepository:
    db_session: AsyncSession

    async def get_user_task(self, task_id, user_id: int) -> DBTasks:
        query = select(DBTasks).where(DBTasks.user_id == user_id, DBTasks.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
            return task

    async def get_tasks(self, user_id: int) -> Sequence[DBTasks]:
        query = select(DBTasks).where(DBTasks.user_id == user_id)
        async with self.db_session as session:
            tasks = (await session.execute(query)).scalars().all()
        return tasks

    async def get_task(self, task_id: int) -> Optional[DBTasks]:
        query = select(DBTasks).where(DBTasks.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateShema, user_id: int) -> int:
        task_model = DBTasks(name=task.name,
                             pomodoro_count=task.pomodoro_count,
                             category_id=task.category_id,
                             user_id=user_id)
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id

    async def update_task_name(self, task_id: int, name: str, ) -> DBTasks:
        query = update(DBTasks).where(DBTasks.id == task_id).values(name=name).returning(
            DBTasks.id)
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.flush()
            await session.commit()
            return await self.get_task(task_id)

    async def delete_task(self, task_id: int, ) -> None:
        query = delete(DBTasks).where(DBTasks.id == task_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> Sequence[DBTasks]:
        query = select(DBTasks).join(DBCategories, DBTasks.category_id == DBCategories.id).where(
            DBCategories.name == category_name)
        async with self.db_session as session:
            tasks: Sequence[DBTasks] = (await session.execute(query)).scalars().all()
            return tasks
