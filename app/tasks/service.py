from dataclasses import dataclass

from app.exception import TaskNotFound
from app.tasks.repository import TaskCache, TaskRepository
from app.tasks.shema import TaskShema, TaskCreateShema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self, user_id: int) -> list[TaskShema]:
        if cache_tasks := await self.task_cache.get_task():  # достаем из редис
            return cache_tasks

        tasks = await self.task_repository.get_tasks(user_id=user_id)  # достаем из бд
        tasks_schema = [TaskShema.model_validate(task) for task in tasks]
        await self.task_cache.set_task(tasks_schema)  # кладем в редис
        return tasks_schema

    async def get_all_tasks(self) -> list[TaskShema]:
        if cache_tasks := await self.task_cache.get_task():  # достаем из редис
            return cache_tasks

        tasks = await self.task_repository.get_all_tasks()  # достаем из бд
        tasks_schema = [TaskShema.model_validate(task) for task in tasks]
        await self.task_cache.set_task(tasks_schema)  # кладем в редис
        return tasks_schema

    async def create_task(self, task: TaskCreateShema, user_id: int) -> TaskShema:
        task_id = await self.task_repository.create_task(task, user_id)
        task = await self.task_repository.get_task(task_id)
        return TaskShema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskShema:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if task is None:
            raise TaskNotFound

        task = await self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskShema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if task is None:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id)
